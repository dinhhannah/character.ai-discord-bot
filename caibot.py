# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
DISCORD_TOKEN = "" #given when making a Discord bot

import asyncio
import random

from characterai import PyAsyncCAI
CAI_TOKEN = "" #In the URL of the character's chat in character.ai
CAI_ID = "" #See kramcat's documentation on how to get this

load_dotenv() #load environment variables

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if (message.author.id != client.user.id):
        if client.user.mentioned_in(message):
            print("generating response...")
            async with message.channel.typing():

                mssg = (str(message.content))

                CAIclient = PyAsyncCAI(CAI_TOKEN)
                await CAIclient.start()

                char = CAI_ID

                chat = await CAIclient.chat.get_chat(char)

                history_id = chat['external_id']
                participants = chat['participants']

                if not participants[0]['is_human']:
                    tgt = participants[0]['user']['username']
                else:
                    tgt = participants[1]['user']['username']

                data = await CAIclient.chat.send_message(
                    char, mssg, history_external_id=history_id, tgt=tgt
                )

                botmssg = data['replies'][0]['text']

            await message.channel.send(f"{botmssg}")
        
client.run(DISCORD_TOKEN)
