from flask import Flask, redirect, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, SelectField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug import secure_filename
import os
from Cartoon import cartoonify
from flask_mail import Mail,Message

app = Flask(__name__)
app.secret_key='Our secret key is our secret key. None of your secret key'

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOADED_PHOTOS_DEST = os.path.join(basedir,'static','uploads')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hh5094266@gmail.com'
app.config['MAIL_PASSWORD'] = 'Hhacker@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER']='hh5094266@gmail.com'

cartoon_choices = [('1','Black&White'),('2','Sketch'),('3','Painting')]
class PhotoForm(FlaskForm):
	name = TextField('Name',[validators.Required("Please enter your name")])
	email = TextField('Email',[validators.Required("Please enter your email address."),validators.Email("Please enter valid email address.")])
	photo = FileField('Choose image',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png'],"Only images are allowed")])
	select = SelectField('Select the choice of image',choices=cartoon_choices)
	submit = SubmitField("Submit")

class mailForm(FlaskForm):
	recieve_mail = SelectField('Want to recieve mail of your image?',choices=[('1','Yes'),('2','No')])
	submit = SubmitField('Confirm')

mail = Mail(app)

def send_mail(email,filename):
	msg = Message('Cartoonify',sender='hh5094266@gmail.com',recipients=[email])
	msg.body = 'Thanks for visiting. Please find attached, your image'
	with app.open_resource(os.path.join(UPLOADED_PHOTOS_DEST,'result_'+filename)) as fp:
		msg.attach(filename,"image/png",fp.read())
		mail.send(msg)
		print ('Sent')

@app.route('/',methods=['GET','POST'])
def initial():
	form = PhotoForm()
	print('Server running')
	if request.method == 'GET':
		return render_template('index.html',form=form)
	else: 
		if form.validate_on_submit():
			f = form.photo.data
			try:
				os.remove(os.path.join(UPLOADED_PHOTOS_DEST,secure_filename(f.filename)))
				print('deleted file')
			except:
				print('new file')
			finally:
				f.save(os.path.join(UPLOADED_PHOTOS_DEST, secure_filename(f.filename)))
				cartoonify(f.filename,dict(cartoon_choices).get(form.select.data))
				print(form.email.data,f.filename)
				return redirect(url_for('result',email = form.email.data,filename=f.filename))
		else: 
			return render_template('index.html',form=form)

@app.route('/result',methods=['GET','POST'])
def result():
	form = mailForm()
	if request.method == 'GET':
		return render_template('preview.html',email=request.args.get('email'), filename=request.args.get('filename'), form = form)
	else:
		if form.recieve_mail.data=='1':
			send_mail(request.args.get('email'), request.args.get('filename'))

		return redirect(url_for('initial'))


if __name__ == '__main__':
	app.run(debug = True)