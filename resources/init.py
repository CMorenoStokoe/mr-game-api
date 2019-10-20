#Import
from flask_restful import Resource #REST API resources 
import json # Handling json objects
from flask_restful import reqparse

from models.simulation import *
from startup.init import Start_Buttons

class Init_Buttons (Resource):
     def get(self):
        return(Start_Buttons())
    