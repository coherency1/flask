from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#create Flask instance
app = Flask(__name__)

#route create
@app.route('/')
def index():
	return render_template('index.html')

#route user
@app.route('/user/<name>')
def user(name):

	return render_template('user.html', name = name)

#form class
app.config['SECRET_KEY'] = "Alexander Gunawan"
class register(FlaskForm):
	name = StringField("Username: ", validators=[DataRequired()])
	password = StringField("Password: ", validators=[DataRequired()])
	submit = SubmitField("Submit")

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	name = None
	password = None
	form = register()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		password = form.password.data
		form.password.data = ''
	return render_template('login.html', name=name, password=password, form=form)

'''
@app.errorhandler(404):
def page_not_found(e):
	return render_template("404.html")
'''