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
import create_quiz
import openai
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

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
    GPT_KEY = configData["GPTKey"]

    supabase: Client = create_client(SB_URL, SB_KEY)

    openai.api_key = GPT_KEY
    messages = [
        {"role": "system", "content": "You are TutorGPT, a friendly and helpful AI that assists students with learning and understanding their school work."}
    ]

    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        bot.add_view(create_quiz.StartQuiz())

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

        upcoming = await guild.create_category("Upcoming")
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
        await api.create_classroom(id=guild.id, name=guild.name)

    async def add_member_to_table(guild_id, role, nickname, did):
        print(guild_id, role, nickname, did)
        if role == "Student":
            print("Student")
            response = supabase.table("User").insert({ "name": nickname, "discordId": did, "attendance": 0 }).execute()
            user_id = response.data[0]['id']
            print(user_id)
            classroom_id = await api.get_classroom_id(guild_id)
            supabase.table("Classroom_User").insert({ "classroomId": classroom_id['id'], 'userId': user_id, 'role': "Student"}).execute()
        else:
            print("Not Student")
            response = supabase.table("User").insert({"name": nickname, "discordId": did}).execute()
            user_id = response.data[0]['id']
            classroom_id = await api.get_classroom_id(guild_id)
            supabase.table("Classroom_User").insert({"classroomId": classroom_id['id'], 'userId': user_id, 'role': "Educator"}).execute()

    #Gives new users the Student role
    @bot.event
    async def on_member_join(member):
        role = discord.utils.get(member.guild.roles, name="Student")
        await member.add_roles(role)
        discordNickname = member.display_name
        discordId = member.id
        await add_member_to_table(guild_id=member.guild.id, role="Student", nickname=discordNickname, did=discordId)
        
    @bot.event 
    async def on_member_remove(member):
        userId = member.id
        supabase.table("User").delete().eq("discordId", userId).execute()

    @bot.event
    async def on_member_update(before, after):
        # Here we should update the Database User's Role
        if before.nick != after.nick:
            try:
                response = supabase.table('User').update({'name': after.nick}).eq('discordId', str(after.id)).execute()
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
                       description='```/syllabus [.pdf file]``` - Updates the syllabus page with the linked pdf file')
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
                       description='Creates a new text channel with a prompt for discussion')
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
                       description='```/poll [topic] [option1] [option2] ... [option8]``` - Creates a poll for users (8 max options)')
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

    async def increment_attendance(discord_id:str):
        student = supabase.table('User').select().eq('discord_id', discord_id).single().execute()
        student_attendance = student.data['attendance'] + 1
        supabase.table('User').update({'attendance': student_attendance}).eq('discordId', discord_id).execute()

    @bot.slash_command(
        name='attendance',
        description='```/attendance [time (minutes)]``` - Creates attendance poll')
    @commands.has_any_role("Educator", "Assistant")
    async def attendance(ctx: discord.ApplicationContext, time: float = 5):
        user_roles = [role.name for role in ctx.author.roles]
        guild_id = ctx.guild_id
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
            attended = []
            for user in users:
                if not user.bot:
                    if user.nick is not None:
                        attended.append(user.nick)
                    else:
                        attended.append(user.name)

            response = f"Attendance for {date}:\n\nAttended:\n" + '\n'.join(attended)

            students = discord.utils.get(ctx.guild.roles, name="Student").members

            absent = []

            for student in students:
                if student not in users:
                    if student.nick is not None:
                        absent.append(student.nick)
                    else:
                        absent.append(student.name)

            response += "\n\nAbsent:\n" + '\n'.join(absent)
            await ctx.author.send(response)

            # Update the 'total attendance' in the Supabase table
            classroom_table = supabase.table('Classroom')
            classroom_id = await api.get_classroom_id(guild_id)
            _, error = await classroom_table.update({'total_attendance': supabase.sql('total_attendance + 1')}).single().where('class_id', '=', classroom_id).execute()
            if error:
                print(f"Error updating total attendance: {error}")

        else:
            student = supabase.table('User').select().eq('discordId', str(ctx.author.id)).single().execute()
            attendance = student.data['attendance']
            response = f"Your attendance count is {attendance}."
            await ctx.author.send(response)
        

    @bot.slash_command(name='ta',
                       description='```/ta [user]``` - Gives/Removes the user the Assistant role')
    async def ta(ctx: discord.ApplicationContext, user: discord.Member):
        edu_role = discord.utils.get(ctx.guild.roles, name="Educator")
        if edu_role in ctx.author.roles:
            role = discord.utils.get(ctx.guild.roles, name="Assistant")
            if role in user.roles:
                await user.remove_roles(role)
                await ctx.respond(f"Removed Assistant role from {user.mention}")
            else:
                await user.add_roles(role)
                await ctx.respond(f"{user.mention} has been given the Assistant role")
        else:
            await ctx.respond("You need the Educator role to use this command")

    @bot.slash_command(name='edu',
                       description='```/edu [user]``` - Gives/Removes the user the Educator role')
    async def edu(ctx: discord.ApplicationContext, user: discord.Member):
        edu_role = discord.utils.get(ctx.guild.roles, name="Educator")
        if edu_role in ctx.author.roles:
            if user == ctx.guild.owner:
                return await ctx.respond("You cannot remove the Educator role from the owner")
            if edu_role in user.roles:
                await user.remove_roles(edu_role)
                await ctx.respond(f"Removed Educator role from {user.mention}")
            else:
                await user.add_roles(edu_role)
                await ctx.respond(f"{user.mention} has been given the Educator role")
        else:
            await ctx.respond("You need the Educator role to use this command")

    # @bot.slash_command(name='section',
    #                    description='```/section [section1] ... [section6]``` - Allows users to assign themselves to a specific section')
    # @commands.has_role("Educator")
    # async def section(ctx: discord.ApplicationContext, section_1: str, section_2: str=None, section_3: str=None,
    #                   section_4: str=None, section_5: str=None, section_6: str=None):
    #     # Create roles for each section
    #     options = [section_1]
    #     if section_2:
    #         options.append(section_2)
    #     if section_3:
    #         options.append(section_3)
    #     if section_4:
    #         options.append(section_4)
    #     if section_5:
    #         options.append(section_5)
    #     if section_6:
    #         options.append(section_6)
    #
    #     msg = ""
    #     for i in range(len(options)):
    #         await ctx.guild.create_role(name=options[i])
    #         msg += f"{options[i]} "
    #
    #     await ctx.respond(f"Sections {msg}created.")
    #
    #     # Create reaction role embed
    #     embed = discord.Embed(title="React to this message to join your section.", color=0x00FF00)
    #
    #     for i, option in enumerate(options):
    #         embed.add_field(name=f"{chr(127462 + i)} Section {option}", value="\u200b", inline=False)
    #
    #     channel = discord.utils.get(ctx.guild.channels, name="roles")
    #     poll_message = await channel.send(embed=embed)
    #
    #     # Add reactions to embed message
    #     for i in range(len(options)):
    #         await poll_message.add_reaction(chr(127462 + i))
    #
    #     # Wait for reactions from users
    #     def check(reaction, user):
    #         return user != bot.user and reaction.message.id == poll_message.id and str(reaction.emoji) in [
    #             chr(127462 + i) for i in range(len(options))]
    #
    #     while True:
    #         reaction, user = await bot.wait_for('reaction_add', check=check)
    #
    #         # Assign role to user who reacted
    #         for i in range(len(options)):
    #             if reaction.emoji == chr(127462 + i):
    #                 role = discord.utils.get(ctx.guild.roles, name=options[i])
    #                 await user.add_roles(role)
    #                 await channel.send(f'{user.mention} has been assigned to Section {role.name}.')

    @bot.slash_command(name='private',
                       description='```/private [question]``` - Creates a private question between Student and Educator/TA')
    async def private(ctx: discord.ApplicationContext, question: str):
        student_role = discord.utils.get(ctx.guild.roles, name="Student")
        if student_role in ctx.author.roles:
            user = ctx.author.mention
            u = ctx.author.nick
            response = user
            q = discord.utils.get(ctx.guild.categories, name="Questions")
            if q is None:
                q = await ctx.guild.create_category("Questions")
            if u is None:
                u = ctx.author
            private_channel = await ctx.guild.create_text_channel(f"Private-{u}", category=q)

            await ctx.respond("Private question created", delete_after=3)

            await private_channel.send(f"{user} asked: {question}")
        else:
            await ctx.respond("Only Students can ask private questions")

    @bot.slash_command(name='help', description='```/help``` sends command information to the user')
    async def help(ctx):
        message = "**Available Commands:**\n\n"
        for command in bot.application_commands:
            if command.name == "create":
                for create in command.walk_commands():
                    message += f"{create.description}\n\n"
            else:
                message += f"{command.description}\n\n"

        await ctx.author.send(message)

        await ctx.respond("Check Direct Messages for available commands")

    create = bot.create_group("create", "create school work")

    @create.command(name='quiz',
                    description='```/create quiz [questions.json]``` - Creates a Quiz for students to take')
    async def quiz(ctx, questions: discord.Attachment = None):

        modal = create_quiz.create_quiz(bot=bot)
        await ctx.send_modal(modal)

    @bot.slash_command(name='upload_file', description='```/upload file`` - User can follow link to upload file')
    async def upload_file(ctx):
        await ctx.respond('https://singular-jalebi-124a92.netlify.app/')

    tutor = bot.create_group("tutor", "AI tutor for students")

    @tutor.command(name='quiz', description='```/tutor quiz [subject] [grade]```')
    async def quiz(ctx: discord.ApplicationContext, subject: str, grade: str):
        nonlocal messages

        await ctx.defer()

        messages.append(
            {"role": "user", "content": f"Give me {grade} grade quiz on {subject} with 5 questions in less than 150 words, hiding the answers"}
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=100)

        reply = chat.choices[0].message.content

        await ctx.respond(f"TutorGPT: {reply}")

        # TODO: When student responds, their answers are checked for correctness


    #assignment update
    #goes through supabase and get data of specific dates
    async def get_dates(start_date: str, due_date: str):
        query = f"SELECT name, start_date, due_date FROM ASSIGNMENT WHERE due_date >= '{start_date}' AND due_date <= '{due_date}'"
        response = await supabase.raw(query)
        return response['data'] 
    
    #clears specific category of all channels
    async def clear_upcoming(category):
        for channel in category.channels:
            await channel.delete()
    
    #function to repace all voice channel icons with memo eoji
    async def add_memo_icon(category):
         # Create a new image for the memo icon with the memo emoji
        memo_emoji = chr(0x1F4DD)
        memo_icon = Image.new('RGBA', (128, 128), (255, 255, 255, 0))
        draw = ImageDraw.Draw(memo_icon)
        draw.text((0, 0), memo_emoji, fill=(255, 255, 255, 255))

        # Iterate over the voice channels in the category
        for channel in category.voice_channels:
            # Load the original channel icon image
            icon_bytes = await channel.icon.read()
            icon_image = Image.open(BytesIO(icon_bytes))

            # Add the memo icon to the original image
            icon_image.alpha_composite(memo_icon)

            # Convert the image to bytes and update the channel icon
            buffer = BytesIO()
            icon_image.save(buffer, format='PNG')
            buffer.seek(0)
            await channel.edit(icon=buffer)

    #update slash command
    @bot.slash_command(
        name = 'update',
        description = "Checks dates in database and updates the category with the upcoming assignments")
    async def update_upcoming(ctx: discord.ApplicationContext, 
                              start_date: discord.Option(str, description= "End date in the format YYYY-MM-DD"),
                              end_date: discord.Option(str, description= "End date in the format YYYY-MM-DD")):
        category = discord.utils.get(ctx.guild.categories, name = 'Upcoming')

        #clears the current category so that it does not get bloated
        clear_upcoming(category)

        #makes channel with the dates used
        new_channel = await ctx.guild.create_voice_channel(
            name = f"for {start_date} through {end_date}",
            category = category
        )
        
        #runs the get data function
        date_data = await get_dates(start_date, end_date)

        #iterates through all dates collected
        for item in date_data:
            channel_name = str(item['name'])

            new_channel = await ctx.guild.create_voice_channel(
                name = channel_name,
                category = category
            )

            await ctx.respond(f"Added new assignment to upcoming: {new_channel.name}")

        #adds the icon for the channels
        await add_memo_icon(category)

    # TESTING COMMANDS-------------------------------------------------------------------------------
    # @bot.command()
    # async def wipe(ctx):
    #     guild = ctx.guild
    #     for channel in guild.channels:
    #         await channel.delete()
    #
    #     await guild.create_text_channel("testing")
    #
    # @bot.command()
    # async def removeRoles(ctx):
    #     safeRoles = ["Developer", "@everyone", "Classroom", "ClassroomTest 2", "ClassroomTest 1"]
    #     guild = ctx.guild
    #     for role in guild.roles:
    #         if role.name not in safeRoles:
    #             print("Deleting role: ", role.name)
    #             await role.delete()
    #     await ctx.send('All roles removed')
    #
    # @bot.command()
    # async def removeSections(ctx):
    #     safeRoles = ["Developer", "@everyone", "Classroom", "ClassroomTest 2", "ClassroomTest 1",
    #                  "Educator", "Assistant", "Student"]
    #     guild = ctx.guild
    #     for role in guild.roles:
    #         if role.name not in safeRoles:
    #             print("Deleting role: ", role.name)
    #             await role.delete()
    #     await ctx.send('All roles removed')
    #
    # @bot.command()
    # async def reset(ctx):
    #     guild = ctx.guild
    #     for channel in guild.channels:
    #         if channel.name != 'testing':
    #             await channel.delete()
    #     await removeRoles(ctx)
    #     await on_guild_join(ctx.guild)
    #
    # @bot.command()
    # async def testInsert(ctx, arg1, arg2):
    #     list = {'student_name': arg1, 'grade': arg2}
    #     data = supabase.table("TestTable").insert(list).execute()
    #     print(data)
    #     await ctx.channel.send("Inserted new student")
    #
    # @bot.command()
    # async def test(ctx):
    #     print("Test")
    #     await ctx.channel.send("Test")

    bot.run(DISCORD_TOKEN)
