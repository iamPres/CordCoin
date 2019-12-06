# Work with Python 3.6
import discord
from io import BytesIO
from PIL import Image
from google_images_search import GoogleImagesSearch
from apiclient.discovery import build
from bc import Blockchain
import os

TOKEN = 'NjUxMTIyNzkyMjE3MDUxMTQ3.XeVTkw.V314i8FKkT5HN8GNUw5ZFTbx7BI'
service = build("customsearch", "v1", developerKey='AIzaSyBQMIDzjmqK-1TihoSr7nKeGJz7qvsy0r4')

client = discord.Client()
bc = Blockchain()
bc.root()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!assfuck'):

        content = message.content[8:]
        print(content)

        bc.add_transaction('server', str(message.author), 1000)
        hash = [bc.hash(value) for value in bc.blocks if value['index'] == bc.last_block]
        bc.add_block(True, hash)
        print("1000 PornCoins to "+str(message.author))
        print(bc.blocks)

        results = service.cse().list(q=content, cx= '013387425609910095295:cr2d9dcnfkc').execute()

        await message.channel.send(str(results['items'][1]['title']+"\n"+results['items'][1]['link']))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
