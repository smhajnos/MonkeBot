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
import monkecloud
import random
import MonkeImages

monke_server = 983896046700736522
logs_channel = 1000524219517505656
mb_color = 0xc16950
piss_channel = 983896047514439682 #general
staff_channel = 983900126605107260 #staff-bots
#piss_channel = logs_channel

#dataWarehouse = sqlite3.connect("datawarehouse.db")
#cursor = dataWarehouse.cursor()
dataWarehouse = None
cursor = None


intents = nextcord.Intents.all()
#intents.members = True

rrhold = False


bot = commands.Bot(command_prefix='}', intents=intents)


def commit():
    dataWarehouse.commit()
    #backup to cloud? - no, do that with a different call to minimize writes
   
    

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



async def monke_log(s, emergent = False):
    if emergent:
        log_str = "<@145372956304867328> EMERGENT: " + s
    else:
        log_str = s
    lc = bot.get_channel(logs_channel)
    await lc.send(s)




@bot.slash_command(name="addrr",description="Add reaction role",guild_ids=[monke_server])
@commands.check(staff_command)
async def addrr(ctx,emoji, role,desc):
    cursor.execute("INSERT INTO reactroles (emoji, role, desc) VALUES (?,?,?)",(emoji,role,desc))
    commit()
    await ctx.send("Done! Don't forget to use `/updaterr` to save your changes!")
    

@bot.slash_command(name="updaterr",description="Update reaction role message",guild_ids=[monke_server])
@commands.check(staff_command)    
async def updaterr(ctx):
    await ctx.send("Uploading changes to cloud...")
    monkecloud.upload_all()
    #if not monkecloud.upload_all():
    #    await monke_log("Cloud save error in updaterr", True)
    #await ctx.send("Done. Updating reaction role message.")
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
    
@bot.slash_command(name="deleterr",description="Delete a reaction role",guild_ids=[monke_server])
@commands.check(staff_command)
async def deleterr(ctx,desc):
    rrhold = True
    await ctx.response.defer(ephemeral=False,with_message=False)
    cursor.execute("DELETE FROM reactroles WHERE desc = ?", (desc,))
    commit()
    rrhold = False
    await ctx.send("Done! Don't forget to use `/updaterr` to update the message!")


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
            
        
            


@bot.slash_command(name="callvote",description="Call a vote",guild_ids=[monke_server])
async def callvote(ctx, text):
    await ctx.send("Calling your vote!",ephemeral=True)
    await monke_log("{} called a vote with text {}".format(ctx.user.name,text))
    em = nextcord.Embed(color=mb_color,description=text,title="Someone called a vote!")
    msg = await ctx.channel.send(embed=em)
    vote_emoji = bot.get_emoji(1192286485286752326)
    await msg.add_reaction(vote_emoji)
    vote_emoji = bot.get_emoji(1192286483420303390)
    await msg.add_reaction(vote_emoji)







@bot.slash_command(name="download_monkefiles",description="Please don't use this command if you don't know what you are doing.",guild_ids=[monke_server])
@commands.check(staff_command)
async def download_monkefiles(ctx):
    monkecloud.download_all()
    await ctx.send("Done!")

@bot.slash_command(name="upload_monkefiles",description="Please don't use this command if you don't know what you are doing.",guild_ids=[monke_server])
@commands.check(staff_command)
async def upload_monkefiles(ctx):
    monkecloud.upload_all()
    await ctx.send("Done!")










@bot.slash_command(name="where",description="where banana",guild_ids=[monke_server])
async def where_banana(ctx, text):  
    (filename, temp_files) = MonkeImages.where_banana(text)
    await ctx.send(content=None,file=nextcord.File(filename,filename="where.png"))
    MonkeImages.cleanup(temp_files)







