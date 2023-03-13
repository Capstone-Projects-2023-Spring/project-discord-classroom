import asyncio
from http import client
import discord
import json
import os
from supabase import create_client, Client
from discord.ext import commands
from typing import Optional, List
import io
import datetime
from PyPDF2 import PdfReader
import api
import create_commands

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

    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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
        # gives discord owner the Educator role
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

    def add_member_to_table(role, nickname, did):
        supabase.table(role).insert({ "name": nickname, "discordId": did }).execute()

    #Gives new users the Student role
    @bot.event
    async def on_member_join(member):
        print(f'on_member_join() called!')
        role = discord.utils.get(member.guild.roles, name="Student")
        await member.add_roles(role)
        print(role)
        discordNickname = member.display_name
        print(discordNickname)
        discordId = member.id
        print(discordId)
        add_member_to_table(role, discordNickname, discordId)
        
    @bot.event 
    async def on_member_remove(member):
        userId = member.id
        supabase.table("Student").delete().eq("discordId", userId).execute()

    @bot.event
    async def on_member_update(before, after):
        id = after.id
        print(id)
        if before.nick != after.nick:
            try:
                response = supabase.table('Student').update({'name': after.nick}).eq('discordId', str(after.id)).execute()
                print(f"Nickname updated for {after.name}")
                
            except Exception:
                print("Unable to update user")
            
    @bot.event
    async def on_guild_channel_create(channel):
        # Add guild to Classroom table
        pass

    @bot.event
    async def on_guild_channel_delete(channel):
        # Remove guild from Classroom table
        pass

    @bot.slash_command(name='syllabus',

                       description='attach pdf file to command',
                       help='!syllabus [attach .pdf file] - Creates a syllabus text channel with the .pdf as a message for students to download and view the syllabus. Library to view syllabus contents on discord.')
    async def syllabus(ctx: discord.ApplicationContext, file: discord.Attachment):
        if ctx.author.id != ctx.guild.owner_id:
            await ctx.send("Error, enter '!help' for  more information.")
            return
        owner = ctx.guild.owner
        # restrict syllabus channel but allow for visibility.
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
            owner: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        await ctx.respond("Success", delete_after=0)

        if file is not None:
            pdf = file
            if pdf.filename.endswith(".pdf"):
                file_data = await pdf.read()
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
                # append and exclude unicodeerror
                chunks = [text_bytes[i:i + max_char].decode('utf-8', errors='ignore') for i in
                          range(0, len(text_bytes), max_char)]

                # send text representation of syllabus to syllabus channel
                for chunk in chunks:
                    await channel.send("```" + chunk + "```")
                await channel.send(
                    "**```diff\n- Please note, the text representation of the syllabus may not be completely accurate. For a more precise version, download syllabus provided below.```**")

                # Send PDF "syllabus" channel
                await channel.send(file=discord.File(io.BytesIO(file_data), filename=pdf.filename))
                await ctx.send("Syllabus uploaded successfully.")

            else:
                await ctx.send("Invalid file format, only PDF files are accepted.")

    @bot.slash_command(name ='discussion',
                       description='Creates a new text channel with a prompt for discussion',
                       help='!poll [channel name] [prompt]')
    async def discussion_create(ctx: discord.ApplicationContext, channel_name: str, prompt: str):
        # Verify existence of 'Discussion' category, or create it if it does not exist
        if discord.utils.get(ctx.guild.categories, name='Discussion'):
            category = discord.utils.get(ctx.guild.categories, name='Discussion')
        else:
            category = await ctx.guild.create_category('Discussion')

        # Create new channel for discussion
        channel = await ctx.guild.create_text_channel(name=channel_name, category=category)
        
        # Send discussion prompt to new channel
        embed = discord.Embed(title=channel_name, description=prompt)
        await channel.send(embed=embed)
        await ctx.respond('Discussion channel created.')

        return channel

    @bot.slash_command(name='poll',
                       description="creates poll (max 8 options)",
                       help='!poll [prompt] [option 1] [option 2] *[option 3] ... [*option n] - Creates a poll where students vote through reactions.')
    async def poll(ctx: discord.ApplicationContext, topic: str, option1: str, option2: str, option3: str = None,
                   option4: str = None, option5: str = None, option6: str = None, option7: str = None,
                   option8: str = None):

        options = [option1, option2]
        if option3:
            options.append(option3)
        if option4:
            options.append(option4)
        if option5:
            options.append(option5)
        if option6:
            options.append(option6)
        if option7:
            options.append(option7)
        if option8:
            options.append(option8)

        # Create the poll embed
        embed = discord.Embed(title=topic, description=' '.join(
            [f'{chr(0x1f1e6 + i)} {option}\n' for i, option in enumerate(options)]))

        await ctx.respond("Poll Created")

        # Send the poll message and add reactions
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(chr(0x1f1e6 + i))

    async def increment_attendance(discordId:str):
        student = await supabase.from_table('Student').select().eq('discord_id', discord_id).single().execute()
        student_attendance = student['attendance'] + 1
        await supabase.from_table('Student').update({'attendance_count': attendance_count}).eq('discord_id', discord_id).execute()

    @bot.slash_command(
        name='attendance',
        description='take attendance',
        help='!attendance - Creates a simple poll with one option prompting user to react to prove they are attending the class. ')
    async def attendance(ctx: discord.ApplicationContext, time: float = 5):
        user_roles = [role.name for role in ctx.author.roles]
        if  'Educator' in user_roles or 'Assistant' in user_roles:
            await ctx.respond("Now taking Attendance...")
            date = datetime.datetime.now().strftime("%m - %d - %y %I:%M %p")
            student_role = discord.utils.get(ctx.guild.roles, name="Student")
            embed = discord.Embed(title="Attendance", description=f'{student_role.mention} React to this message to check into today\'s attendance')
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            timeLeft = time * 60
            while timeLeft >= 0:
                embed.title = f"Attendance - {int(timeLeft)}s"
                await asyncio.sleep(1)
                await message.edit(embed=embed)
                timeLeft -= 1
            embed.description = "Attendance CLOSED"
            await asyncio.sleep(1)
            await message.edit(embed=embed)
            attendance_message = await ctx.channel.fetch_message(message.id)
            reactions = attendance_message.reactions
            users = []
            for r in reactions:
                if r.emoji == '✅':
                    async for user in r.users():
                        users.append(user)
                        await increment_attendance(str(user.id))
            users = [user.nick for user in users if not user.bot]

            response = f"Attendance for {date}:\n" + '\n'.join(users)
            await ctx.author.send(response)
        else:
            student = await supabase.from_table('Student').select().eq('discordId', str(ctx.author.id)).single().execute()
            attendance = student['attendance']
            response = f"Your attendance count is {attendance}."
            await ctx.author.send(response)

    @bot.slash_command(name='ta',
                       description='Gives the user the assistant role',
                       help='!ta @user - Gives the user the assistant role')
    async def ta(ctx: discord.ApplicationContext, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Assistant")
        await user.add_roles(role)
        await ctx.respond(f"{user.mention} has been given the Assistant role")

    @bot.slash_command(name='edu',
                       description='Gives the user the Educator role',
                       help='!edu @user - Gives the user the educator role')
    async def edu(ctx: discord.ApplicationContext, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Educator")
        await user.add_roles(role)
        await ctx.respond(f"{user.mention} has been given the Educator role")

    @bot.slash_command(name='section',
                       description='Creates sections for students to join',
                       help='!section [prompt] [role1] *[option 2] ... *[option n] - Creates a roles for each section of the class.')
    @commands.has_role("Educator")
    async def section(ctx: discord.ApplicationContext, section_1: str, section_2: str=None, section_3: str=None,
                      section_4: str=None, section_5: str=None, section_6: str=None):
        # Create roles for each section
        options = [section_1]
        if section_2:
            options.append(section_2)
        if section_3:
            options.append(section_3)
        if section_4:
            options.append(section_4)
        if section_5:
            options.append(section_5)
        if section_6:
            options.append(section_6)

        msg = ""
        for i in range(len(options)):
            await ctx.guild.create_role(name=options[i])
            msg += f"{options[i]} "

        await ctx.respond(f"Sections {msg}created.")

        # Create reaction role embed
        embed = discord.Embed(title="React to this message to join your section.", color=0x00FF00)

        for i, option in enumerate(options):
            embed.add_field(name=f"{chr(127462 + i)} Section {option}", value="\u200b", inline=False)

        channel = discord.utils.get(ctx.guild.channels, name="roles")
        poll_message = await channel.send(embed=embed)

        # Add reactions to embed message
        for i in range(len(options)):
            await poll_message.add_reaction(chr(127462 + i))

        # Wait for reactions from users
        def check(reaction, user):
            return user != bot.user and reaction.message.id == poll_message.id and str(reaction.emoji) in [
                chr(127462 + i) for i in range(len(options))]

        while True:
            reaction, user = await bot.wait_for('reaction_add', check=check)

            # Assign role to user who reacted
            for i in range(len(options)):
                if reaction.emoji == chr(127462 + i):
                    role = discord.utils.get(ctx.guild.roles, name=options[i])
                    await user.add_roles(role)
                    await channel.send(f'{user.mention} has been assigned to Section {role.name}.')

    @bot.slash_command(name='private',
                       description='creates private channel for the question',
                       help=' /private - Creates a private text-channel between the student and teacher')
    @commands.has_role("Student")
    async def private(ctx: discord.ApplicationContext, question: str):
        user = ctx.author.mention
        u = ctx.author.nick
        response = user
        q = discord.utils.get(ctx.guild.categories, name="Questions")
        if q is None:
            q = await ctx.guild.create_category("Questions")
        private_channel = await ctx.guild.create_text_channel(f"Private-{u}", category=q)

        await ctx.respond("Private question created", delete_after=3)

        await private_channel.send(f"{user} asked: {question}")

    create = bot.create_group("create", "create school work")

    @create.command(name='quiz',
                    description='creates a quiz (date format: yyyy-mm-dd)',
                    help='creates a quiz for students to take')
    async def quiz(ctx, questions: discord.Attachment = None):

        modal = create_commands.create_quiz(bot=bot)
        await ctx.send_modal(modal)

    # TESTING COMMANDS-------------------------------------------------------------------------------
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
