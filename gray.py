#importing different pakages
from flask import Flask,render_template,request,url_for,redirect
from werkzeug.utils import secure_filename
import cv2
import os

app=Flask(__name__)
app.config['UPLOAD_FOLDER']= '/uploads'

@app.route('/',methods=["GET","POST"])
def start():
	return render_template('gray_scale.html')

@app.route('/gray_scale',methods=["POST"])
def gray_scale():

	#form=cgi.FieldStorage()
	videoFile=request.files['filename']

	#contains filename
	fn=os.path.basename(videoFile.filename)

	#saving file in specified directory
	videoFile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(videoFile.filename)))

	#contains path where file is saved
	videoFile=os.path.join(app.config['UPLOAD_FOLDER'])+'/'+fn

	#dividing the file location into its filename and extension
	name, ext =os.path.splitext(videoFile)

	#checking whether the file is videofile or not 
	allowed_extensions=[".mp4" , ".mov" , ".avi" , ".webm" , ".wmv" , ".flv"]
	if (ext.lower() in allowed_extensions)==False:
		return render_template("gray_scale.html",text="Vedio extension not allowed")

	#capturing the vedio
	cap=cv2.VideoCapture(videoFile)

	#output file name
	output_vedio_file="gray_video"+ext

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

	return render_template("gray_scale.html",text="Successfully saved Gray Scaled video with name {}".format(output_vedio_file))
	

if __name__=="__main__":
	app.run()
