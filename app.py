from flask import Flask,jsonify,send_file
from flask import request
from instamojohelper import InstamojoHelper
app=Flask(__name__,instance_relative_config=True)


# directing to the page based on url
@app.route('/')
def index():
	return send_file('static/index.html')

# url to upload the file
@app.route('/upload/', methods=['POST'])
def upload_file():
	print len(request.files)
	f = request.form['file']
	helper_object = InstamojoHelper()
	helper_object.create_offers_from_file(f)	




if __name__=='__main__':
	app.run(host='0.0.0.0',debug=True)