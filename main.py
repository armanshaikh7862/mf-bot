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
        await client.change_presence(game=discord.Game(name='for !mfhelp'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='with '+str(len(set(client.get_all_members())))+' users'))
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

@client.command(pass_context=True)
async def gifsearch(ctx, *keywords):
    if keywords:
        keywords = "+".join(keywords)
    else:
        await client.say('Invalid args')
        return
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title='Search Results for', description=f'{keywords}', color = discord.Color((r << 16) + (g << 8) + b))
    url = ("http://api.giphy.com/v1/gifs/search?&api_key={}&q={}"
           "".format(GIPHY_API_KEY, keywords))
    async with aiohttp.get(url) as r:
        result = await r.json()
        if r.status == 200:
            if result["data"]:
                embed.set_image(url=result["data"][0]["url"])
                embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
                embed.timestamp = datetime.datetime.utcnow()
                await client.say(embed=embed)
            else:
                await client.say("No results found.")
        else:
            await client.say("Error contacting the API")
        
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def say(ctx, *, msg = None):
    await client.delete_message(ctx.message)
    if ctx.message.author.bot:
      return
    else:
      if not msg: await client.say("Please specify a message to send")
      else: await client.say(msg)

@client.command(pass_context = True)
async def meme(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title='Random Meme', description='from reddit', color = discord.Color((r << 16) + (g << 8) + b))
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.reddit.com/r/me_irl/random") as r:
            data = await r.json()
            embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
            embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.timestamp = datetime.datetime.utcnow()
            await client.say(embed=embed)
        
	
@client.command(pass_context=True)
async def tweet(ctx, usernamename:str, *, txt:str):
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={usernamename}&text={txt}"
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            res = await r.json()
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
            embed.set_image(url=res['message'])
            embed.title = "{} twitted: {}".format(usernamename, txt)
            await client.say(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["r", "r34", "rule"])
@commands.cooldown(3, 5)
async def rule34(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	limit = 100
	if message==None:
		listu = ["anime", "ass", "boobs", "anal", "pussy", "thighs", "yaoi", "yuri", "bdsm"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, message)
	try:
		response = requests.get(url)
		data = json.loads(response.text)
		limit = len(data)
	except json.JSONDecodeError:
		embed=discord.Embed(description = "Couldn't find a picture with that tag or there was a server problem", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = "http://img.rule34.xxx/images/{}/{}".format(x["directory"], x["image"])
	embed=discord.Embed(title = "Enjoy {}, lewd!!!".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From Rule34, Tag: {}, Results found: {}".format(message, limit))
	await client.say(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["yan"])
@commands.cooldown(3, 5)
async def yandere(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	limit = 100
	if message==None:
		listu = ["pantsu", "swimsuits", "dress", "breasts", "animal ears", "open shirt", "bra", "no bra", "cameltoe", "loli"\
				" thighhighs", "cleavage", "nipples", "ass", "bikini", "naked", "pussy", "panty pull", "see through", "underboob"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://yande.re/post/index.json?limit={}&tags={}".format(limit, message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = x["file_url"]
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From yande.re, Tag: {}, Results found: {}".format(message, limit))
	await client.say(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["dan"])
@commands.cooldown(3, 5)
async def danbooru(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	limit = 100
	if message==None:
		listu = ["breasts", "blush", "skirt", "thighhighs", "large breasts", "underwear", "panties"\
				"nipples", "ass", "pantyhose", "nude", "pussy"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://danbooru.donmai.us/post/index.json?limit={}&tags={}".format(limit, message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	x = data[random.randint(0, limit-1)]
	if x["file_url"].startswith("http"):
		final_url = x["file_url"]
	else:
		final_url = "http://danbooru.donmai.us{}".format(x["file_url"])
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From danbooru, Tag: {}, Results found: {}".format(message, limit))
	await client.say(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["gel"])
@commands.cooldown(3, 5)
async def gelbooru(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	limit = 100
	if message==None:
		listu = ["ass", "breasts", "cameltoe", "long hair", "female", "pussy", "nude", "on bed"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit,message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = x["file_url"]
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From gelbooru, Tag: {}, Results found: {}".format(message, limit))
	await client.say(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["xb"])
@commands.cooldown(3, 5)
async def xbooru(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	limit = 100
	if message==None:
		listu = ["ass", " breasts", "pussy", "female", "nude", "bdsm", "spanking"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://xbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = "http://img3.xbooru.com/images/{}/{}".format(x["directory"], x["image"])
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From xbooru, Tag: {}, Results found: {}".format(message, limit))
	await client.say(embed=embed)

@client.command(pass_context=True, no_pm=True, aliases=["rb"])
@commands.cooldown(10, 10)
async def realbooru(ctx, *, message:str=None):
	if ctx.message.channel.is_nsfw == False:
		embed=discord.Embed(description = "This is not a **nsfw** channel", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	limit = 100
	if message==None:
		listu = ["ass", " breasts", "pussy", "female", "nude", "bdsm", "spanking"]
		message = listu[random.randint(0, len(listu)-1)]
	message = message.replace(" ", "_")
	url = "https://realbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, message)
	response = requests.get(url)
	data = json.loads(response.text)
	limit = len(data)
	if not data:
		embed=discord.Embed(description = "Couldn't find a picture with that tag", color = color_blue)
		x = await client.say(embed=embed)
		await asyncio.sleep(5)
		return await client.delete_message(x)
	x = data[random.randint(0, limit-1)]
	final_url = "https://realbooru.com/images/{}/{}".format(x["directory"], x["image"])
	embed=discord.Embed(title = "Enjoy {}, ".format(ctx.message.author.name), color = color_blue)
	embed.set_image(url = final_url)
	embed.set_footer(text = "From realbooru, Tag: {}, Results found: {}".format(message, limit))
	await client.say(embed=embed)
		
        
@client.command(pass_context = True)
async def help(ctx):
    if ctx.message.author.bot:
      return
    else:
      author = ctx.message.author
      r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
      embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
      embed.set_author(name='Help')
      embed.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
      embed.add_field(name = '!mfsay',value ='To make bot send any message in channel',inline = False)
      embed.add_field(name = '!mfmeme',value = 'To see rabdom memes',inline = False)
      embed.add_field(name = '!mfjoke',value ='To see random jokes',inline = False)
      embed.add_field(name = '!mfgifsearch',value ='To search anything and get result as gif image',inline = False)
      embed.add_field(name = '!mfteet',value ='To tweet anything from any id. Example: ``!mftweet <UserName of twitter> <any text>``',inline = False)
      embed.add_field(name = "NSFW", value = "`!mfrule34`, `!mfyandere`, `!mfdanbooru`, `!mfgelbooru`, `!mfxbooru`, `!mfrealbooru`, `!mfgif`")
      embed.add_field(name = 'Music Commands',value ='``!mfplay``, ``!mfstop``, ``!mfskip``, ``!mfvolume``, ``!mfnp`` and ``!mfqueue``.',inline = False)
      await client.say(embed=embed)
     

        
client.run(os.getenv('Token'))
