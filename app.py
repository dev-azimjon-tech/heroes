from flask import Flask, render_template

import os
import secrets
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/heroes')
def heroes():
    return render_template("heroes.html")



# Initialize Flask app


# Generate or set secret key
# Option 1: Use os.urandom or secrets.token_hex
# app.secret_key = secrets.token_hex(32)  # Uncomment for development

# Option 2: Use environment variable (best practice)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# In-memory users database (for demonstration purposes only)
users_db = {}

# Flask-WTF Form Class
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

def email_exists(email):
    return email in users_db

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Check if the email is already registered
        if email_exists(email):
            flash('Email is already registered, please log in or use a different email.', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Save the user (in-memory for now)
        users_db[email] = {'name': name, 'password': hashed_password}

        # Flash a success message and redirect to the register page (or login page)
        flash('You have successfully registered!', 'success')
        return redirect(url_for('register'))  # Change this to a login page URL in a real app

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
