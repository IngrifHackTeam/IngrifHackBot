import io
import aiohttp
import discord,asyncio,os
from discord.ext import commands, tasks
from dateutil.parser import parse
import json
from urllib import request
from urllib.request import Request, urlopen


TOKEN = "MTA4NTE5NzIyMzA3MzE2MTI3Ng.G1K1TK.42zQTmIW5m8HxiZXbmJQoxPeVBQBca8_WDjnNI"

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('ctf'):
        await message.channel.send('Hello!')

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
    ctftime_url = "https://ctftime.org/api/v1/events/?limit=10"
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

        if event['participants'] >=15:
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

client.run(TOKEN)
