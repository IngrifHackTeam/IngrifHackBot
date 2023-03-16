import io
import aiohttp
import datetime
import discord,asyncio,os
from discord.ext import commands, tasks
from dateutil.parser import parse
import json
from urllib import request
from urllib.request import Request, urlopen


TOKEN = ""

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!scoreboard'):
        embedVar=discord.Embed(title="STATS", description= get_stat(), color=0xff0000)
        await message.channel.send(embed=embedVar)

@tasks.loop(hours=168)
async def myloop():
    embedVar = discord.Embed(title="CAPTURE THE FLAGS", description=await ctftime_contest(), color=0xff0000)
    await client.get_channel(1080970448155721818).send(embed=embedVar)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    if not myloop.is_running():
        myloop.start()

async def ctftime_contest() :
    ctftime_url = "https://ctftime.org/api/v1/events/?limit=20"
    answ = Request(ctftime_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"})
    resp = urlopen(answ).read()
    # Decode response json into utf8 then load
    # into a dictionary using json module
    resp_body = resp.decode('utf8')
    events = json.loads(resp_body)

    # Initialize string to return
    contests_string = "Next CTFs\n\n"
    embedVar = discord.Embed(title="CAPTURE THE FLAGS", description="Next 5 CTFS!", color=0x00ff00)

    for event in events:

        # Iterate over the dictionary to extract
        # info for all on-line competitions
        if event['onsite'] == True:
            continue

        if event['weight']!= 0:
            contests_string += "Site: {}\n".format(event['url'])
            contests_string += "Name: {}\n".format(event['title'])
            embedVar.add_field(name="Name: ", value=event['title'], inline=False)
            contests_string += "Weight: {}\n".format(event['weight'])
            time_meta = event['start']
            time_comp = parse(time_meta).isoformat(' ')
            time = time_comp.split('+')[0]
            contests_string += "From: {}\n".format(time)
            embedVar.add_field(name="From: ", value=time, inline=False)

            time_meta = event['finish']
            time_comp = parse(time_meta).isoformat(' ')
            time = time_comp.split('+')[0]
            contests_string += "To: {}\n".format(time)
            embedVar.add_field(name="To: ", value=time, inline=False)

            contests_string += "Format: {}\n".format(event['format'])
            embedVar.add_field(name="Format: ", value=event['format'], inline=False)
            contests_string += "Duration: {} Days {} Hours\n\n".format(event['duration']['days'], event['duration']['hours'])
            embedVar.add_field(name = chr(173), value = chr(173))
    return contests_string

def get_stat():
    ctftime_url = "https://ctftime.org/api/v1/teams/193569/"
    answ = Request(ctftime_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"})
    resp = urlopen(answ).read()
    # Decode response json into utf8 then load
    # into a dictionary using json module
    resp_body = resp.decode('utf8')
    events = json.loads(resp_body)

    today = datetime.date.today()
    year = today.year
    # Initialize string to return
    contests_string = "IngrifHack Stats\n\n"

    contests_string += "Name: {}\n".format(events['name'])
    contests_string += "Country: {}\n".format(events['country'])
    contests_string += "Country Rating: {}\n".format(events['rating'][str(year)]['country_place'])
    contests_string += "Global Rating: {}\n".format(events['rating'][str(year)]['rating_place'])

    return contests_string

client.run(TOKEN)
