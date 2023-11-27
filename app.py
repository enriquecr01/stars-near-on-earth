from flask import Flask
from flask_cors import CORS
import time
from web_scraping import printPage

app = Flask(__name__)

CORS(app, origins=['http://localhost:3000', 'https://enriquechavezr.com/*'])

@app.route('/')
def index():
    return 'Hello World'

@app.route('/<name>')
def print_name(name):
    return 'Welcome, {}'.format(name)

@app.route('/getStars')
def getStars():
    start = time.time()
    print("Started Timer")
    text = printPage()
    end = time.time()
    print(end - start)
    return text

if __name__ == '__main__':
    app.run(debug=True)