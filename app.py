from flask import Flask, session, redirect, url_for, escape, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.automap import automap_base
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
meta = MetaData()

Base = automap_base()
Base.prepare(db.engine, reflect=True)
User = Base.classes.users
Remark = Base.classes.remark
Mark = Base.classes.marks
Feedback = Base.classes.feedbacks



############################################# LOGIN #############################################



@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	# If there's an attempt to login, then verify login info is correct
	if request.method=='POST':
		sql = """
			SELECT *
			FROM users
			"""
		results = db.engine.execute(text(sql))
		for result in results:
			#If login information is correct
			if result['username']==request.form['username']:
				if result['password']==request.form['password']:
					# Logging in with session
					session['username']=request.form['username']
					sql1 = """
						SELECT *
						FROM marks
						where studentname='{}'""".format(request.form['username'])
					results = db.engine.execute(text(sql1))
					return redirect(url_for('home'))

		# Else user told to try again and reload page
		flash('Username or password is wrong. Please try again')
		return render_template('login.html')

	# If user is already logged in, go to Home Page
	elif 'username' in session:
			return redirect(url_for('home'))

	# If user is not logged in, go to Login Page
	else:
		return render_template('login.html')

#################################### HOME PAGE ####################################
# Home page with greetings and general course description
@app.route('/home', methods=['GET','POST'])
def home():
	if 'username' in session:
		sql1 = """
			SELECT username
			FROM users
			where username='{}'""".format(session['username'])
		results = db.engine.execute(text(sql1))
		return render_template('index.html',data=session['username'])
	
	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))

#################################### GRADES ####################################
# Grades
@app.route('/grades',methods=['GET','POST'])
def grades():
	if 'username' in session:
		# If remark requests are made by students
		if request.method=='POST':
			students=session['username']

			# Gathering date and time when remark request is made
			date = datetime.now()
			now = datetime.now()
			time = now.strftime("%H:%M:%S")

			# Adding request to database
			new_remark = Remark(student=session['username'], instructor=request.form['instructor'], assignment=request.form['assignment'], comments=request.form['comments'], date=date, time=time)
			db.session.add(new_remark)
			db.session.commit()
			
			# Reload the page
			return redirect(url_for('grades'))
		
		# Display grades
		else:	
			sql1 = """
				SELECT *
				FROM users LEFT JOIN marks on marks.studentname = users.username
				WHERE username='{}'""".format(session['username'])
			results = db.engine.execute(text(sql1))
			sql2 = """
				SELECT *
				FROM users LEFT JOIN marks on marks.studentname = users.username
				"""
			results2 = db.engine.execute(text(sql2))
			sql3 = """
				SELECT *
				FROM remark 
				ORDER BY date , time 
				"""
			results3 = db.engine.execute(text(sql3))
			return render_template('grades.html',data=results, data2=results2, data3=results3)
	
	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))


# Edit Marks
@app.route('/editmark',methods=['GET', 'POST'])
def editMark():
	if request.method=='POST':
		updateSQL="""UPDATE marks
				SET {} = '{}' 
				WHERE studentname = '{}'""".format(request.form['assignment'], request.form['mark'], request.form['username']);
		db.engine.execute(text(updateSQL))
		return redirect(url_for('grades'))


#################################### OTHER PAGS ####################################
# Calendar page
@app.route('/calendar')
def calendar():
	if 'username' in session:
		return render_template('calendar.html')

	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))

# Page displays instructor's announcements
@app.route('/news')
def news():
	if 'username' in session:
		return render_template('news.html')

	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))

# Page with link to discussion board
@app.route('/discussion_board')
def discussion_board():
	if 'username' in session:
		return render_template('discussion_board.html')
		
	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))

# Page with all lecture materials
@app.route('/lectures')
def lectures():
	if 'username' in session:
		return render_template('lectures.html')
		
	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))

# Page with all lab materials
@app.route('/labs')
def labs():
	if 'username' in session:
		return render_template('labs.html')
		
	# If user is not signed in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))

# Page with all assignment materials
@app.route('/assignments')
def assignments():
	if 'username' in session:
		return render_template('assignments.html')
		
	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))

# Page will all test materials and old tests/exams/midterms
@app.route('/tests')
def tests():
	if 'username' in session:
		return render_template('tests.html')
		
	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))

# Page with all additional class resources
@app.route('/resources')
def resources():
	if 'username' in session:
		return render_template('resources.html')
		
	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))


#################################### FEEDBACK ####################################
# Feedback page
@app.route('/feedback', methods=['GET','POST'])
def feedback():
	if 'username' in session:
		# If student gives a feedback
		if request.method=='POST':
			instructor = request.form['instructor']
			subject = request.form['subject']
			feedback = request.form['feedback']
			date = datetime.now()
			now = datetime.now()
			time = now.strftime("%H:%M:%S")

			# Inserting feedback to the database
			new_feedback = Feedback(instructor=instructor, subject=subject, feedback=feedback, date=date, time=time)
			db.session.add(new_feedback)
			db.session.commit()
			
			# Reload the Page
			return redirect(url_for('feedback'))
		
		else:	
			sql1 = """
				SELECT *
				FROM users LEFT JOIN marks on marks.studentname = users.username
				WHERE username='{}'""".format(session['username'])
			results = db.engine.execute(text(sql1))
			sql2 = """
				SELECT instructor, feedback, date, time, position, subject
				FROM feedbacks LEFT JOIN users on feedbacks.instructor = users.username
				ORDER BY date DESC, time DESC
				"""
			results2 = db.engine.execute(text(sql2))
			return render_template('feedback.html',data=results, data2=results2)
		
	# If user is not logged in
	flash('You are currently not signed in. To access this page please login and try again.')
	return redirect(url_for('login'))
		

############################################# LOGOUT #############################################
# If user logs out, it wil be redirected to the login page
@app.route('/logout')
def logout():
	session.pop('username', None)
	flash('You have been logged out')
	return redirect(url_for('login'))

############################################# REGISTER #############################################
# Registering a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method=='POST':
		# Make sure username or password is not empty
		if request.form['username'] == "": #if username already in database
			flash('Please enter a username')
			return render_template('register.html')
		if request.form['password'] == "": #if username already in database
			flash('Please enter a password')
			return render_template('register.html')
		# Make sure username does not already exist
		sql = """
			SELECT *
			FROM users
			"""
		results = db.engine.execute(text(sql))
		for result in results:
			if result['username']==request.form['username']: #if username already in database
				flash('Username already exists. Please try a different username')
				return render_template('register.html')
		
		# create new user account 
		new_user = User(username=request.form['username'], password=request.form['password'], position=request.form['position'])
		db.session.add(new_user)
		db.session.commit()

		# create new grade account
		new_grade = Mark(studentname=request.form['username'])
		db.session.add(new_grade)
		db.session.commit()
		
		# User needs to login after registering to view class content
		flash('Your account is created. Please login to view the course contents.')
		return redirect(url_for('login'))

	else:
		return render_template('register.html')

if __name__=="__main__":
	app.run(debug=True,host='0.0.0.0')

