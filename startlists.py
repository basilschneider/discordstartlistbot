#!/usr/bin/env python3

import os
import random
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

#race = 'Strade Bianche 2021'

# MongoDB connection information
conn_url = 'mongodb+srv://live-radsport:anOrdinaryPassword@cluster0.zywng.mongodb.net/cycling_startlists'
cluster_name = 'cycling_startlists'
#db_name = '2021_volta-catalunya'

# Connect to MongoDB
cluster = MongoClient(conn_url)
db = cluster[cluster_name]
#collection = db[db_name]

# Report when connected
@bot.event
async def on_ready():
    print("Connected")

# Generic function to output data
async def get_startlist(collectionname, racename, ctx, *args):

    ## Delete sl command from user
    #await ctx.message.delete()

    print(f'[{racename}] User {ctx.author} asks for start number(s) {args}.')

    response = ''
    for sslnr in args:

        try:
            islnr = int(sslnr)
            try:
                # Get record from MongoDB
                record = db[collectionname].find_one({'number': islnr})

                # Create response
                response += f'\n[{racename}] {record["number"]} {record["name"]} ({record["team"]}) '
            except TypeError:
                response += f'\n[{racename}] Einen Fahrer mit Nummer {islnr} gibt\'s gar nicht. :-( '
        except ValueError:
            response += f'{sslnr} '
            #response += 'egal, gutr wille war da. es gibt solche tage\n'


    # Send response
    #await ctx.author.send(response)
    await ctx.send(response)

# Handle sl command
#@bot.command(name='vc', help=race)
#async def vc(ctx, *args):
#    await get_startlist('2021_volta-catalunya', 'VC', ctx, *args)
#@bot.command(name='gw', help=race)
#async def gw(ctx, *args):
#    await get_startlist('2021_gent-wevelgem', 'GW', ctx, *args)
@bot.command(name='sl')
async def sl(ctx, *args):
    await get_startlist('2021_dauphine', 'Dauphine', ctx, *args)

bot.run(TOKEN)
