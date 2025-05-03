import discord
import asyncio
import requests

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_server_status():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    already_online = False

    while not client.is_closed():
        try:
            response = requests.get(f"https://api.mcsrvstat.us/2/{SERVER_IP}:{SERVER_PORT}")
            data = response.json()

            if data.get('online'):
                if not already_online:
                    await channel.send(f"The Minecraft server **{SERVER_IP}:{SERVER_PORT}** is now ONLINE!")
                    already_online = True
            else:
                already_online = False

        except Exception as e:
            print(f"Error checking server: {e}")

        await asyncio.sleep(60)  # Check every 60 seconds

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    client.loop.create_task(check_server_status())  # Start server status checking once the bot is ready

client.run(TOKEN)
