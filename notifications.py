import discord
from discord.ext import commands

import json
import re


# CONSTANT VARIABLE
DB_PATH = "database/contacts.json"
REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# GETS DATABASE DATA
def load_json(path):
    with open(path, 'r') as f:
        dictionary = json.load(f)
    return dictionary


# UPDATES DATABASE DATA
def dump_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent = 4)


class Notifications(commands.Cog):
    def __init(self, client):
        self.client = client


    @commands.command(aliases = ['su', 'add'])
    async def setup(self, ctx, *, email):
        if (re.fullmatch(REGEX, email)):
            contact = load_json(DB_PATH)
            email_list = contact["emails"]
            if email.lower() not in email_list:
                email_list.append(email.lower())
                contact = {'emails': email_list} 
                dump_json(DB_PATH, contact)
                await ctx.reply("Successfully added your email to the database!", mention_author = False)
            else:
                await ctx.reply("Your email is already in our database", mention_author = False)
        else:
            await ctx.reply("Invalid email! Please try again!", mention_author = False)


def setup(client):
    client.add_cog(Notifications(client))
