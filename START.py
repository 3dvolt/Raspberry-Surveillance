import os
import cv2
import sys
import numpy as np
from flask_basicauth import BasicAuth
from mail import sendEmail
from time import sleep
from datetime import datetime
from PIL import Image
import time
import traceback
from flask import Flask, session, redirect, url_for, escape, request, render_template, Response, flash, abort
from camera import VideoCamera
from flask_mysqldb import MySQL,MySQLdb
import threading
import RPi.GPIO as GPIO

email_update_interval = 600 # sends an email only once in this time interval
video_camera = VideoCamera(flip=False) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") # an opencv classifier

# App Globals (do not edit)
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sorveglianza'
mysql = MySQL(app)
last_epoch = 0

#variabili globali
global panServoAngle
global tiltServoAngle

#angolo massimo
panServoAngle = 90
tiltServoAngle = 90

#pin servo connessi
panPin = 27
tiltPin = 17

#computer vision
def check_for_objects():
	global last_epoch
	while True:
		try:
			frame, found_obj = video_camera.get_object(object_classifier)
			if found_obj and (time.time() - last_epoch) > email_update_interval:
				last_epoch = time.time()
				print("Image captured...")
				#img  = Image.open(frame)
				#nomefile=("static/img/%s") % (str(datetime.now()))
				#img.save(nomefile.jpg, format)
				sendEmail(frame)
				print("Sending email...")
				print("done!")
		except:
			print(traceback.format_exc())
			
			
def gen(camera):
	#streamdellaRpiCamera
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


#pagina principale
@app.route('/')
def index():
      	return render_template('login.html') #di default nella pagina di Login

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


#gestione Login
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        curl = mysql.connection.cursor()
        curl.execute("SELECT * FROM utente u WHERE u.username=%s and u.psw =%s",(email,password,))
        user = curl.fetchone()
        if len(user) > 1:
                curr = mysql.connection.cursor()
                curr.execute("INSERT INTO accessi(FKutente) SELECT u.id FROM utente u WHERE u.username =%s",(email,))
                cur = mysql.connection.cursor()
                Accessi = cur.execute("SELECT a.dataora,u.nome,u.permessi FROM accessi a, utente u where u.ID=a.fkutente limit 5")
                userDetails = cur.fetchall()
				
                currr = mysql.connection.cursor()
                USer = currr.execute("SELECT u.nome FROM utente u where u.username=%s",(email,))
                Username = currr.fetchone()
                Username=''.join(Username)
				
                currrr = mysql.connection.cursor()
                ril = currrr.execute("SELECT a.dataora,a.tipologia_rilevamento,a.email FROM allerte a")
                rilevamento = currrr.fetchall()
                mysql.connection.commit()
                templateData = {
					'userDetails' : userDetails,
					'Username' : Username,
					'rilevamento' : rilevamento
				}
                return render_template("index.html",**templateData)
        else:
            	return index()#render_template("login.html")
    else:
        return index()#render_template("login.html")

#logout della area privata
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return index()

@app.route("/intrusion")
def intrusione():
	cur = mysql.connection.cursor()
	resultValue = cur.execute("SELECT a.dataora,a.tipologia_rilevamento,a.email FROM allerte a")
	userDetails = cur.fetchall()
	return render_template('intrusion.html',userDetails=userDetails)

@app.route("/motor")
def motori():
	return render_template('motor.html')

@app.route('/settings',methods=["GET","POST"])
def impostazioni():
	if request.method == 'POST':
			Email_destinatario = request.form['Email_destinatario']
			Email_mittente = request.form['toemail']
			Password_mittente = request.form['toemailpass']
			motor = request.form['motor']
			cur = mysql.connection.cursor()
			cur.execute("update impostazioni set motore = %s, psw = %s, toemail = %s, email =%s", (motor, Password_mittente, Email_destinatario, Email_mittente))
			mysql.connection.commit()
			return index()
			
	else:
		return render_template('settings.html')

@app.route("/streaming1")
def streaming():
	return render_template('streaming.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO utente(name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return render_template("index.html")

#route per gestire gli angoli del servo per lo spostamento tramite bottoni
@app.route("/<servo>/<angolo>")
def move(servo, angolo):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		panServoAngle = int(angolo)
		os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
	if servo == 'tilt':
		tiltServoAngle = int(angolo)
		os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
	if servo == 'auto':
		os.system("sudo modprobe bcm2835-v4l2")
		os.system("python3 face_tracker.py")

	templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}
	return render_template('motor.html', **templateData)

@app.route('/accessi')
def accessi():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT a.dataora,u.nome,u.permessi FROM accessi a, utente u where u.ID=a.fkutente")
    userDetails = cur.fetchall()
    return render_template('tables.html',userDetails=userDetails)


if __name__ == '__main__':
    app.secret_key = os.urandom(12) #cryptazione
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
