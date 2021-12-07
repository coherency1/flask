from flask import Flask, render_template, request, flash, redirect, url_for, Markup, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import re
from datetime import date, datetime
import pymysql.cursors
import random
from dateutil.relativedelta import relativedelta
from flask import Response
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

	
# change the global variables every time a user logs in!!!!!
# global variables that are used to control search results. some of the functions belonging to different user types render the same html page.
userPrimaryKey = None
loginType = None
permissions = None
airline = None

	# for bar chart if needed
labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]


#create Flask instance
app = Flask(__name__)

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_PORT'] = 8080
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'DatabaseProject'

#Creates a connection to MySQL Database on default port 3306
#Personal my connection to root is 88888888 and my database is FinalProject
cnx = pymysql.connect(

							  host='localhost',
							  port=3306,
							user='root',
                            password='88888888',
	#port=8080,

							  db='FinalProject',
	#cursorclass=pymysql.cursors.DictCursor,


                              )


#Creates a route to Default home page
@app.route('/')
def index():
	#reset all global variables
	global  userPrimaryKey
	global  loginType
	global permissions
	global airline
	userPrimaryKey = None
	loginType = None
	permissions = None
	airline = None
	#cursor.execute('''INSERT INTO airline VALUES ('Sam')''')
	return render_template('index.html')

#route user
@app.route('/search', methods=['GET', 'POST'])
def search():
	with cnx.cursor() as cur:
		query = "select * from flight where status = 'Upcoming'"
		cur.execute(query)
		data = cur.fetchall()
	return render_template('customer_searchforflights.html', data=data, loginType=session[0], default= True)

@app.route('/purchase_info', methods=['GET', 'POST'])
def purchase_info():
	#to specify based on airports, etc as per project page. redirected from view my flight
	return render_template("purchase_info.html", loginType=loginType)

@app.route('/search_info', methods=['GET', 'POST'])
def search_info():
	# to specify based on airports, etc as per project page. redirected from search/purchase.
	return render_template("search_info.html", loginType=loginType)

#Form Class
#Secret Key is set to "Alexander Gunawan"
app.config['SECRET_KEY'] = "Alexander Gunawan"
class register(FlaskForm):
	name = StringField("Username: ", validators=[DataRequired()])
	password = StringField("Password: ", validators=[DataRequired()])
	submit = SubmitField("Submit")

#Creates route to Registration of Users and Dropdown
@app.route('/registers', methods=['GET', 'POST'])
def registers():
	
	if request.method == 'POST':


		registerType =  request.form.get('LoginType')

		if registerType == "1":

			return redirect(url_for('register_customer'))

		elif registerType == "2":
			return redirect(url_for('register_agent'))

		elif registerType == "3":

			return redirect(url_for('register_staff'))


		print(registerType)

	return render_template('register.html')
	
#Creates route to the Booking Agent Registration
@app.route('/register_agent',methods = ['GET','POST'])
def register_agent():
	if request.method == 'POST':
		email = request.form.get('email')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		agentID = request.form.get('agentID')
		with cnx.cursor() as cur:
			query = "SELECT * FROM booking_agent WHERE email = '{}'".format(email)

			cur.execute(query)
			data = cur.fetchone()

			if (data):
				error = "This user already exists!"
				return render_template('register_customer.html', error=error)

			else:
				sql = '''INSERT INTO booking_agent VALUES ('{}','{}','{}')'''.format(email, password1, agentID)

				with cnx.cursor() as cur:
					cur.execute(sql)


				cnx.commit()

				return redirect(url_for('register_success'))

	return render_template('register_agent.html')

#Creates route to the Airline Staff registration
@app.route('/register_staff',methods = ['GET','POST'])
def register_staff():
	if request.method == 'POST':
		username = request.form.get('username')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		first_name = request.form.get('firstName')
		last_name = request.form.get('lastName')
		airlineName = request.form.get('airlineName')
		dob = request.form.get('Date of Birth')
		agentID = request.form.get('agentID')

		with cnx.cursor() as cur:
			query = "SELECT * FROM airline_staff WHERE username = '{}'".format(username)

			cur.execute(query)
			data = cur.fetchone()

			if (data):
				error = "This user already exists!"
				return render_template('register_staff.html', error = error)
			else:
				with cnx.cursor() as cur:

					sql = '''INSERT INTO airline_staff VALUES ('{}','{}','{}','{}','{}','{}')'''.format(username,password1,first_name,last_name,dob,airlineName)

					sql2 = '''INSERT INTO permission VALUES ('{}', 'None')'''.format(username)

					cur.execute(sql)
					cur.execute(sql2)

				cnx.commit()

				return redirect(url_for('register_success'))

	return render_template('register_staff.html')

