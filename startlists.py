#!/usr/bin/env python3

import os
import random
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGODB = os.getenv('MONGODB')
MONGOPW = os.getenv('MONGOPW')

bot = commands.Bot(command_prefix='/')

# MongoDB connection information
conn_url = f'mongodb+srv://{MONGODB}:{MONGOPW}@cluster0.zywng.mongodb.net/cycling_startlists'
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
@bot.command(name='sl')
async def sl(ctx, *args):
    await get_startlist('2023_volta-catalunya', 'Volta', ctx, *args)
#@bot.command(name='pn')
#async def sl(ctx, *args):
#    await get_startlist('2022_paris-nice', 'PN', ctx, *args)
#@bot.command(name='ta')
#async def sl(ctx, *args):
#    await get_startlist('2022_tirreno-adriatico', 'TA', ctx, *args)

bot.run(TOKEN)