@bot.message_command(name="agree",guild_ids=[monke_server])
async def agree(ctx, message):
    print("agreeing")
    await ctx.user.send(content="Working on your `agree` image...")
    husband = await message.author.avatar.read()
    wife = await ctx.user.avatar.read()
    text = message.content
    pics = message.attachments
    print(text)
    print(pics)
    if text != "" or pics == []:  
        print(husband)
        print(wife)
        print(text)
        (filename, temp_files) = await MonkeImages.agree(text, husband, wife)
        await ctx.send(content=None,file=nextcord.File(filename,filename="agree.png"))
        MonkeImages.cleanup(temp_files)
    else:
        print(husband)
        print(wife)
        img2 = await pics[0].read()
        (filename, temp_files) = await MonkeImages.imgagree(img2, husband, wife)
        await ctx.send(content=None,file=nextcord.File(filename,filename="agree.png"))
        MonkeImages.cleanup(temp_files)
        


@bot.message_command(name="balls",guild_ids=[monke_server])
async def balls(ctx, message):
    print("balls")
    await ctx.user.send(content="Working on your `balls` image...")
    text = message.content
    print(text)
    (filename, temp_files) = await MonkeImages.monkeballs(text)
    await ctx.send(content=None,file=nextcord.File(filename,filename="balls.png"))
    MonkeImages.cleanup(temp_files)
    
    
    

@tasks.loop(seconds=3600)
async def pisscheck():
    pissday = datetime.date(2024,8,3)
    today = datetime.date.today()
    delta = today - pissday
    pissdays = delta.days
    print("Days since last piss: {}".format(pissdays))
    with open("savedata/lastpisscheck.txt","r") as pissfile:
        try:
            lastpissdays = int(pissfile.read())
        except:
            lastpissdays = 0
    if lastpissdays < pissdays:
        pc = bot.get_channel(piss_channel)
        await pc.send("Days since dalty pissed on the floor: {}".format(pissdays))
        with open("savedata/lastpisscheck.txt","w") as pissfile:
            pissfile.write(str(pissdays))
        cloudsuccess = monkecloud.upload_file("lastpisscheck.txt")
        if not cloudsuccess:
            await monke_log("Cloud save error in pisscheck", True)
            


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
        
        
async def gwenchana(message):
    if message.author.id != 1000524966762127501:
        if random.uniform(0,1) <= 0.001:
            await message.channel.send("<a:gwenchana:1346421255980585012> Gwenchana! <a:gwenchana:1346421255980585012>")
        elif random.uniform(0,1) <= 0.001:
            await message.channel.send("EYY I'M WALKIN HERE!")
        
        

async def dm_display(message):
    if isinstance(message.channel, nextcord.DMChannel) and message.author.id !=  1000524966762127501:
        chan = bot.get_channel(staff_channel)
        
        timestamp = message.created_at.timestamp()
        em = nextcord.Embed(color=mb_color,description=message.content,title="New DM!")
        em.set_author(name=message.author.name,icon_url=message.author.display_avatar.url)
        if len(message.attachments)==0:
            await chan.send(embed=em)
        elif len(message.attachments)==1:
            attach = message.attachments[0]
            if "image" in attach.content_type:
                print(message.attachments[0].url)
                em.set_image(url=message.attachments[0].url)
            else:
                em.add_field(name="attachment:", value=message.attachments[0].url)
            await chan.send(embed=em)
        else:
            await chan.send(embed=em)
            for attach in message.attachments:
                em = nextcord.Embed(color=mb_color,description="",title="Attachments!")
                if "image" in attach.content_type:
                    em.set_image(url=attach.url)
                else:
                    em.add_field(name="attachment:", value=message.attachments[0].url)
                await chan.send(embed=em)
        


@bot.event
async def on_message(message):
      await thanos(message) 
      await dm_display(message)
      await gwenchana(message)
            
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
    try:
        await reactionroles()
    except:
        pass
    
    #start timers
    try:
        if not pisscheck.is_running():
            pisscheck.start()
    except:
        pass




print("Starting bot")
monkecloud.download_all()
dataWarehouse = sqlite3.connect("savedata/datawarehouse.db")
cursor = dataWarehouse.cursor()
bot.run(monkebotsecrets.DISCORD_TOKEN)