#importing different pakages
from flask import Flask,render_template,request,url_for,redirect,send_file
from flask_mail import Mail,Message 
from werkzeug.utils import secure_filename
import time
import cv2
import os
# re module provides support 
# for regular expressions 
import re 
  
# Make a regular expression 
# for validating an Email 
regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"

#app configurations
application=app=Flask(__name__)

app.config['UPLOAD_FOLDER']= 'uploads/'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USERNAME']='aadarshgupta875@gmail.com'
app.config['MAIL_PASSWORD']=os.environ.get('password')
app.config['MAIL_DEFAULT_SENDER']='aadarshgupta875@gmail.com'

mail=Mail(app)
global output_vedio_filename

@app.route('/',methods=["GET","POST"])
def start():
	return render_template('gray_scale.html')

@app.route('/gray_scale',methods=["POST"])
def gray_scale():

	global output_vedio_filename

	#loads file from html
	videoFile=request.files['filename']

	#retrieves email ID from html
	recipient_id=str(request.form.get("email"))

	#if invalid email is provided 
	if not(re.search(regex,recipient_id)):
		return render_template("gray_scale.html",text="Invalid Email Id")

	#contains filename
	fn=os.path.basename(videoFile.filename)

	#saving file in specified directory
	videoFile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(videoFile.filename)))

	#contains path where file is saved
	videoFile=os.path.join(app.config['UPLOAD_FOLDER'])+fn

	#dividing the file location into its filename and extension
	name, ext =os.path.splitext(videoFile)

	#checking whether the file is videofile or not 
	allowed_extensions=[".mp4" , ".mov" , ".avi" , ".webm" , ".wmv" , ".flv"]
	if (ext.lower() in allowed_extensions)==False:
		return render_template("gray_scale.html",text="not a video file extension")

	#capturing the vedio
	cap=cv2.VideoCapture(videoFile)

	#output file name
	output_vedio_file="gray_"+time.strftime("%Y%m%d_%H%M%S")+ext
	output_vedio_filename=output_vedio_file

	#making mp4 output vedio file
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')

	#Get frame per second of the vedio
	frame_per_second=cap.get(cv2.CAP_PROP_FPS)

	#get frame size
	width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	size=(width,height)

	#Initialize VedioWriter
	out = cv2.VideoWriter(output_vedio_file, fourcc, frame_per_second, size,False)
	while(1):
		ret, frame=cap.read()
		if ret==False:
			break
		gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		out.write(gray)

	cap.release()
	out.release()

	try:
		return send_file(output_vedio_filename,as_attachment=True)
	
		#Message Content that is to be emailed 
		msg=Message(
			subject='Gray_Scale video file',
			recipients=[recipient_id],
			body='Below is your required Gray Scaled video File'
			)

		#attaching gray scale video file
		with app.open_resource(output_vedio_file) as output_file:
			msg.attach(output_vedio_file,'video/mp4',output_file.read())

		#sending mail
		mail.send(msg)

		return render_template("gray_scale.html",text1="Successfully mailed the gray scale videofile to your provided email id",text2="Download")	

	except Exception:
		return render_template("gray_scale.html",text1="Sorry!!! Unable to send to mail... Gmail have protections to avoid their service being used to deliver spam",text2="Download")

@app.route('/download',methods=["GET"])
def download_file():
	global output_vedio_filename
	return send_file(output_vedio_filename,as_attachment=True)
		
if __name__=="__main__":
	app.run()
