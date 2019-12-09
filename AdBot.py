# Work with Python 3.6
import discord
from bc import Blockchain
import os

TOKEN = 'NjUxMTIyNzkyMjE3MDUxMTQ3.Xepk9Q.Pk1WXox8e3UealSejAxhgERRgEE'

client = discord.Client()
bc = Blockchain()
bc.add_advertiser('corpinc', 2000, "myad")

if (bc.blocks == []):
    bc.root()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!AdBot give'):
        content = message.content[11:]
        status = bc.add_transaction('server', str(message.author), int(content))
        hash = [bc.hash(value) for value in bc.blocks if value['index'] == bc.last_block]
        bc.add_block(True, hash)
        if status:
            await message.channel.send(content+" CordCoins to "+str(message.author))
        else:
            await message.channel.send("Sorry, server does not have enough funds for that.")

    if message.content.startswith('!AdBot send'):
        content = message.content[11:]
        words = content.split()
        status = bc.add_transaction(str(message.author), words[0], int(words[1]))
        hash = [bc.hash(value) for value in bc.blocks if value['index'] == bc.last_block]
        bc.add_block(True, hash)
        if status:
            await message.channel.send("Just sent "+words[1]+" CordCoins to "+words[0]+".")
        else:
            await message.channel.send("Sorry, you dont have the funds for that.")

    if message.content.startswith('!AdBot show'):
        content = message.content[12:]
        await message.channel.send(content+" has "+str(bc.users[content]['balance'])+" CordCoins")

    if message.content.startswith('!AdBot join'):
        status = bc.add_user(str(message.author))
        if status:
            await message.channel.send("You have joined CordCoin and have 0 coins.")
        else:
            await message.channel.send("You are already a member of CordCoin.")

    if str(message.author) == 'Prestoon#9786':
        if message.content.startswith('!AdBot create_advertiser'):
            content = message.content[25:].split()
            status = bc.add_advertiser(content[0], int(content[1]), content[2])
            if status:
                await message.channel.send("Created advertiser "+content[0]+" with "+content[1]+" CordCoins.")
            else:
                await message.channel.send("Name already taken. Please choose another name.")

        if message.content.startswith('!AdBot reserve'):
            content = message.content[15:].split()
            status = bc.reserve_funds(str(message.author), int(content[0]), content[1])

            if status:
                await message.channel.send(content[0]+" CordCoins reserved at "+content[1]+".")
            else:
                await message.channel.send("There was an error.")

        if message.content.startswith('!AdBot ad'):
            ad = bc.credit(str(message.author))
            await message.channel.send(ad)

        if message.content.startswith('!AdBot remove_ad'):
            content = message.content[17:]
            status = bc.remove_ad(content)
            if status:
                await message.channel.send("Ad removed.")
            else:
                await message.channel.send("Sorry, that company does not exist.")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
