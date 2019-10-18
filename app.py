#This file initialises the FLask app and sets resource locations (URLs)

#Import
from flask import Flask #Flask app 
from flask_restful import Api #Flask REST API
from flask_cors import CORS #For local testing

from resources.simulation import * #App simulation model for setting resource URL
from startup.init_values import Start_Values


#Initialise app
app = Flask(__name__) #Flask APP
api = Api(app) #Flask REST API
CORS(app) #CORS for local testing

#Initialise data
Start_Values()

#Resource locations
api.add_resource(View_Data, '/simulation')
api.add_resource(Intervene, '/intervene')

#Only runs if current file is main (prevents feedback loops?)
if __name__ == '__main__':
	app.run(port=5000, debug=True)