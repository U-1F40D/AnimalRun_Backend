# import main Flask class and request object
from flask import Flask, request
from load_sample_response import get_data

# temp
response = ''
# create the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello"


@app.route('/classify-animal', methods=['GET', 'POST'])
def classify_animal():

    global response

    if request.method == 'POST':
        request_data = request.data
    # send request data to model
    
    # get response
    response = get_data()
        
    # send response back to app
    return response

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
