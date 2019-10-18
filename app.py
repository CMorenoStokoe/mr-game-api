#This file initialises the FLask app and sets resource locations (URLs)

#Import
from flask import Flask #Flask app 
from flask_restful import Api #Flask REST API
from flask_cors import CORS #For local testing

#Importing resources called by requests or startup
from resources.simulation import *
from resources.init import *
from startup.init import Start_Values

#Initialise app
app = Flask(__name__) #Flask APP
api = Api(app) #Flask REST API
CORS(app) #CORS for local testing

#Initialise data
Start_Values()

#Resource locations
api.add_resource(View_Data, '/simulation')
api.add_resource(Intervene, '/intervene')
api.add_resource(Reset, '/reset')
api.add_resource(Init_Buttons, '/init_buttons')


#Only runs if current file is main (prevents feedback loops?)
if __name__ == '__main__':
	app.run(port=5000, debug=True)