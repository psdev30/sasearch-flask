import os
import random
import flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import nltk
from conversions import Conversions
from flask_cors import CORS
import cloudinary, cloudinary.uploader, cloudinary.api
import config

clip_directory = config.clip_directory

nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

config.cloudinary_config()

env = config.env

if env == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config.LOCAL_POSTGRES

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.HEROKU_POSTGRES

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

db = SQLAlchemy(app)


# database model
class Clip(db.Model):
    __tablename__ = 'clip'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    short_path = db.Column(db.String(200), unique=True)
    text = db.Column(db.Text(), unique=False)

    # classification = db.Column(db.Integer, primary_key=True, unique=False)

    def __init__(self, name, short_path, text):
        self.name = name
        self.short_path = short_path
        self.text = text
        # self.classification = classification


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# default server page
@app.route('/')
def landing_page():
    return render_template('index.html')


# just to see cloudinary JSON response for debugging
@app.route('/list_cloudinary', methods=['GET'])
def list_cloudinary():
    return cloudinary.api.resources(resource_type='video')


# handles random query
@app.route('/random', methods=['GET'])
def get_random_clip():
    count = db.engine.execute('select count(id) from clip').scalar()
    random_id = random.randint(1, count)
    return random_search(random_id)


# executes SQL query for /random
def random_search(random_id):
    sql_query = db.engine.execute("SELECT * FROM clip WHERE id = (%s)", random_id)
    for row in sql_query:
        response = cloudinary.Search().expression(row.short_path).execute()
    return flask.jsonify(response['resources'][0]['public_id'])


# handles search query
@app.route('/search/<query>', methods=['GET'])
def query_search(query):
    counter = 0
    cloudinary_resp = dict()
    urls = dict()
    sql_query = db.engine.execute("SELECT * FROM clip WHERE text ILIKE CONCAT('%%', (%s) ,'%%')", query)
    for row in sql_query:
        cloudinary_resp[counter] = cloudinary.Search().expression(row.short_path).execute()
        urls[counter] = cloudinary_resp[counter]['resources'][0]['public_id']
        counter += 1
    return urls


# adds all clips in directory
@app.route('/add_all_clips', methods=['POST'])
def add_all_clips():
    count = 0
    for mp4 in os.listdir(clip_directory):
        file_name = mp4.split('.')[0]
        curr = add_clip(file_name)
        count = count + curr
    return 'successfully added' + count + 'clips!'


# add select clip to cloudinary + db
@app.route('/add_clip/<file_name>', methods=['POST'])
def add_clip(file_name):
    count = 0

    # convert mp4 file to mp3
    mp3, wav = Conversions.convert_to_mp3(file_name)

    # convert mp3 to wav
    Conversions.convert_to_wav(mp3, wav)

    # extract text from wav file & set Clip model properties
    name, short_path, text = Conversions.extract_text(wav, file_name)

    text = text.lower()

    # filters out stopwords before committing to database (decided against it to allow for less specific searches)
    # split_text = text.split()
    # split_text = [word for word in split_text if word not in nltk.corpus.stopwords.words('english')]

    # construct Clip row + push to db if it doesn't already exist
    if db.session.query(Clip).filter(Clip.short_path == short_path).count() == 0:
        new_clip_row = Clip(name, short_path, text)
        db.session.add(new_clip_row)
        db.session.commit()
        file = "clips_library/" + file_name + '.mp4'
        cloudinary.uploader.upload_large(file, resource_type="video", public_id='clips_library/' + file_name)
        Conversions.remove_mp3_wav()
        count += 1
        return count

    Conversions.remove_mp3_wav()
    count += 1
    return count


if __name__ == '__main__':
    app.run()