#Creates route to the Customer registration
@app.route('/register_customer',  methods = ['GET','POST'])
def register_customer():

	if request.method == 'POST':
		email = request.form.get('email')
		first_name = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		buildingNumber = request.form.get('buildingnumber')
		street = request.form.get('Street')
		city = request.form.get('City')
		state = request.form.get('State')
		phoneNumber = request.form.get('Phone Number')
		passportNumber = request.form.get('Passport Number')
		passportExpiration = request.form.get('Passport Expiration')
		passportCountry = street = request.form.get('Street')
		dob = request.form.get('Date of Birth')

		with cnx.cursor() as cur:
			query = "SELECT * FROM customer WHERE email = '{}'".format(email)

			cur.execute(query)
			data = cur.fetchone()

			if (data):
				error = "This user already exists!"
				return render_template('register_customer.html', error=error)
			else:

				sql = '''INSERT INTO customer VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(email, first_name,
																									 password1, buildingNumber,
																									 street, city, state,
																									 phoneNumber,
																									 passportNumber,
																									 passportExpiration,
																			 passportCountry, dob)


				with cnx.cursor() as cur:
					cur.execute(sql)

				cnx.commit()

				return redirect(url_for('register_success'))

	return render_template('register_customer.html')

@app.route('/register_success')
def register_success():
	return render_template('register_success.html')

#Creates route to Login of users and Dropdown
@app.route('/login', methods=['GET', 'POST'])
def login():
	
	if "customer" in session:
		return redirect(url_for("customer_home"))
	elif "booking_agent" in session:
		return redirect(url_for("booking_agent_home"))
	elif "staff" in session:
		return redirect(url_for("airline_staff_home"))
	elif request.method == 'POST':

		loginType =  request.form.get('LoginType')

		if loginType == "1":

			return redirect(url_for('login_customer'))

		elif loginType == "2":
			return redirect(url_for('login_agent'))

		elif loginType == "3":

			return redirect(url_for('login_staff'))

	return render_template('login.html')

#Default Logout route, fixes errors for bugs with navbar so you can logout
@app.route('/logout')
def logout():
	if "customer" in session:
		return redirect(url_for('customer_logout'))
	elif "booking_agent" in session:
		return redirect(url_for('agent_logout'))
	elif "staff" in session:
		return redirect(url_for('staff_logout'))
	return redirect(url_for('index'))

#Creates Logout function for Customers
@app.route('/customer_logout')
def customer_logout():
	session.pop("customer", None)
	return redirect(url_for('index'))

#Creates Logout function for Booking Agents
@app.route('/agent_logout')
def agent_logout():
	session.pop("booking_agent", None)
	return redirect(url_for('index'))

#Creates Logout function for Airline Staff
@app.route('/staff_logout')
def staff_logout():
	session.pop("staff", None)
	return redirect(url_for('index'))

#Creates Login page for customers and creates session for successful logins
@app.route('/login_customer',  methods=['GET', 'POST'])
def login_customer():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		with cnx.cursor() as cur:
			query = "SELECT email, password FROM customer WHERE email = '{}'".format(email)
			cur.execute(query)
			data = cur.fetchone()

			if not (data):
				error = Markup('<p>User not found</p>')
				flash(error)
			else:
				if data[1] != password:
					error = Markup('<p>Incorrect Password</p>')
					flash(error)
				else:
					session["customer"] = email
					return redirect(url_for('customer_home'))
	return render_template('login_customer.html')

#Creates Login page for Booking Agents and creates session for successful logins
@app.route('/login_agent', methods=['GET', 'POST'])
def login_agent():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		with cnx.cursor() as cur:
			query = "SELECT email, password FROM booking_agent WHERE email = '{}'".format(email)
			cur.execute(query)
			data = cur.fetchone()

			if not (data):
				error = Markup('<p>User not found</p>')
				flash(error)
			else:
				if data[1] != password:
					error = Markup('<p>Incorrect Password</p>')
					flash(error)
				else:
					session["booking_agent"] = email
					return redirect(url_for('booking_agent_home'))
	return render_template('login_agent.html')

#Creates Login page for Airline Staff and creates session for successful logins
@app.route('/login_staff', methods=['GET', 'POST'])
def login_staff():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		with cnx.cursor() as cur:
			query = "SELECT username, password FROM airline_staff WHERE username = '{}'".format(username)
			cur.execute(query)
			data = cur.fetchone()
			if not (data):
				error = Markup('<p>User not found</p>')
				flash(error)
			else:
				if data[1] != password:
					error = Markup('<p>Incorrect Password</p>')
					flash(error)
				else:
					session["staff"] = username
					#query = "SELECT permission_type FROM permission WHERE username = '{}'".format(username)
					#cur.execute(query)
					#permissions = cur.fetchone()
					return redirect(url_for('airline_staff_home', permissions=permissions, name=username))
	return render_template('login_staff.html')

'''
@app.route('/search')
def search():
	return render_template('search.html')
