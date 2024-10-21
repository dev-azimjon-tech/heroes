from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm  #type: ignore
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length #type:ignore
import random
import string
from secret import *

app = Flask(__name__)
app.secret_key = secret_key # Replace with a strong secret key


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/heroes")
def heroes():
    return render_template("heroes.html")
# In-memory "database" for demonstration purposes
users = {}

# Generate a random email
def generate_random_email(name):
    domain = "example.com"
    random_number = ''.join(random.choices(string.digits, k=5))
    return f"{name.lower()}.{random_number}@{domain}"

# Registration Form
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        surname = form.surname.data
        password = form.password.data
        email = generate_random_email(first_name)

        # Store user info in the "database"
        users[email] = {
            'first_name': first_name,
            'surname': surname,
            'password': password
        }

        flash(f'Registration successful! Your generated email is {email}', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Authenticate the user
        if email in users and users[email]['password'] == password:
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        email = session['user']
        user = users[email]
        return render_template('dashboard.html', user=user)
    else:
        flash('You need to login first!', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
