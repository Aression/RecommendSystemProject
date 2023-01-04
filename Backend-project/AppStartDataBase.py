from flask import Flask
from flask_cors import CORS
import pymongo

App = Flask(__name__)
CORS(App, resources={r'/*': {'origins': '*', 'supports_credentials': True, 'Access-Control-Allow-Origin': '*'}})

Client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
DB = Client["PCD"]
CUser = DB["User"]
CMovie = DB["Movie"]
CCustomUser = DB["CustomUser"]
CMovieTag = DB["MovieTag"]
