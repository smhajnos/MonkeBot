# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 23:43:14 2022

@author: sam
"""
import datetime
import esd
import monkebotsecrets
from geopy import Nominatim
import requests
import sqlite3


dataWarehouse = sqlite3.connect("datawarehouse.db")
cursor = dataWarehouse.cursor()
def commit():
    dataWarehouse.commit()
    
    
def pisstest1():
    pissday = datetime.date(2022,7,20)
    today = datetime.date.today()
    delta = today - pissday
    pissdays = delta.days
    print(pissdays)
    with open("lastpisscheck.txt","r") as pissfile:
        try:
            lastpissdays = int(pissfile.read())
        except:
            lastpissdays = 0
    if lastpissdays < pissdays:
        print("Days since last piss: {}".format(pissdays))
        with open("lastpisscheck.txt","w") as pissfile:
            pissfile.write(str(pissdays))
            
            
            
def esdtest1():
    location = Nominatim(user_agent="MonkeBot").geocode("York, PA")
    url = "http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&limit=1&appid={}".format(location.latitude,location.longitude,monkebotsecrets.OWM_KEY)
    
def esdtest2():
    location = Nominatim(user_agent="MonkeBot").geocode("York, PA")
    url = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&appid={}".format(location.latitude,location.longitude,monkebotsecrets.OWM_KEY)
    response = requests.get(url)
    print(response)
    
def esdtest3():
    esdchecker = esd.ESDChecker(monkebotsecrets.OWM_KEY)
    print(esdchecker.getESDRisk("York, PA"))
    
    
def getconfig(param):
    cursor.execute("SELECT val FROM config WHERE param = ?",(param,))
    res = cursor.fetchone()
    return res[0]

def setconfig(param, val):
    cursor.execute("SELECT COUNT(*) FROM config WHERE param = ?",(param,))
    res = cursor.fetchone()
    if res[0] > 0:
            cursor.execute("DELETE FROM config WHERE param = ?",(param,))
    cursor.execute("INSERT INTO config (param, val) VALUES (?,?)",(param,val,))
    commit()