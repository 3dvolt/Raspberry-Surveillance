import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import mysql.connector
from datetime import datetime

def sendEmail(image):
	mydb = mysql.connector.connect(
	host="localhost", #MYSQL host
	user="root", #MYSQL user
	passwd="", #Mysql passwd
	database="sorveglianza" #db name
	)

	#get fromEmail from db
	curs1 = mydb.cursor()
	curs1.execute("SELECT i.email FROM impostazioni i")
	fromEmail = curs1.fetchone()
	fromEmail = ''.join(fromEmail)

	#get email passwd from db
	curs2 = mydb.cursor()
	curs2.execute("SELECT i.psw FROM impostazioni i")
	fromEmailPassword = curs2.fetchone()
	fromEmailPassword=''.join(fromEmailPassword)

	#get toEmail from db
	curs3 = mydb.cursor()
	curs3.execute("SELECT i.toemail FROM impostazioni i")
	toEmail = curs3.fetchone()
	toEmail=''.join(toEmail)

	#add new allert --> values
	#url_foto contain the Photo attached email # TODO
	#tipologia_rilevamento contain the type of models used TODO
	curs4 = mydb.cursor()
	curs4.execute('insert into allerte(ID,url_foto,email,tipologia_rilevamento,dataora) values(default,"/img/noname.jpg",%s,"face",default)',(toEmail,))
	mydb.commit()

	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Security Update'
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail
	msgRoot.preamble = 'Raspberry pi security camera update'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Smart security cam found object')
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	msgImage = MIMEImage(image)
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword)
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()
