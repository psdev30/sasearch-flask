import cloudinary

LOCAL_POSTGRES = 'postgresql://postgres:postgres@localhost/SASearch'

HEROKU_POSTGRES = 'postgres://fgqiizxvcihyjj:135ccc0f72406e82cf6730ef0d77f9789b020f4341e62012b9e59a7090a634e2@ec2-34-195-115-225.compute-1.amazonaws.com:5432/d1d9mkaifbettr'

CLOUD_NAME = "dzoq2eys2"

clip_directory = 'C:/Users/psjuk/PyCharmProjects/SASearch-backend/clips_library/'

env = 'prod'

def cloudinary_config():
    # connect cloudinary to API
    cloudinary.config(
        cloud_name="dzoq2eys2",
        api_key="134647386342649",
        api_secret="l7kp0buevFOoZjzge7DZkVEVA0Q"
    )
