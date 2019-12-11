# Work with Python 3.6
import discord
from bc import Blockchain
import os
import requests
import json
import asyncio

TOKEN = 'NjUxMTIyNzkyMjE3MDUxMTQ3.Xe7lKQ.lvVvfRmfOajpLV5ZSpHJfJ_CdGI'
transaction_url='https://7sbk6kabq4.execute-api.us-east-2.amazonaws.com/test2/ManageBlockChain/create-transaction'
view_balance_url='https://7sbk6kabq4.execute-api.us-east-2.amazonaws.com/test2/ManageBlockChain/view-balance'
delete_user_url='https://7sbk6kabq4.execute-api.us-east-2.amazonaws.com/test2/ManageBlockChain/delete-user'
create_user_url='https://7sbk6kabq4.execute-api.us-east-2.amazonaws.com/test2/ManageBlockChain/create-user'
sync_url='https://7sbk6kabq4.execute-api.us-east-2.amazonaws.com/test2/ManageBlockChain/sync'
transaction_listener_url='https://7sbk6kabq4.execute-api.us-east-2.amazonaws.com/test2/ManageBlockChain/transaction-listener'
validated_url='https://7sbk6kabq4.execute-api.us-east-2.amazonaws.com/test2/ManageBlockChain/validate-transaction'

def sync():
	content = requests.get(sync_url)
	
async def listener():
	incoming_transaction = ""
	last_transaction = ""
	while True:
		incoming_transaction = requests.post(transaction_listener_url)
		current = eval(incoming_transaction.content)
		current_transaction = current['Item']
		if str(last_transaction) != str(current_transaction['id']):
			print("INCOMING TRANSACTION")	
			print(current_transaction)
			status = requests.post(url=view_balance_url,data=json.dumps({'name':current_transaction['sender']}))
			content = eval(status.content)
			balance = content['data']
			if int(current_transaction['amount']) <= int(balance):
				requests.post(url=validated_url,data=json.dumps({'validated':'True'}))
			else:
				requests.post(url=validated_url,data=json.dumps({'validated':'False'}))
				
		last_transaction = current_transaction['id']
		
		await asyncio.sleep(1)

sync()		
asyncio.Task(listener())
		
client = discord.Client()
bc = Blockchain()
bc.add_advertiser('corpinc', 2000, "myad")
listener()
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
		status = requests.post(url=transaction_url,data=json.dumps({'sender': str('sdsdd'), 'reciever': words[1], 'amount': words[0]}))
		content = eval(status.content)
		if content['statusCode'] == 200:
			await message.channel.send(words[0]+" CordCoin has been sent to "+words[1])
		else:		
			await message.channel.send(content['statusText'])

	if message.content.startswith('!AdBot balance'):
		status = requests.post(url=view_balance_url,data=json.dumps({'name':str(message.author)}))
		content = eval(status.content)
		if content['statusCode'] == 200:		
			await message.channel.send("You have "+str(content['data'])+" CordCoin.")
		else:
			await message.channel.send("Something went wrong.")

	if message.content.startswith('!AdBot join'):
		status = requests.post(url=create_user_url,data=json.dumps({'name':str(message.author)}))
		content = eval(status.content)
		print(content)
		if content['statusCode'] == 200:
			await message.channel.send("You have joined CordCoin and have 0 coins.")
		else:
			await message.channel.send("You are already a member of CordCoin.")
			
	if message.content.startswith('!AdBot leave'):
		status = requests.post(url=delete_user_url,data=json.dumps({'name':str(message.author)}))
		content = eval(status.content)
		if content['statusCode'] == 200:
			await message.channel.send("You have left CordCoin.")
		else:
			await message.channel.send("Something went wrong.")

	if str(message.author) == 'Prestoon#9786':
		if message.content.startswith('!AdBot reserve'):
			content = message.content[15:].split()
			status = bc.reserve_funds(str(message.author), int(content[0]), content[1])

			if status:
				await message.channel.send(content[0]+" CordCoins reserved at "+content[1]+".")
			else:
				await message.channel.send("There was an error.")

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(TOKEN)