#if name = customer, else if name = booking agent
'''


@app.route('/view_public_info', methods=['GET', 'POST'])
def view_public_info():
	pass

#Creates route to home page for logged in customers, kicks to login page if not logged in
@app.route('/customer_home')
def customer_home():
	if "customer" in session:
		email = session["customer"]
		return render_template('customer_home.html', name=email)
	else:
		return redirect(url_for("login"))


@app.route('/customer_purchasetickets', methods = ['GET','POST'])
def customer_purchasetickets(flight):
	if 'customer' in session:
		if request.method == 'POST':
			with cnx.cursor() as cur:
				#search for unbought tickets.
				query2 = "SELECT flight.flight_num,ticket.ticket_ID FROM (flight natural join ticket) left join purchases on ticket.ticket_id = purchases.ticket_id where flight.status = 'Upcoming' and ticket.flight_num = '{}' and purchases.customer_email is null".format(
					flight)
				cur.execute(query2)
				data = cur.fetchone()
				if not data:
					message = 'There is no tickets!'
					return customer_ticketspurchased(message)
				else:
					today = date.today()
					today = today.strftime("%Y-%m-%d")
					ticket_ID = data[1]
					email = userPrimaryKey
					if loginType == 'agent':
						#redirect agent to enter the customer email
						return render_template('booking_agent_purchasing.html',ticket_ID=ticket_ID,today=today)
						#return booking_agent_purchasing(ticket_ID,today)
						#return redirect(url_for('booking_agent_purchasing',ticket_ID=ticket_ID,today=today))
					else:
						query = '''INSERT INTO purchases VALUES ('{}','{}',null,'{}')'''.format(ticket_ID, email, today)
					cur.execute(query)
				cnx.commit()
			message = 'You have bought the ticket! Your ticket number is {} for flight {}'.format(data['ticket_ID'],
																								  data['flight_num'])
			print("Hello")
			return customer_ticketspurchased(message)
		return render_template('customer_purchasetickets.html', user=userPrimaryKey)
	else:
		return redirect(url_for('login'))

@app.route('/customer_ticketspurchased')
def customer_ticketspurchased(message):
	return render_template('customer_ticketspurchased.html', message=message, loginType = loginType)


@app.route('/customer_searchforflights',methods = ['GET','POST'])
def customer_searchforflights():
	criteria = None
	input_value = None
	if request.method == 'POST':
		# this is here to define criteria for use in sql after customer enters their criterias. this needs to be here above the 2nd post
		# in order for the if-else statement below to work.
		criteria = request.form.get('criteria')
		input_value = request.form.get('input_value')
	with cnx.cursor() as cur:
		if criteria == None and input_value == None:
			print("Noooo")
			query = "SELECT * FROM flight WHERE status = 'Upcoming'"
		else:
			print(criteria, input_value, "Hello!")
			query = "SELECT * FROM flight WHERE status = 'Upcoming' and flight.{} = '{}'".format(criteria,input_value)
		cur.execute(query)
		data = cur.fetchall()
		if request.method == 'POST' and request.form.get('flight_num'):
			print("Yayayaya")
			flight_num = request.form.get('flight_num')
			if permissions == 'Operator':
				#operator - airline staff. used to change status. they have a different submit button on the html.
				airline_name = request.form.get('airline_name')
				print(airline_name)
				print(flight_num)
				return render_template('change_status.html',flight_num=flight_num,airline_name=airline_name)
			#return redirect(url_for('customer_purchasetickets', flight= flight_num))
			return customer_purchasetickets(flight_num)
	return render_template('customer_searchforflights.html', data=data, loginType = loginType)

@app.route('/get_duration',methods = ['GET','POST'])
def get_duration():
	return render_template("get_duration.html")

@app.route('/tracker')
def tracker():
	user = session['customer']
	with cnx.cursor() as cur:
		x = labels
		last_year = date.today() + relativedelta(months=-12)
		query = "SELECT sum(flight.price) FROM ticket natural join purchases natural join flight WHERE purchases.customer_email = '{}' and purchases.purchase_date < '{}'".format(user,last_year)
		cur.execute(query)
		y = cur.fetchall()
		print(y)
		print(x)
		plt.bar(x, y)
		plt.title('Spending')
		plt.xlabel('Months')
		plt.ylabel('Amount')
		plt.show()


@app.route('/customer_trackmyspending')
def customer_trackmyspending():
	with cnx.cursor() as cur:
		last_year = date.today() + relativedelta(months=-12)
		query = "SELECT sum(flight.price) FROM ticket natural join purchases natural join flight WHERE purchases.customer_email = '{}' and purchases.purchase_date < '{}'".format(userPrimaryKey,last_year)
		cur.execute(query)
		data = cur.fetchall()
		total = data
		bardata = dict()
		default = 6
		the_date = date.today()
		if request.method == 'POST':
			default = int(request.form.get('duration'))
			the_date = request.form.get('starting_date')
			the_date = datetime.strptime(the_date, '%Y-%m-%d')
			print(the_date)
		for i in range(default):
			month_x_axis = (the_date + relativedelta(months=-i)).month
			year_x_axis = (the_date + relativedelta(months=-i)).year
			x_axis = str(month_x_axis) + "/" + str(year_x_axis)
			query2 = "SELECT sum(flight.price) as month_spend FROM ticket natural join purchases natural join flight WHERE purchases.customer_email = '{}' and MONTH(purchases.purchase_date) = '{}' and YEAR(purchases.purchase_date) = '{}'".format(userPrimaryKey, month_x_axis, year_x_axis)
			cur.execute(query2)
			month_data = cur.fetchall()
			bardata[x_axis] = month_data
		print(bardata)
	return render_template('customer_trackmyspending.html', data=data, bardata=bardata)


@app.route('/customer_viewmyflights')
def customer_viewmyflights():
	criteria = None
	input_value = None
	if request.method == 'POST':
		criteria = request.form.get('criteria')
		input_value = request.form.get('input_value')
		user = request.form.get('customer_email')
		print(user, "yay")
		print(criteria)
		print(input_value)
	if not request.form.get('customer_email'):
		user = session['customer']
	with cnx.cursor() as cur:
		if criteria == None and input_value == None:
			query = "SELECT distinct * FROM flight natural join ticket natural join purchases WHERE purchases.customer_email = '{}'".format(user)
		elif criteria:
			query = "SELECT distinct * FROM flight natural join ticket natural join purchases WHERE purchases.customer_email = '{}' and flight.{} = '{}'".format(
				user, criteria, input_value)
		cur.execute(query)
		data = cur.fetchall()
		print(type(data))
		print(data)
	return render_template('customer_viewmyflights.html', data=data)

#Creates route to home page for logged in booking agents, kicks to login page if not logged in
@app.route('/booking_agent_home')
def booking_agent_home():
	if "booking_agent" in session:
		email = session["booking_agent"]
		return render_template('booking_agent_home.html', name=email)
	else:
		return redirect(url_for("login"))

@app.route('/booking_agent_viewtopcustomers',methods = ['GET','POST'])
def booking_agent_viewtopcustomers():
	six_months_ago = date.today() + relativedelta(months=-6)
	one_year_ago = date.today() + relativedelta(months=-12)
	with cnx.cursor() as cur:
		query_ticketsbought = " select customer_email,count(*) from purchases natural join booking_agent where booking_agent.email = '{}' and purchases.purchase_date <= '{}' and purchases.purchase_date > '{}' group by customer_email order by count(*) desc limit 5;".format(userPrimaryKey, date.today(),six_months_ago)
		cur.execute(query_ticketsbought)
		ticket_data = cur.fetchall()
		query_commission = "select purchases.customer_email,sum(flight.price)*0.1 as commission from purchases natural join booking_agent natural join flight natural join ticket where booking_agent.email = '{}' and purchases.purchase_date > '{}' and purchases.purchase_date <= '{}' group by purchases.customer_email order by count(*) desc limit 5;".format(userPrimaryKey, one_year_ago, date.today())
		cur.execute(query_commission)
		commission_data = cur.fetchall()
		print(ticket_data)
		print(commission_data)
	return render_template('booking_agent_viewtopcustomers.html', ticket_data = ticket_data, commission_data = commission_data)

@app.route('/booking_agent_viewcommission',methods = ['GET','POST'])
def booking_agent_viewcommission():
	#assuming commission is 10% of ticket price.
	default = 6
	the_date = date.today()
	with cnx.cursor() as cur:
		if request.method == 'POST':
			default = int(request.form.get('duration'))
			the_date = request.form.get('starting_date')
			the_date = datetime.strptime(the_date, '%Y-%m-%d')
			start_date = the_date + relativedelta(months=-default)
			print(the_date)
			number_days = default * 30
			query_email = "select sum(flight.price)*0.1 as total_commission, sum(flight.price)/{} as average_commission,  count(*) as salecount from purchases natural join booking_agent natural join flight natural join ticket where booking_agent.email = '{}' and purchases.purchase_date > '{}' and purchases.purchase_date < '{}' group by booking_agent.email ".format(
				number_days,userPrimaryKey, start_date, the_date)
			cur.execute(query_email)
			data = cur.fetchall()
			print(data)
		else:
			query_email = "select sum(flight.price)*0.1 as total_commission, sum(flight.price)/300 as average_commission,  count(*) as salecount from purchases natural join booking_agent natural join flight natural join ticket where booking_agent.email = '{}' group by booking_agent.email".format(userPrimaryKey)
			cur.execute(query_email)
			data = cur.fetchall()
			print(data)
	return render_template('booking_agent_viewcommission.html', data=data)

@app.route('/booking_agent_viewmyflights')
def booking_agent_viewmyflights():
	global userPrimaryKey
	user = userPrimaryKey
	print(user)
	criteria = None
	input_value = None
	if request.method == 'POST':
		criteria = request.form.get('criteria')
		input_value = request.form.get('input_value')
	with cnx.cursor() as cur:
		if criteria == None and input_value == None:
			query = "SELECT * FROM flight natural join ticket natural join purchases natural join booking_agent WHERE booking_agent.email = '{}'".format(user)
		else:
			query = "SELECT * FROM flight natural join ticket natural join purchases natural join booking_agent WHERE booking_agent.email = '{}' and flight.{} = '{}'".format(
				user, criteria, input_value)
		cur.execute(query)
		data = cur.fetchall()
		print(type(data))
		print(data)
	return render_template('customer_viewmyflights.html', data=data, loginType=loginType)

@app.route('/booking_agent_purchasing',methods = ['GET','POST'])
def booking_agent_purchasing():
	if request.method == 'POST':
		if request.form.get('customer_email'):
			with cnx.cursor() as cur:
				email = request.form.get('customer_email')
				ticket_ID = request.form.get('ticket_ID')
				today = request.form.get('today')
				print(ticket_ID)
				check = "SELECT airline_name from ticket where ticket_ID = '{}'".format(ticket_ID)
				cur.execute(check)
				data = cur.fetchall()
				if data[0]["airline_name"] != airline:
					message = 'Not from the correct airline'
					return customer_ticketspurchased(message)
				else:
					user = userPrimaryKey
					check = "SELECT booking_agent_id from booking_agent where email = '{}'".format(user)
					cur.execute(check)
					data=cur.fetchall()
					id = data[0]["booking_agent_id"]
					query = '''INSERT INTO purchases VALUES ('{}','{}','{}','{}')'''.format(ticket_ID, email, id, today)
					cur.execute(query)
				cnx.commit()
				message = 'You have helped user with email {} buy the ticket! Your ticket number is {}'.format(email,
																									  ticket_ID)
			#custticketspurhcased is the default landing after success.
			return customer_ticketspurchased(message)
	#return render_template('booking_agent_purchasing.html')

#Creates route to home page for logged in airline staff, kicks to login page if not logged in
@app.route('/airline_staff_home')
def airline_staff_home():
	if "staff" in session:
		global airline
		username = session["staff"]
		with cnx.cursor() as cur:
			query = "SELECT airline_name from airline_staff where username = '{}'".format(username)
			cur.execute(query)
			data = cur.fetchone()
			airline = data

		with cnx.cursor() as cur:
			query = "SELECT permission_type from permission where username = '{}'".format(username)
			cur.execute(query)
			data = cur.fetchone()
			permissions = data
			print(permissions)
		return render_template('airline_staff_home.html', permissions=permissions, name=username)
	else:
		return redirect(url_for("login"))

@app.route('/create_flight', methods=['GET','POST'])
def create_flight():
	if 'staff' in session:
		with cnx.cursor() as cur:
			query = "SELECT permission_type FROM permission WHERE username = '{}'".format(session['staff'])
			cur.execute(query)
			permission = cur.fetchone()
			print(permission[0])
		if permission[0] == 'Operator' or permission[0] == 'Both':
			if request.method == 'POST':

				airline_name = request.form.get('airline_name')
				flight_num = request.form.get('flight_num')
				departure_airport = request.form.get('departure_airport')
				departure_time = request.form.get('departure_time')
				arrival_airport = request.form.get('arrival_airport')
				arrival_time = request.form.get('arrival_time')
				price = request.form.get('price')
				status = request.form.get('status')
				airplane_ID = request.form.get('airplane_number')

				query = "INSERT INTO flight VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status,airplane_ID)

				with cnx.cursor() as cur:
					cur.execute(query)

				cnx.commit()

				message = 'Successfully Created!'

				generate_seats(airline_name,flight_num,airplane_ID)

				return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)
			return render_template('create_flight.html')
		else:
			return redirect(url_for('airline_staff_home'))
	else:
		return redirect(url_for('login'))


def generate_seats(airline_name,flight_num,airplane_ID):
	query = "SELECT airplane.seats from airplane natural join flight where flight.airplane_ID = '{}' and flight.airline_name = '{}'".format(airplane_ID,airline_name)
	with cnx.cursor() as cur:
		cur.execute(query)
	cnx.commit()


	data = cur.fetchone()
	print(data[0])

	for i in range(data[0]):
		with cnx.cursor() as cur:
			query = "INSERT INTO ticket VALUES ('{}','{}','{}')".format(random.randint(10,999999),airline_name,flight_num)
			cur.execute(query)
			print('Added Ticket!')
		cnx.commit()




@app.route('/add_airplane', methods=['GET','POST'])
def add_airplane():

	if request.method == 'POST':

		airline_name = request.form.get('airline_name')
		airplane_ID = request.form.get('airplane_ID')
		seats = request.form.get('seats')

		query = "INSERT INTO airplane VALUES ('{}','{}','{}')".format(airline_name,airplane_ID,seats)
		with cnx.cursor() as cur:
			cur.execute(query)

		cnx.commit()

		message = 'Successfully Created!'

		return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)
	return render_template('add_airplane.html')


@app.route('/add_airport', methods=['GET','POST'])
def add_airport():

	if request.method == 'POST':

		airport_name = request.form.get('airport_name')
		airport_city = request.form.get('airport_city')

		query = "INSERT INTO airport VALUES ('{}','{}')".format(airport_name,airport_city)

		with cnx.cursor() as cur:
			cur.execute(query)

		cnx.commit()

		message = 'Successfully Created!'

		return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)
	return render_template('add_airport.html')

@app.route('/change_status', methods=['GET','POST'])
def change_status():
	if 'staff' in session:
		with cnx.cursor() as cur:
			query = "SELECT permission_type FROM permission WHERE username = '{}'".format(session['staff'])
			cur.execute(query)
			permission = cur.fetchone()
			print(permission[0])
		if permission[0] == 'Operator' or permission[0] == 'Both':
			if request.method == 'POST':

				airline_name = request.form.get('airline_name')
				flight_number = request.form.get('flight_num')
				new_status = request.form.get('new_status')

				print(airline_name)
				print(flight_number)

				query = "UPDATE flight SET status = '{}' WHERE airline_name = '{}' and flight_num = '{}'".format(new_status,airline_name,flight_number)

				with cnx.cursor() as cur:
					cur.execute(query)

				cnx.commit()

				message = 'Successfully Updated!'

				return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)

			return render_template('change_status.html')
		else:
			return redirect(url_for('airline_staff_home'))
	else:
		return redirect(url_for('login'))

@app.route('/staff_view_flights', methods=['GET','POST'])
def staff_view_flights():
	criteria = None
	input_value = None
	print(airline)
	if request.method == 'POST':
		criteria = request.form.get('criteria')
		input_value = request.form.get('input_value')
	with cnx.cursor() as cur:
		if criteria == None and input_value == None:
			query = "SELECT * FROM flight WHERE airline_name = '{}'".format(airline[0])
		else:
			query = "SELECT * FROM flight WHERE airline_name = '{}' and flight.{} = '{}'".format(
				airline, criteria, input_value)
		cur.execute(query)
		data = cur.fetchall()
		print(data)
	return render_template('customer_viewmyflights.html', data=data, permission=permissions)


@app.route('/view_agents', methods=['GET','POST'])
def view_agents():
	if 'staff' in session:
		#query1 = "SELECT airline_name 
		one_year_ago = date.today() + relativedelta(months=-12)
		if request.method == "POST":
			duration = int(request.form.get('duration'))
			modified_date = date.today() + relativedelta(months=-duration)
			sort_query = "select purchases.booking_agent_id, sum(flight.price) as sales from ticket natural join flight natural join purchases where flight.airline_name = '{}' and purchases.booking_agent_id is not null and purchases.purchase_date > '{}' group by purchases.booking_agent_id order by sales desc limit 5;".format(airline[0],modified_date)
			with cnx.cursor() as cur:
				cur.execute(sort_query)
				data = cur.fetchall()
				return render_template('view_agents.html', data=data, permission=permissions)
		with cnx.cursor() as cur:
			query = "select purchases.booking_agent_id, sum(flight.price) as sales from ticket natural join flight natural join purchases where flight.airline_name = '{}' and purchases.booking_agent_id is not null and purchases.purchase_date > '{}' group by purchases.booking_agent_id order by sales desc limit 5;".format(airline[0],one_year_ago)
			cur.execute(query)
			data = cur.fetchall()
		return render_template('view_agents.html', data=data, permission=permissions)
	else:
		return redirect(url_for('login'))


@app.route('/view_customers', methods=['GET','POST'])
def view_customers():
	if 'staff' in session:
		with cnx.cursor() as cur:
			query = "select purchases.customer_email, count(*)  from purchases natural join ticket where ticket.airline_name = '{}'  group by purchases.customer_email order by count(*) desc;".format(airline)
			print(airline)
			cur.execute(query)
			data = cur.fetchall()
			print(data)
		return render_template('view_customers.html', data=data, permission=permissions, airline=airline)
	else:
		return redirect(url_for('login'))


@app.route('/view_reports', methods=['GET','POST'])
def view_reports():
	if 'staff' in session:
		with cnx.cursor() as cur:
			default=12
			the_date = date.today()
			bardata = dict()
			if request.method == 'POST':
				print('posting')
				default = int(request.form.get('duration'))
				the_date = request.form.get('starting_date')
				the_date = datetime.strptime(the_date, '%Y-%m-%d')
				start_date = the_date + relativedelta(months=-default)
				print(the_date)
				query_email = "select count(*) as number_sold from purchases natural join flight natural join ticket where flight.airline_name = '{}' and purchases.purchase_date > '{}' and purchases.purchase_date <= '{}'".format(
					airline, start_date, the_date)
				cur.execute(query_email)
				data = cur.fetchall()
				print(data)
			else:
				query_email = "select count(*) as number_sold from purchases natural join flight natural join ticket where flight.airline_name = '{}'".format(
					airline)
				cur.execute(query_email)
				data = cur.fetchall()
				print(data)
			for i in range(default):
				month_x_axis = (the_date + relativedelta(months=-i)).month
				year_x_axis = (the_date + relativedelta(months=-i)).year
				x_axis = str(month_x_axis) + "/" + str(year_x_axis)
				query2 = "SELECT count(*) as number_sold FROM ticket natural join purchases natural join flight WHERE flight.airline_name = '{}' and MONTH(purchases.purchase_date) = '{}' and YEAR(purchases.purchase_date) = '{}'".format(airline, month_x_axis, year_x_axis)
				cur.execute(query2)
				month_data = cur.fetchall()
				bardata[x_axis] = month_data
			print(bardata)
		return render_template('view_reports.html', data=data, permission=permissions, bardata=bardata)
	else:
		return redirect(url_for('login'))

@app.route('/compare_revenue_earned', methods=['GET','POST'])
def compare_revenue_earned():
	if "staff" in session:
		with cnx.cursor() as cur:
			default=12
			the_date = date.today() + relativedelta(months=-default)
			if request.method == 'POST':
				print('posting')
				default = int(request.form.get('duration'))
				the_date = date.today() + relativedelta(months=-default)
			query_customer = "SELECT sum(flight.price) as sales FROM ticket natural join flight natural join purchases WHERE ticket.airline_name = '{}' and purchases.booking_agent_id is null and purchases.purchase_date > '{}'".format(
				airline, the_date)
			query_agent = "SELECT sum(flight.price) as sales FROM ticket natural join purchases natural join flight WHERE ticket.airline_name = '{}' and purchases.booking_agent_id is not null and purchases.purchase_date > '{}'".format(
				airline, the_date)
			cur.execute(query_customer)
			data_customer = cur.fetchone()
			print(data_customer)
			cur.execute(query_agent)
			data_agent = cur.fetchone()
			print(data_agent)
		return render_template('compare_revenue_earned.html', data_agent = data_agent, data_customer = data_customer)
	else:
		return redirect(url_for('login'))

@app.route('/view_destinations', methods=['GET','POST'])
def view_destinations():
	if 'staff' in session:
		with cnx.cursor() as cur:
			query = "select count(*) as dest_count, flight.arrival_airport as dest from flight where flight.airline_name = '{}' group by flight.arrival_airport order by dest_count desc".format(airline)
			cur.execute(query)
			data = cur.fetchall()
			print(data)

		return render_template('view_destinations.html', data=data, permission=permissions)
	else:
		return redirect(url_for('login'))


@app.route('/grant_new_permissions', methods=['GET','POST'])
def grant_new_permissions():
	if 'staff' in session:
		with cnx.cursor() as cur:
			query = "SELECT permission_type FROM permission WHERE username = '{}'".format(session['staff'])
			cur.execute(query)
			permission = cur.fetchone()
			print(permission[0])
		if permission[0] == 'Admin' or permission[0] == 'Both':
			if request.method == 'POST':

				new_status = request.form.get('new_status')
				username = request.form.get('username')

				print(new_status)
				print(username)
				query = "UPDATE permission SET permission_type = '{}' WHERE username = '{}'".format(new_status, username)
				with cnx.cursor() as cur:
					cur.execute(query)

				cnx.commit()

				message = 'Permission Changed!'

				return render_template('customer_ticketspurchased.html', message=message, loginType=loginType)


			with cnx.cursor() as cur:
				query = "SELECT * FROM airline_staff left join permission on airline_staff.username = permission.username"
				print(airline)
				cur.execute(query)
				data = cur.fetchall()
				print(data)

			return render_template('grant_new_permissions.html', data=data, permission=permissions)
		else:
			return redirect(url_for('airline_staff_home'))
	else:
		return redirect(url_for('login'))


@app.route('/add_agents', methods=['GET','POST'])
def add_agents():
	if 'staff' in session:
		with cnx.cursor() as cur:
			query = "SELECT permission_type FROM permission WHERE username = '{}'".format(session['staff'])
			cur.execute(query)
			permission = cur.fetchone()
			print(permission[0])
		if permission[0] == 'Admin' or permission[0] == 'Both':

			with cnx.cursor() as cur:
				query = "SELECT booking_agent.* FROM booking_agent left join booking_agent_work_for on booking_agent.email = booking_agent_work_for.email where booking_agent_work_for.airline_name is null"
				cur.execute(query)
				data = cur.fetchall()
				print(data)

			if request.method == 'POST':

				with cnx.cursor() as cur:

					
					email = request.form.get('email')
					print(email)

					query2 = "SELECT airline_name FROM airline_staff WHERE username = '{}'".format(session['staff'])
					cur.execute(query2)
					airline = cur.fetchone()
					print(airline)

					query = "INSERT INTO booking_agent_work_for values ('{}','{}')".format(email,airline[0])
					cur.execute(query)
				cnx.commit()

			return render_template('view_agents.html', data=data, redir=add_agents)
		else:
			return redirect(url_for('airline_staff_home'))
	else:
		return redirect(url_for('login'))



if __name__ == '__main__':
    app.run()

'''
@app.errorhandler(404):
def page_not_found(e):
	return render_template("404.html")
'''