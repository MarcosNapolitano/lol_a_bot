import discord
import requests
import json
from decouple import config

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f"We are now logged in as {client.user}")

@client.event
async def on_message(message):

	if message.author == client.user:
		return

	if message.content.startswith("$hello"):
		await message.channel.send("Hello!")


client.run(config("Token"))