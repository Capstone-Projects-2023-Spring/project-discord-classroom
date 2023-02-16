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

    bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
    

    @bot.event
    async def on_guild_join(guild):
        owner = guild.owner
        #to create a private channel (lounge) for educators
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            owner: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        lounge = await guild.create_text_channel("Lounge", overwrites=overwrites)

        assignments_category = await guild.create_category("Assignments")
        quizzes_category = await guild.create_category("Quizzes")
        discussions_category = await guild.create_category("Discussions")
        submissions_category = await guild.create_category("Submissions")

        assignment_text = await assignments_category.create_text_channel("Assignment")
        quiz_text = await quizzes_category.create_text_channel("Quiz")
        discussion_text = await discussions_category.create_text_channel("Discussion")
        submission_text = await submissions_category.create_text_channel("Submission")

    @bot.command()
    async def create_channel(ctx, category, topic):
        if ctx.author.id != ctx.guild.owner_id:
            await ctx.send("Error, enter '!help' for  more information.")
            return

        category_list = discord.utils.get(ctx.guild.categories, name=category)
        if category_list is None:
            await ctx.send(f"Category '{category}' not found.")
            return
            
        channel = await category_list.create_text_channel(name=topic)


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