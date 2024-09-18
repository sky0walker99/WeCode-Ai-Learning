from flask import Flask ,request , jsonify

# Creating web application instance
app = Flask(__name__)


@app.route('/')
def custom():
    return "<h2>  THIs is testing  <h2>"

@app.route('api/get_user_input',methods = ['GET'])
def get_user_input():
    data = request.get_json()
    
    return jsonify(data), 201 
    
# Start the server
if __name__ == '__main__':
    app.run(debug=True)