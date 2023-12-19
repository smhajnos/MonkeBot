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
import sqlite3


monke_server = 983896046700736522
logs_channel = 1000524219517505656
mb_color = 0xc16950
piss_channel = 983896047514439682 #general
staff_channel = 983900126605107260 #staff-bots
#piss_channel = logs_channel

dataWarehouse = sqlite3.connect("datawarehouse.db")
cursor = dataWarehouse.cursor()

intents = nextcord.Intents.all()
#intents.members = True

rrhold = False


bot = commands.Bot(command_prefix='}', intents=intents)


def commit():
    dataWarehouse.commit()
    #backup to cloud?

async def staff_command(ctx):
    ctx.channel.id = staff_channel
    
    
    
def getconfig(param):
    cursor.execute("SELECT COUNT(*) FROM config WHERE param = ?",(param,))
    res = cursor.fetchone()
    if res[0] > 0:
        cursor.execute("SELECT val FROM config WHERE param = ?",(param,))
        res = cursor.fetchone()
        return res[0]
    else:
        return None

def setconfig(param, val):
    cursor.execute("SELECT COUNT(*) FROM config WHERE param = ?",(param,))
    res = cursor.fetchone()
    if res[0] > 0:
            cursor.execute("DELETE FROM config WHERE param = ?",(param,))
    cursor.execute("INSERT INTO config (param, val) VALUES (?,?)",(param,val,))
    commit()
    
@bot.slash_command(name="ping",description="Check if the bot is working", guild_ids=[monke_server])
async def ping(ctx):
    await ctx.send("Pong!")







@bot.slash_command(name="addrr",description="Add reaction role",guild_ids=[monke_server])
@commands.check(staff_command)
async def addrr(ctx,emoji, role,desc):
    cursor.execute("INSERT INTO reactroles (emoji, role, desc) VALUES (?,?,?)",(emoji,role,desc))
    commit()
    await ctx.send("Done! Don't forget to use `/updaterr` to update the message!")
    

@bot.slash_command(name="updaterr",description="Update reaction role message",guild_ids=[monke_server])
@commands.check(staff_command)    
async def updaterr(ctx):
    rrhold = True
    data = getconfig("rrdesc")
    data = "{}\r\n\r\n".format(data)
    cursor.execute("SELECT emoji, desc FROM reactroles")
    for row in cursor:
        data = "{}\r\n{} {}".format(data, row[0], row[1])
    rrchan = getconfig("rrchan")
    rrmes = getconfig("rrmes")
    chan = bot.get_channel(int(rrchan))
    mes = await chan.get_partial_message(int(rrmes)).fetch()
    await mes.edit(content=data)
    cursor.execute("SELECT emoji FROM reactroles")
    for row in cursor:
        await mes.add_reaction(row[0])
    rrhold = False
    await ctx.send("Done!")
    

@bot.slash_command(name="initrr",description="Initiate reaction role. This will reset reaction roles!",guild_ids=[monke_server])
@commands.check(staff_command)
async def initrr(ctx,channel,desc):
    rrhold = True
    chanid = int(channel[2:-1])
    cursor.execute("DELETE FROM reactroles")
    commit()
    rrchan = int(getconfig("rrchan"))
    rrmes = int(getconfig("rrmes"))
    try:
        if rrmes and rrchan:
            chan = bot.get_channel(rrchan)
            mes = await chan.get_partial_message(rrmes).fetch()
            await mes.delete()
    except:
        pass
    rrchan = chanid
    chan = bot.get_channel(rrchan)
    mes = await chan.send(desc)
    rrmes = mes.id
    setconfig("rrchan",rrchan)
    setconfig("rrmes",rrmes)
    setconfig("rrdesc",desc)
    rrhold = False
    await ctx.send("Done!")


async def reactionroles():
    cursor.execute("DELETE FROM tmpreactroles")
    rrchan = getconfig("rrchan")
    rrmes = getconfig("rrmes")
    if rrmes and rrchan:
        chan = bot.get_channel(int(rrchan))
        mes = await chan.get_partial_message(int(rrmes)).fetch()
    reactions = mes.reactions
    for reaction in reactions:
        cursor.execute("SELECT role FROM reactroles WHERE emoji = ?",(str(reaction),))
        rolestr = cursor.fetchone()[0]
        async for user in reaction.users():
            cursor.execute("INSERT INTO tmpreactroles (user, role) VALUES (?,?)",(str(user.id),rolestr,))
    commit()
    monke = bot.get_guild(monke_server)
    for role in monke.roles:
        cursor.execute("SELECT COUNT(*) FROM reactroles WHERE role = ?", (role.mention,))
        cnt = cursor.fetchone()[0]
        print("{}: {}".format(str(role),cnt))
        if cnt > 0:    
            for user in monke.members:
                if user != bot.user:
                    cursor.execute("SELECT COUNT(*) FROM tmpreactroles WHERE role = ? AND user = ?", (role.mention,str(user.id),))
                    cnt = cursor.fetchone()[0]
                    if cnt > 0:
                        if role not in user.roles:
                            print("Giving {} the {} role".format(user, role))
                            await user.add_roles(role)
                    else:
                        if role in user.roles:
                            print("Removing the {} role from {}".format(role,user))
                            await user.remove_roles(role)
            
        
            

@bot.slash_command(name="emojitest",description="Emoji test")
async def log(s):
    lc = bot.get_channel(logs_channel)
    await lc.send(s)
    
    
    

@tasks.loop(seconds=3600)
async def pisscheck():
    pissday = datetime.date(2022,9,20)
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
            


async def reactrole(payload,add):
    
    rrmes = getconfig("rrmes")
    if payload.message_id == int(rrmes):
        cursor.execute("SELECT role FROM reactroles WHERE emoji = ?",(str(payload.emoji),))
        res = cursor.fetchone()
        if res:
            rolestr = res[0]
            monke = bot.get_guild(monke_server)
            role = [role for role in monke.roles if role.mention == rolestr][0]
            user = monke.get_member(payload.user_id)
            if add:
                if role not in user.roles:
                    print("Giving {} the {} role".format(user, role))
                    await user.add_roles(role)
            else:
                if role in user.roles:
                    print("Removing the {} role from {}".format(role,user))
                    await user.remove_roles(role)


async def thanos(message):
    if message.author.id == 689365676007489542:
        thanos_emoji = bot.get_emoji(1186493812655272008)
        await message.add_reaction(thanos_emoji)

@bot.event
async def on_message(message):
      await thanos(message) 
            
@bot.event
async def on_raw_reaction_add(payload):
    await reactrole(payload,True)
        
@bot.event
async def on_raw_reaction_remove(payload):
    await reactrole(payload,False)
    

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}') 
    main_channel = bot.get_channel(logs_channel)
    await main_channel.send("Starting")
    
    #cache the reaction message
    reactchan = bot.get_channel(int(getconfig("rrchan")))
    reactmes = await reactchan.fetch_message(int(getconfig("rrmes")))
    print(reactmes.id)
    
    
    #update reaction roles that may have changed since last restart
    await reactionroles()
    
    #start timers
    if not pisscheck.is_running():
        pisscheck.start()
        




print("Starting bot")
bot.run(monkebotsecrets.DISCORD_TOKEN)