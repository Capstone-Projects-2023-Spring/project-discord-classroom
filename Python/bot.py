import discord
import json
import os
from supabase import create_client, Client
import random
from discord.ext import commands
from typing import Optional

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemp = {"DiscordToken": "", "Prefix": "!", "SupaUrl": "", "SupaKey": "", "SupaSecret": ""}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemp, f)

def run_discord_bot():
    DISCORD_TOKEN = configData["DiscordToken"]
    PREFIX = configData["Prefix"]
    SB_URL = configData["SupaUrl"]
    SB_KEY = configData["SupaKey"]
    SB_SECRET = configData["SupaSecret"]

    supabase: Client = create_client(SB_URL, SB_KEY)

    bot = commands.Bot(command_prefix=PREFIX)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    @bot.command()
    async def testInsert(ctx, arg1, arg2):
        list = {'student_name': arg1, 'grade': arg2}
        data = supabase.table("TestTable").insert(list).execute()
        print(data)
        await ctx.channel.send("Inserted new student")

    async def poll(ctx, prompt, opt1, opt2, opt3:Optional[str] = None, opt4:Optional[str] = None):
        # TODO - poll command, 'prompt' is the question and the opt1 -> opt4 are the options. opt1 and 2 being required, others are optional
        return

    bot.run(DISCORD_TOKEN)