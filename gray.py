#importing different pakages
from flask import Flask,render_template,request,url_for,redirect
from flask_mail import Mail,Message 
from werkzeug.utils import secure_filename
import cv2
import os
# re module provides support 
# for regular expressions 
import re 
  
# Make a regular expression 
# for validating an Email 
regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"

#app configurations
app=Flask(__name__)
app.config.update(dict(
	UPLOAD_FOLDER= 'uploads/',
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=587,
	MAIL_USE_TLS=True,
	MAIL_USE_SSL=False,
	MAIL_USERNAME='aadarshgupta875@gmail.com',
	MAIL_PASSWORD=os.environ.get('password'),
	MAIL_DEFAULT_SENDER='aadarshgupta875@gmail.com',
))

mail=Mail(app)

@app.route('/',methods=["GET","POST"])
def start():
	return render_template('gray_scale.html')

@app.route('/gray_scale',methods=["POST"])
def gray_scale():

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
	output_vedio_file="gray_"+fn

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

		return render_template("gray_scale.html",text="Successfully mailed the gray scale videofile to your provided email id")	

	except Exception:
		return render_template("gray_scale.html",text="Sorry!!! Unable to send to mail... Gmail have protections in place to avoid their service being used to deliver spam")

		
if __name__=="__main__":
	app.run()
