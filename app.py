from flask import Flask
import time
from web_scraping import printPage

app = Flask(__name__)

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