from flask import Flask ,request , jsonify

# Creating web application instance
app = Flask(__name__)


@app.route('/')
def custom():
    return "<h2>  THIs is testing  <h2>"


# The endpoint should be set up to handle POST requests since the user's input will be sent as a JSON payload
@app.route('/api/get_user_input', methods = ['POST'])        
def get_user_input():
    data = request.get_json()                  # Extract JSON data from the request
    user_input = data.get('user_input', '')    # Get the user input from the JSON data
                                              
    response_data = {                          # Process the input, to pass it to an AI model.
        'received_input':user_input , 'status':'success'  } 
    return jsonify(response_data), 200


@app.route('/api/submit_input', methods =['PSOT'])   # The route for giving the input from user to ai models.
def submit_input_to_ai():
    data = request.get_json()
    user_input = data.get('user_input', '') 
    ai_result = f"ai: {user_input}"
    response_data = {
        'received_input': user_input,
        'ai_result': ai_result,
        'status': 'success'
    }
    return jsonify(response_data), 200

# Start the server
if __name__ == '__main__':
    app.run(debug=True)