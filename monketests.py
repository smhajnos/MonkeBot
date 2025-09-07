# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 23:43:14 2022

@author: sam
"""
import datetime
#import esd
import monkebotsecrets
#from geopy import Nominatim
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
            
            
            
#def esdtest1():
#    location = Nominatim(user_agent="MonkeBot").geocode("York, PA")
#    url = "http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&limit=1&appid={}".format(location.latitude,location.longitude,monkebotsecrets.OWM_KEY)
    
#def esdtest2():
#    location = Nominatim(user_agent="MonkeBot").geocode("York, PA")
#    url = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&appid={}".format(location.latitude,location.longitude,monkebotsecrets.OWM_KEY)
#    response = requests.get(url)
#    print(response)
    
#def esdtest3():
#    esdchecker = esd.ESDChecker(monkebotsecrets.OWM_KEY)
#    print(esdchecker.getESDRisk("York, PA"))
    
    
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
    
    
def walktests():
    import os
    f = []
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd() + "/savedata"):
        f.extend(filenames)
    print(f)
    
    
    
    
def ballstest():
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    import uuid
    import urllib.request
    import os
    from io import BytesIO
    
    """
    out = Image.new("RGB", (150, 100), (255, 255, 255))
    d = ImageDraw.Draw(out)
    fnt = ImageFont.truetype('arial.ttf',15)
    d.multiline_text((10, 10), "Hello\nWorld", font=fnt, fill=(0, 0, 0))
    """
    txt = "Did you ever hear the tragedy of Darth Plagueis the wise? I thought not. It's not a story the Jedi would tell you."
    fnt = ImageFont.truetype('arial.ttf',15)
    def generate_image(text_rows):
        width = 500
        height = 657+25*text_rows+15
        composite = Image.new('RGBA', (width, height))
        y = 0
        timage = Image.open("img/balls/top.png")
        composite.paste(timage,(0,y))
        y += timage.height
        for x in range(0,text_rows):
            timage = Image.open("img/balls/middle.png")
            composite.paste(timage,(0,y))
            y += timage.height
        timage = Image.open("img/balls/bottom.png")
        composite.paste(timage,(0,y))
        y += timage.height
        return composite
    
    def calculate_lines(text):
        def get_text_width(text_in):
            text_to_calc = " ".join(text_in)
            print("Getting text width of {}".format(text_to_calc))
            img = Image.new('RGBA', (500, 25))
            draw = ImageDraw.Draw(img)

            bbox = draw.textbbox((0,0),text_to_calc,fnt)
            print(bbox[2] - bbox[0])
            return bbox[2] - bbox[0]
        total_text = text.split()
        finished_text = []
        remaining_text = total_text
        while len(remaining_text) > 0:
            i = 1 # How words we are trying to fit on this line
            cont = True
            while i < len(remaining_text) and cont:
                this_line = remaining_text[0:i]
                w = get_text_width(this_line)
                if w < 475: # Add 1 to i and 
                    i += 1
                else: # the previous i was the one we want
                    i -= 1
                    cont = False
            if i == 0:
                this_line = remaining_text[0]
                # TODO: clip it at the right number of characters and continue on next line
            else:   
                this_line = remaining_text[0:i]
            finished_text.append(this_line)
            remaining_text = remaining_text[i:]
            print(finished_text)
            print(remaining_text)
        return finished_text
                    
    lines = calculate_lines(txt)       
            
    img = generate_image(len(lines))
    
    i = 0
    for line in lines:
        line_text = " ".join(line)
        imgdraw = ImageDraw.Draw(img)
        imgdraw.text((10,i*25+10), line_text ,font=fnt, fill = (0,0,0))
    
        i += 1
    
    img.save("tmp/balls.png")
    
    
    
    
    