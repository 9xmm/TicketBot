import discord
import responses
from discord.ext import tasks
from datetime import datetime, timedelta
import asyncio

welcome_sent = {}
closed_ticket_warn = {}

########################################

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)
        
########################################
        
def run_discord_bot():
    TOKEN = 'MTE1MTU3NTg0MjU2OTMyNjU5Mg.GZNBSm.uMTmxDep4t-IOn2xyNTR-Bt7b7VoNBvX0U0U68'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @tasks.loop(seconds=5)
    async def delete_inactive_channels():
        category_name = "closed tickets"
        # Get the current server (guild)
        guild = discord.utils.get(client.guilds, name='9xm server') 
        if guild is None:
            print("Guild not found.")
            return
        # Find category by name
        category = discord.utils.get(guild.categories, name=category_name)
        if category is None:
            print(f'Category "{category_name}" not found.')
            return
        for channel in category.text_channels:
            # Check if the channel has a last message and if it has been inactive for 2 days
            if channel.last_message is not None and (discord.utils.utcnow() - channel.last_message.created_at).total_seconds() >= 172800:
                await channel.delete()
                print(f'Deleted inactive channel: {channel.name}')

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        delete_inactive_channels.start()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            if message.author.bot or not message.guild:
                return
        # Check message sent in channel under category "created tickets"
        if message.channel.category and message.channel.category.name.lower() == "created tickets":
            if message.channel.id not in welcome_sent:
                await message.channel.send("Thanks for showing interest in our vision! Please follow this link to fill out our collab form: https://www.machinatrader.com/collab-and-influencer-registration/ :relaxed:")
                welcome_sent[message.channel.id] = True
        elif message.channel.category and message.channel.category.name.lower() == "closed tickets":
            if message.channel.id not in closed_ticket_warn:
                await message.channel.send("This ticket has been closed! This channel will be deleted after 2 days of inactivity :relaxed: ")
                closed_ticket_warn[message.channel.id] = True
                   

#############################################


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
