import os
import random
import flask
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import nltk
from selenium.webdriver.chrome.options import Options
# from conversions import Conversions
from flask_cors import CORS
import cloudinary, cloudinary.uploader, cloudinary.api
from selenium import webdriver


clipDirectory = 'C:/Users/psjuk/SASearch/clips_library/'

nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

cloudinary.config(
    cloud_name="dzoq2eys2",
    api_key="134647386342649",
    api_secret="l7kp0buevFOoZjzge7DZkVEVA0Q"
)

env = 'dev'

if env == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/SASearch'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zjpruukwmzslom:f101159ab3c8cbf5d03c955e3e3c035bb6078292a019ee0c4bfdbb0088922bc0@ec2-35-175-155-248.compute-1.amazonaws.com:5432/dfs59f0918ndjr'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Clip(db.Model):
    __tablename__ = 'clip'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    short_path = db.Column(db.String(200), unique=True)
    text = db.Column(db.Text(), unique=True)

    def __init__(self, name, short_path, text):
        self.name = name
        self.short_path = short_path
        self.text = text


# default server page
@app.route('/')
def landingPage():
    return render_template('index.html')


# add all clips in clips_library directory
@app.route('/add_clicked', methods=['POST'])
def add_clips_in_directory():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    for file in os.listdir(clipDirectory):
        file = file.split('.')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://127.0.0.1:5000/add_clip/{}'.format(file[0]))
    return 'successfully added all clips!'


@app.route('/random', methods=['GET'])
def get_random_clip():
    count = db.engine.execute('select count(id) from clip').scalar()
    random_id = random.randint(1, count)
    return random_search(random_id)

def random_search(random_id):
    # results = dict()
    sql_query = db.engine.execute("SELECT * FROM clip WHERE id = (%s)", random_id)
    for row in sql_query:
       response = cloudinary.Search().expression(row.short_path).execute()
    # return response
    return flask.jsonify(response['resources'][0]['public_id'])


    # vid_path = clipDirectory + '/' + results[0]
    # clip = make_response(send_file(vid_path, 'video/mp4'))
    # clip.headers['Content-Disposition'] = 'inline'
    # return clip


# handle search query: ONLY RETURNS FIRST CLIP IF MULTIPLE HITS
@app.route('/search/<query>', methods=['GET'])
def query_search(query):
    cloudinary_resp = dict()
    urls = dict()
    counter = 0
    sql_query = db.engine.execute("SELECT * FROM clip WHERE text LIKE CONCAT('%%', (%s) ,'%%')", (query))
    for row in sql_query:
        cloudinary_resp[counter] = cloudinary.Search().expression(row.short_path).execute()
        urls[counter] = cloudinary_resp[counter]['resources'][0]['public_id']
        counter += 1
    return urls


    # returns a video
    # paths[counter] = i.short_path
    # vid_path = clipDirectory + paths[counter]

    # clip = make_response(send_file(vid_path, 'video/mp4'))
    # clip.headers['Content-Disposition'] = 'inline'
    # return render_template('index.html', clip)
    # return clip


# only for adding clips to library
@app.route('/add-clip/<file_name>', methods=['GET'])
def add_clip(file_name):
    # convert mp4 file to mp3
    wav, mp3 = Conversions.convertToMp3(file_name)

    # convert mp3 to wav
    Conversions.convertToWav(wav, mp3)

    # extract text from wav file & set Clip model properties
    name, short_path, text = Conversions.extractText(wav, file_name)

    # filter out stopwords before committing to database
    text = text.lower()
    split_text = text.split()
    split_text = [word for word in split_text if word not in nltk.corpus.stopwords.words('english')]

    # construct Clip object + push to db if it doesn't already exist
    if db.session.query(Clip).filter(Clip.name == name).count() == 0:
        clip_obj = Clip(name, short_path, split_text)
        db.session.add(clip_obj)
        db.session.commit()

    # add to cloudinary
    file = "clips_library/" + file_name + '.mp4'
    cloudinary.uploader.upload_large(file, resource_type="video", public_id='clips_library/' + file_name)

    return 'clip successfully added to database + cloudinary!'



if __name__ == '__main__':
    app.run()
