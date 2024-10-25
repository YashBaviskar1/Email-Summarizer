from flask import Flask, jsonify 
from flask_cors import CORS
from fetching import data
app = Flask(__name__)
CORS(app)
@app.route('/api/send', methods = ['GET'])
def index() :
    return jsonify({"message" : "Hello World"})

@app.route('/fetched')
def fetched() :
    email = "yashbav24@gmail.com"
    return jsonify({"email" : f"{email}"})


@app.route('/fetch_latest_email')
def fetch_latest_email():
    return jsonify(data)