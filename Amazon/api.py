from flask import Flask, render_template, request, redirect, url_for, session
#session is a special kind of dictionary that is accessible anywhere in the program
#even in the jinja without passing it explicitly

app = Flask(__name__)
app.secret_key = 'hello'

@app.route('/')
def home():
	return render_template('home.html', title = "Home")

@app.route('/about')
def about():
	return render_template('about.html', title = "About")

@app.route('/contact')
def contact():
	return render_template('contact.html', title = "Contact")

@app.route('/login', methods=['GET', 'POST'])
def login():
	
	if request.method == 'POST':
		users = {
			'user1': '123',
			'user2': '234', 
			'user3': '456'
		}

		username = request.form['username']
		password = request.form['password']

		if username not in users:
			return "User does not exist. Go back and enter a valid username"

		if users[username] != password:
			return "Password does not match. Go back and enter the password"

		session['username'] = username
		return redirect(url_for('home'))
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))
app.run(debug = True)