import asyncio
from http import client
import discord
import json
import os
from supabase import create_client, Client
import random
from discord.ext import commands
from typing import Optional
import io
import datetime
from PyPDF2 import PdfReader

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemp = {"DiscordToken": "", "Prefix": "!", "SupaUrl": "", "SupaKey": ""}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemp, f)

def run_discord_bot():
    DISCORD_TOKEN = configData["DiscordToken"]
    PREFIX = configData["Prefix"]
    SB_URL = configData["SupaUrl"]
    SB_KEY = configData["SupaKey"]

    supabase: Client = create_client(SB_URL, SB_KEY)

    bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
    
    @bot.event
    async def on_guild_join(guild):
        all_perms = discord.Permissions.all()
        owner_role = await guild.create_role(name="Educator", color=discord.Color(0xffff00), permissions=all_perms)
        grading_perms = discord.Permissions.all_channel()
        await guild.create_role(name="Assistant", color=discord.Color(0xff8800), permissions=grading_perms)
        student_perms = discord.Permissions.none()
        student_perms.update(
            add_reactions=True, stream=True, read_messages=True, view_channel=True,
            send_messages=True, embed_links=True, attach_files=True, read_message_history=True,
            connect=True, speak=True, use_voice_activation=True, change_nickname=True, use_application_commands=True,
            create_public_threads=True, send_messages_in_threads=True, use_embedded_activites=True
        )
        await guild.create_role(name="Student", color=discord.Color(0x8affe9), permissions=student_perms)
        #gives discord owner the Educator role
        await guild.owner.add_roles(owner_role)
        everyone_perms = discord.Permissions.none()
        everyone_perms.update(
            read_message_history=True, read_messages=True
        )
        everyone = guild.default_role
        await everyone.edit(permissions=everyone_perms)

        general = await guild.create_category("General")
        await guild.create_text_channel("General", category=general)
        await guild.create_text_channel("Announcements", category=general)
        await guild.create_text_channel("Lounge", category=general)
        await guild.create_text_channel("Syllabus", category=general)
        roles = await guild.create_text_channel("Roles", category=general)
        await roles.set_permissions(everyone, read_messages=True, send_messages=False)
        await guild.create_category("Assignments")
        await guild.create_category("Quizzes")
        await guild.create_category("Discussions")
        await guild.create_category("Submissions")
        questions = await guild.create_category("Questions")
        await guild.create_text_channel("Public", category=questions)
        await guild.create_text_channel("Private", category=questions)

    #Gives new users the Student role
    @bot.event
    async def on_member_join(member):
        role = discord.utils.get(member.guild.roles, name="Student")
        await member.add_roles(role)

    @bot.event
    async def on_guild_channel_create(channel):
        #Add guild to Classroom table
        pass

    @bot.event
    async def on_guild_channel_delete(channel):
        #Remove guild from Classroom table
        pass

    #public and private questions from dms to proper channels 
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        if isinstance(message.channel, discord.DMChannel):
            if message.content.startswith('!public '):
                for guild in client.guilds:
                    if message.author in guild.members:
                        target_channel_id = discord.utils.get(guild.text_channels, name='Public')
                        content = message.replace('!public', '').strip()
                        await target_channel_id.send(f'Anonymous: {content}')
                        break
            elif message.content.startswith('!private '):
                for guild in client.guilds:
                    if message.author in guild.members:
                        target_channel_id = discord.utils.get(guild.text_channels, name='Private')
                        content = message.replace('!private', '').strip()
                        await target_channel_id.send(f'{message.author}: {content}')
                        break           
            


    @bot.command(name = 'channelCreate', help = '!channelCreate [category] [topic] when educator wants to create a channel under a category')
    async def create_channel(ctx, category, topic):
        if ctx.author.id != ctx.guild.owner_id:
            await ctx.send("Error, enter '!help' for  more information.")
            return

        category_list = discord.utils.get(ctx.guild.categories, name=category)
        if category_list is None:
            await ctx.send(f"Category '{category}' not found.")
            return
            
        channel = await category_list.create_text_channel(name=topic)


    @bot.command(name = 'syllabus', help = '!syllabus [attach .pdf file] - Creates a syllabus text channel with the .pdf as a message for students to download and view the syllabus. Library to view syllabus contents on discord.')
    async def syllabus(ctx):
        if ctx.author.id != ctx.guild.owner_id:
            await ctx.send("Error, enter '!help' for  more information.")
            return
        owner = ctx.guild.owner
        #restrict syllabus channel but allow for visibility.
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
            owner: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        attachments = ctx.message.attachments
        if len(attachments) == 0:
            await ctx.send("Please attach a syllabus file to upload.")
        else:
            pdf = attachments[0]
            if pdf.filename.endswith(".pdf"):
                file_data =  await pdf.read()
                # Check whether "syllabus" channel exists;
                channel = discord.utils.get(ctx.guild.channels, name="syllabus")
                if channel is None:
                    channel = await ctx.guild.create_text_channel("syllabus", overwrites=overwrites)

                await channel.send("**```diff\n+ Class Syllabus```**")
                pdf_reader = PdfReader(io.BytesIO(file_data))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                text_bytes = text.encode('utf-8')
                max_char = 1500
                #append and exclude unicodeerror
                chunks = [text_bytes[i:i+max_char].decode('utf-8', errors='ignore') for i in range(0, len(text_bytes), max_char)]
                
                #send text representation of syllabus to syllabus channel
                for chunk in chunks:
                    await channel.send("```"+chunk+"```")
                await channel.send("**```diff\n- Please note, the text representation of the syllabus may not be completely accurate. For a more precise version, download syllabus provided below.```**")
                
                # Send PDF "syllabus" channel
                await channel.send(file=discord.File(io.BytesIO(file_data), filename=pdf.filename))
                await ctx.send("Syllabus uploaded successfully.")
                
            else:
                await ctx.send("Invalid file format, only PDF files are accepted.")

    @bot.command(name = 'poll', help = '!poll [prompt] [option 1] [option 2] *[option 3] ... [*option n] - Creates a poll where students vote through reactions.')
    async def poll(ctx, prompt, *options):
        if len(options) <= 1:
            await ctx.send('You need more than one option to create a poll!')
            return
        if len(options) > 8:
            await ctx.send('You cannot create a poll with more than 8 options!')
            return

        #Create the poll embed
        embed = discord.Embed(title=prompt, description=' '.join([f'{chr(0x1f1e6 + i)} {option}\n' for i, option in enumerate(options)]))

        # Send the poll message and add reactions
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            
            await message.add_reaction(chr(0x1f1e6 + i))

        
    @bot.command(name = 'attendance', help = '!attendance - Creates a simple poll with one option prompting user to react to prove they are attending the class. ')
    async def attendance(ctx, time: int = 5):
        user = ctx.author
        Assistant = discord.utils.get(ctx.guild.roles, name="Assistant")
        Educator = discord.utils.get(ctx.guild.roles, name="Educator")
        #Student = discord.utils.get(member.guild.roles, name="Student")
        if Educator or Assistant in user.roles:
            date = datetime.datetime.now().strftime("%m - %d - %y %I:%M %p")
            message = await ctx.send("React to this message to check into todays attendance")
            await message.add_reaction('✅')
            await asyncio.sleep(time*60)
            reaction = discord.utils.get(message.reactions, emoji = '✅')
            users = await reaction.users().flatten()
            users = [user.name for user in users if not user.bot]
            response = "Attendance for {date}:\n" + '\n'.join(users)
            await ctx.author.send(response)
        

    @bot.command(name='ta', help='!ta @user - Gives the user the assistant role')
    async def ta(ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Assistant")
        await user.add_roles(role)
        await ctx.send(f"{user.mention} has been given the Assistant role")

    @bot.command(name='edu', help='!edu @user - Gives the user the educator role')
    async def edu(ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Educator")
        await user.add_roles(role)
        await ctx.send(f"{user.mention} has been given the Educator role")

    @bot.command(name='private', help=' !private - Creates a private text-channel between the student and teacher')
    async def private(ctx, *args):
        question = ' '.join(args)
        user = ctx.author.mention
        u = ctx.author
        response = user
        q = discord.utils.get(ctx.guild.categories, name="Questions")

        if q is None:
            q = await ctx.guild.create_category("Questions")

        private_channel = await ctx.guild.create_text_channel("Private:{u}", category=q)

        await private_channel.send(f"{user} asked: {question}")

        await ctx.message.delete()

    #TESTING COMMANDS-------------------------------------------------------------------------------
    @bot.command()
    async def wipe(ctx):
        guild = ctx.guild
        for channel in guild.channels:
            await channel.delete()

        await guild.create_text_channel("testing")

    @bot.command()
    async def removeRoles(ctx):
        safeRoles = ["Developer", "@everyone", "Classroom", "ClassroomTest 2", "ClassroomTest 1"]
        guild = ctx.guild
        for role in guild.roles:
            if role.name not in safeRoles:
                print("Deleting role: ", role.name)
                await role.delete()
        await ctx.send('All roles removed')

    @bot.command()
    async def removeSections(ctx):
        safeRoles = ["Developer", "@everyone", "Classroom", "ClassroomTest 2", "ClassroomTest 1",
                     "Educator", "Assistant", "Student"]
        guild = ctx.guild
        for role in guild.roles:
            if role.name not in safeRoles:
                print("Deleting role: ", role.name)
                await role.delete()
        await ctx.send('All roles removed')

    @bot.command()
    async def reset(ctx):
        guild = ctx.guild
        for channel in guild.channels:
            if channel.name != 'testing':
                await channel.delete()
        await removeRoles(ctx)
        await on_guild_join(ctx.guild)

    @bot.command()
    async def testInsert(ctx, arg1, arg2):
        list = {'student_name': arg1, 'grade': arg2}
        data = supabase.table("TestTable").insert(list).execute()
        print(data)
        await ctx.channel.send("Inserted new student")

    @bot.command()
    async def test(ctx):
        print("Test")
        await ctx.channel.send("Test")

    bot.run(DISCORD_TOKEN)
