# from when I used to iterate through local file directory
# for file in os.listdir(clipDirectory):
#     file = file.split('.')
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get('https://sasearch-backend.herokuapp.com/add_clip/{}'.format(file[0]))
#     # driver.get('http://127.0.0.1:5000/add_clip/{}'.format(file[0]))
# return 'successfully added all clips!'


# old code that tried to return a video
# paths[counter] = i.short_path
# vid_path = clipDirectory + paths[counter]

# clip = make_response(send_file(vid_path, 'video/mp4'))
# clip.headers['Content-Disposition'] = 'inline'
# return render_template('index.html', clip)
# return clip

# from way back when I was trying to return mp4 files..
# vid_path = clipDirectory + '/' + results[0]
# clip = make_response(send_file(vid_path, 'video/mp4'))
# clip.headers['Content-Disposition'] = 'inline'
# return clip


# cloudinary_response = cloudinary.api.resources(resource_type='video')
# for i in range(len(cloudinary_response['resources'])):
#     public_id = cloudinary_response['resources'][i]['public_id'].split('/')[1]

# driver = webdriver.Chrome(options=chrome_options)
# driver.get('https://sasearch-backend.herokuapp.com/add_clip/{}'.format(public_id))
# driver.get('http://127.0.0.1:5000/add_clip/{}'.format(public_id[1]))
# curr = add_clip(public_id)


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument('--headless')
