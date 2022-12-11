# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 19:16:21 2022

@author: sam
"""



from geopy import Nominatim
import random
import requests

class ESDChecker():
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.gl = Nominatim(user_agent="MonkeBot")
        
    def check(self, query=None):
        if query:
            city = query
        else:
            city = self.getCity()
        return self.getESDRisk(city)
    
        
        
    def getESDRisk(self, query):
        location = self.gl.geocode(query)
        url = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&appid={}".format(location.latitude,location.longitude,self.API_KEY)
        response = requests.get(url)
        hum = response.json()["main"]["humidity"]
        if hum >= 30:
            return "The humidity is {}%. The ESD risk is low. Go ahead and rub your feet on the carpet.".format(hum)
        else:
            return "The humidity is {}%. The ESD risk is high. Use ESD precautions!".format(hum)
        
        
    def getCity(self):
            f = open("cities.txt","r")
            cities = f.read().splitlines()
            return random.choice(cities)

