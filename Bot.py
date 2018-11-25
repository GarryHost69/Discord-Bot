Token = "NTE1ODIyNjM3NzM0Mjk3NjE0.DtvU3Q.z6Y2IRbj8VMQscb_akbl5h6PlqI"

import discord
import asyncio
import random
from itertools import cycle
from py_translator import Translator

client = discord.Client()
translator = Translator()
_game = ["Destiny", "Fortnite", "Battlefield", "Minecraft"]

async def change_status():
	await client.wait_until_ready()
	g_name = cycle(_game)
	while not client.is_closed:
		this_game = next(g_name)
		await client.change_presence(game=discord.Game(name=this_game))
		await asyncio.sleep(3600)

@client.event
async def on_ready():
	print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
	print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}:")

	if message.content.startswith('j!greet'):
		id = message.content[slice(10, (len(message.content) - 1))]
		name = await client.get_user_info(id)
		await client.send_message(message.channel, f"{message.author.name} greets {name.name}")

	if message.content.startswith('j!help'):
		embed = discord.Embed(
			color = discord.Color.green()
		)
		embed.set_author(name='Jifser Help')
		embed.add_field(name='j!hi or j!hello', value='return hello message', inline=False)
		embed.add_field(name='j!count', value='return member count', inline=False)
		embed.add_field(name='j!status', value='return status of all members', inline=False)
		embed.add_field(name='j!translate', value='return text translation and pronunciation', inline=False)
		embed.add_field(name='j!quit', value='logs out of the server', inline=False)
		embed.add_field(name='j!help', value='return help embed', inline=False)
		await client.send_message(message.channel, embed=embed)

	if "j!count" == message.content.lower():
		ct = 0
		for m in client.get_all_members():
			ct += 1
		await client.send_message(message.channel, ct)

	if "j!status" == message.content.lower():
		online = 0
		idle = 0
		offline = 0
		for m in client.get_all_members():
			if str(m.status) == "online":
				online += 1
			elif str(m.status) == "offline":
				offline += 1
			else:
				idle += 1
		await client.send_message(message.channel, f"Online: {online}.\nIdle/Busy/DND: {idle}.\nOffline: {offline}")

	if "j!hi" == message.content.lower() or "j!hello" == message.content.lower():
		await client.send_message(message.channel, f"Hello!! {message.author.name}")

	if "j!quit" == message.content.lower():
		await client.send_message(message.channel, "Bye!!")
		await client.logout()

	if "j!translate" == message.content.lower():
		await client.send_message(message.channel, "Enter Text to be translated: ")
		origin_text = await client.wait_for_message()
		origin_text = origin_text.content.lower()
		await client.send_message(message.channel, "Translate To: ")
		dest = await client.wait_for_message()
		dest = dest.content.lower()
		txt = translator.translate(origin_text, dest).text
		prn = translator.translate(origin_text, dest).pronunciation
		await client.send_message(message.channel, f"Text : {txt}\nPronunciation : {prn}")

client.loop.create_task(change_status())
client.run(Token)
