from flask import Flask,jsonify,send_file
from flask import request
from instamojohelper import InstamojoHelper
import uuid
import os
app=Flask(__name__,instance_relative_config=True)


# directing to the page based on url
@app.route('/')
def index():
	return send_file('static/index.html')

# url to upload the file
@app.route('/upload/', methods=['POST'])
def upload_file():
    f = request.files['file']
    random_num = uuid.uuid1()
    filename = f.filename+str(random_num)
    f.save(filename)
    insta_obj = InstamojoHelper()
    insta_obj.create_offers_from_file(f.filename+str(random_num))
    return 'ok' 


if __name__=='__main__':
	app.run(host='0.0.0.0',debug=True)