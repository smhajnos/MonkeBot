# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 18:03:41 2022

@author: sam
"""


import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
import monkebotsecrets
import datetime

monke_server = 983896046700736522
logs_channel = 1000524219517505656
nb_color = 0xc16950
piss_channel = 983896047514439682 #general
#piss_channel = logs_channel

intents = nextcord.Intents.all()
#intents.members = True


bot = commands.Bot(command_prefix='}', intents=intents)


@bot.slash_command(name="ping",description="Check if the bot is working", guild_ids=[monke_server])
async def ping(ctx):
    await ctx.send("Pong!")

async def log(s):
    lc = bot.get_channel(logs_channel)
    await lc.send(s)
    
    
    
@tasks.loop(seconds=3600)
async def pisscheck():
    pissday = datetime.date(2022,7,20)
    today = datetime.date.today()
    delta = today - pissday
    pissdays = delta.days
    print("Days since last piss: {}".format(pissdays))
    with open("lastpisscheck.txt","r") as pissfile:
        try:
            lastpissdays = int(pissfile.read())
        except:
            lastpissdays = 0
    if lastpissdays < pissdays:
        pc = bot.get_channel(piss_channel)
        await pc.send("Days since dalty pissed on the floor: {}".format(pissdays))
        with open("lastpisscheck.txt","w") as pissfile:
            pissfile.write(str(pissdays))
            

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}') 
    main_channel = bot.get_channel(logs_channel)
    await main_channel.send("Starting")
    if not pisscheck.is_running():
        pisscheck.start()
        




print("Starting bot")
bot.run(monkebotsecrets.DISCORD_TOKEN)