from flask import Flask


# Creating web application instance
app = Flask(__name__)

@app.route('/')
def custom():
    return "<h2>  THIs is testing  <h2>"

@app.route('/api/user_input')
