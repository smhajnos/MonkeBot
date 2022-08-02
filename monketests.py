# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 23:43:14 2022

@author: sam
"""
import datetime

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