import discord
import responses
from discord.ext import tasks
from datetime import datetime, timedelta

welcome_sent = {}

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTE1MTU3NTg0MjU2OTMyNjU5Mg.GLI0lc.RprJJHaPNQKvddeimIlOqrR70jsBx6Mzso2T6A'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

    @client.event
    async def on_message(message):
        if message.author.bot or not message.guild:
            return

        # Check message sent in channel under category "created tickets"
        if message.channel.category and message.channel.category.name.lower() == "created tickets":
            if message.channel.id not in welcome_sent:
                await message.channel.send("Thanks for showing interest in our vision! Please follow this link to fill out our collab form: https://www.machinatrader.com/collab-and-influencer-registration/ :relaxed:")
                welcome_sent[message.channel.id] = True

    @tasks.loop(minutes=1)
    async def check_inactive_channels():
        # Get the current time
        current_time = datetime.now()

        # Iterate through all channels
        for guild in client.guilds:
            for category in guild.categories:
                if category.name.lower() == "closed tickets":
                    for channel in category.text_channels:
                        # Check if channel is older than 2 days
                        last_message = await channel.history(limit=1).flatten()
                        if last_message:
                            last_message_time = last_message[0].created_at
                            if current_time - last_message_time > timedelta(days=2):
                                await channel.delete()
                                print(f"Deleted inactive channel: {channel.name} in {category.name}")
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}"  ({channel}) ')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message,  is_private=False)


    client.run(TOKEN)
