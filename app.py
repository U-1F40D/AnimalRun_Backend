# import main Flask class and request object
from flask import Flask, request

response = ''

# create the Flask app
app = Flask(__name__)


@app.route('/classify-animal', methods=['GET', 'POST'])
def classify_animal():

    global response

    if request.method == 'POST':
        request_data = request.data
    # encoded Base64
    
    # decode data
    base64 = '''Decoded Base64 Object'''


    return 'Output from model'

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
