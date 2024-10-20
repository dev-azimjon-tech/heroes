from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/library')
def library():
    return "Library Page"

@app.route('/create_planet')
def create_planet():
    return "Create Planet Page"

@app.route('/register')
def register():
    return "Register Page"

@app.route('/heroes')
def heroes():
    return "Heroes Page"

if __name__ == '__main__':
    app.run(debug=True)
