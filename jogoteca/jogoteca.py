from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = MongoClient('localhost', 27017).jogoteca

from views import *

if __name__ == '__main__':
    app.run(debug=True)
