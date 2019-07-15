from flask import Flask, render_template, request, redirect, url_for, session
from news_api import getheadlines
#session is a special kind of dictionary that is accessible anywhere in the program
#even in the jinja without passing it explicitly
from model import save_user, user_exists, product_exists, add_product

app = Flask(__name__)
app.secret_key = 'hello'


@app.route('/')
def home():
	headlines = getheadlines()
	
	if(headlines != None):
		return render_template('home.html', title = "Home", headlines = headlines, totalheadlines = len(headlines))
	return render_template('home.html', title = "Home", headlines = ["Cannot retrieve the news, Internet Not Connected"], totalheadlines = 1)

@app.route('/about')
def about():
	return render_template('about.html', title = "About")

@app.route('/contact')
def contact():
	return render_template('contact.html', title = "Contact")

@app.route('/login', methods=['GET', 'POST'])
def login():
	
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		result = user_exists(username)

		if result:
				if result['password'] != password:
					return render_template('access_denied.html', error_msg = "Password doesn't match. Go back and re-renter the password")

				session['username'] = username
				session['c_type'] = result['c_type']
				return redirect(url_for('home'))
		return render_template('access_denied.html', error_msg = "Username doesn't exist")
	return redirect(url_for('home'))


@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		user_info = {}
		user_info['username'] = request.form['username']
		
		user_info['password'] = request.form['password1']
		password2 = request.form['password2']
		user_info['c_type'] = request.form['type']

		if user_info['c_type'] == 'buyer':
			user_info['cart'] = []

		if user_exists(user_info['username']):
			return "Username already exist"

		if user_info['password'] != password2:
			return "Passwords doesn't match"

		save_user(user_info)

	return redirect(url_for('home'))


@app.route('/products', methods=['GET', 'POST'])
def products():
	if request.method == 'POST':
		product_info = {}
		product_info['name'] = request.form['name']
		product_info['price'] = int(request.form['price'])
		product_info['description'] = request.form['description']
		product_info['seller'] = session['username']

		if product_exists(product_info['name']):
			return "Product exists"

		add_product(product_info)
		return "Product added! Check your db"
	return (redirect(url_for('home')))
app.run(debug = True, port = 9999)