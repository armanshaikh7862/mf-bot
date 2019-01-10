import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import colorsys
import random
import platform
from discord import Game, Embed, Color, Status, ChannelType
import os
import functools
import time
import datetime
import requests
import json
import praw
import aiohttp
from imgurpython import ImgurClient
from random import choice, shuffle

client = commands.Bot(description="MF Bot", command_prefix=commands.when_mentioned_or("!mf"), pm_help = True)
reddit = praw.Reddit(client_id='G-SK66FZT8at9g',
                     client_secret='DLqIkkdoD0K8xKpxuaMAhRscrS0',
                     user_agent='android:com.G-SK66FZT8at9g.SolarBot:v1.2.3 (by /u/LaidDownRepaer)')

CLIENT_ID = "1fd3ef04daf8cab"
CLIENT_SECRET = "f963e574e8e3c17993c933af4f0522e1dc01e230"
imgur = ImgurClient(CLIENT_ID,CLIENT_SECRET)

GIPHY_API_KEY = "dc6zaTOxFJmzC"


client.remove_command('help')

async def status_task():
    while True:
        await client.change_presence(game=discord.Game(name='for mv!help'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='with '+str(len(set(client.get_all_members())))+' users'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='in '+str(len(client.servers))+' servers'))
        await asyncio.sleep(5)
        
@client.event
async def on_ready():
    print('Started Our BOT')
    print('Created for ShreyasMF')
    client.loop.create_task(status_task())

@client.command(pass_context=True)
async def joke(ctx):
    res = requests.get(
            'https://icanhazdadjoke.com/',
             headers={"Accept":"application/json"}
             )
    if res.status_code == requests.codes.ok:
        await client.say(str(res.json()['joke']))
    else:
        await client.say('oops!I ran out of jokes')

client.run(os.getenv('Token'))
