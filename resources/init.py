#Import
from flask_restful import Resource #REST API resources 
import json # Handling json objects
from flask_restful import reqparse

from models.simulation import *
from startup.init import Start_Buttons
from models.simulation import Overall_Stats

class Init_Buttons (Resource):
     def get(self):
        btnInfo = Start_Buttons();
        statsInfo = Overall_Stats("Subjective well being",100)
        return({"btnInfo":btnInfo, "statsInfo":statsInfo})
    