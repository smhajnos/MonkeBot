# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 18:03:41 2022

@author: sam
"""


import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
import monkebotsecrets


monke_server = 983896046700736522
logs_channel = 1000524219517505656
nb_color = 0xc16950

intents = nextcord.Intents.all()
#intents.members = True


bot = commands.Bot(command_prefix='}', intents=intents)


@bot.slash_command(name="ping",description="Check if the bot is working", guild_ids=[monke_server])
async def ping(ctx):
    await ctx.send("Pong!")

async def log(s):
    lc = bot.get_channel(logs_channel)
    await lc.send(s)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}') 
    main_channel = bot.get_channel(logs_channel)
    await main_channel.send("Starting")


print("Starting bot")
bot.run(monkebotsecrets.DISCORD_TOKEN)