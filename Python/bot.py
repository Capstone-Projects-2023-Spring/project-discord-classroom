import discord
import commands

async def send_message(message, user_message, is_private):
    try:
        response = commands.handle_command(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTA2OTEzNjQ3MTYzNTgwMDE2NA.GzpHp8.dpQBjwRjlILuhf_p6Sa3gT7JTHxgYBYORmiWnA'
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message): #Function is called whenever a message is sent
        #If the message came from the bot, ignore it
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(message)
        print(f"{username} said '{user_message}' ({channel})")

        #Ignores all messages without the ! indicator
        if user_message[0] != '!':
            return

        #Removes the '!' from the message
        user_message = user_message[1:]
        await send_message(message, user_message, is_private=False)

    client.run(TOKEN)