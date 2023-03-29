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
import utils
import create_quiz
import create_quiz, create_assignment, create_discussion
import openai
from create_classes import Assignment, Grade

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

        # Create server categories
        upcoming = await guild.create_category("Upcoming")
        general = await guild.create_category("General")
        await guild.create_category("Assignments")
        await guild.create_category("Quizzes")
        await guild.create_category("Discussions")
        await guild.create_category("Submissions")
        questions = await guild.create_category("Questions")

        # Create server channels
        await guild.create_text_channel("General", category=general)
        await guild.create_text_channel("Announcements", category=general)
        await guild.create_text_channel("Lounge", category=general)
        await guild.create_text_channel("Syllabus", category=general)
        await guild.create_text_channel("Public", category=questions)
        roles = await guild.create_text_channel("Roles", category=general)
        await roles.set_permissions(everyone, read_messages=True, send_messages=False)


        # Add classroom and educator to database
        await api.create_classroom(id=guild.id, name=guild.name)
        await utils.add_member_to_table(guild_id=guild.id, role='Educator', nickname=guild.owner.nick, did=guild.owner.id)

    #Gives new users the Student role
    @bot.event
    async def on_member_join(member):
        role = discord.utils.get(member.guild.roles, name="Student")
        await member.add_roles(role)
        discordNickname = member.display_name
        discordId = member.id
        await utils.add_member_to_table(guild_id=member.guild.id, role="Student", nickname=discordNickname, did=discordId)
        
    @bot.event 
    async def on_member_remove(member):
        userId = member.id
        supabase.table("User").delete().eq("discordId", userId).execute()

    @bot.event
    async def on_member_update(before, after):
        # Update member nickname in database
        if before.nick != after.nick:
            await api.update_member_nick(after.nick, str(after.id))

        # Update member role in database
        if before.role != after.role:
            id = await api.get_member_id(after.discord_id).get('id')
            server_id = str(after.guild.id)
            classroom_id = await api.get_classroom_id(server_id)
            await api.update_member_role(after.role, id, classroom_id)
            
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

    @bot.slash_command(name='poll',
                       description='```/poll [topic] [option1] [option2] ... [option8]``` - Creates a poll for users (8 max options)')
    async def poll(ctx: discord.ApplicationContext, topic: str, option1: str, option2: str, option3: str = None,
                   option4: str = None, option5: str = None, option6: str = None, option7: str = None,
                   option8: str = None):

        await ctx.defer()

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

        num_reactions_for_option_idx = [0] * len(options)

        #box area created for reactions
        boxes = []
        for i in range(10):
            boxes.append("⬛")
        boxesStr = ''.join(boxes)

        # Create the poll embed
        embed = discord.Embed(title=topic, description=' '.join(
            [f'{chr(0x1f1e6 + i)} {option}\n `{boxesStr}` {0} (0%)\n' for i, option in enumerate(options)]))

        await ctx.respond("Poll Created")

        # Send the poll message and add reactions
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(chr(0x1f1e6 + i))

        num_total_reactions = [0]

        async def update_poll_data(change_to_reactions, num_total_reactions, reaction):
            num_total_reactions[0] += change_to_reactions
            print(f"{num_total_reactions[0]} users reacted to the message")

            new_description_for_option_idx = [None] * len(options)
            for i in range(len(options)):
                # If the reaction emoji corresponds to options[i],
                # update num_reactions_for_option_idx[i]
                if reaction.emoji == chr(127462 + i):
                    num_reactions_for_option_idx[i] += change_to_reactions

                print(f"option{i + 1} reaction total: {num_reactions_for_option_idx[i]}")  
                reactionPercentage = round((num_reactions_for_option_idx[i] / num_total_reactions[0]) * 100) if num_total_reactions[0] > 0 else 0
                print(f"option{i + 1}%: {reactionPercentage}")

                boxesForOption = boxes.copy()
                for j in range(round(reactionPercentage / 10)):
                    if i < 7:
                        boxesForOption[j] = f"{chr(0x1F7E5+i)}"
                    else:
                        boxesForOption[j] = f"{chr(0x2B1C)}"
                boxesForOptionStr = ''.join(boxesForOption)
                
                new_description_for_option_idx[i] = f'{chr(0x1f1e6 + i)} {options[i]}\n `{boxesForOptionStr}` {num_reactions_for_option_idx[i]} ({reactionPercentage}%)\n'

            embed.description = ' '.join(new_description_for_option_idx)
            await message.edit(embed=embed)

        # check that the reaction is from a user, not a bot
        def check(reaction, user):
            return user != bot.user and reaction.message.id == message.id and str(reaction.emoji) in [
                chr(127462 + i) for i in range(len(options))]
        
        async def on_reaction_add(reaction, user):
            if check(reaction, user):
                await update_poll_data(1, num_total_reactions, reaction)

        async def on_reaction_remove(reaction, user):
            await update_poll_data(-1, num_total_reactions, reaction)

        #bot waits for reaction event from user
        bot.add_listener(on_reaction_add, 'on_reaction_add')
        bot.add_listener(on_reaction_remove, 'on_reaction_remove')

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
        if 'Educator' in user_roles or 'Assistant' in user_roles:
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
            classroom_id = await api.get_classroom_id(str(guild_id))
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
            user_mention = ctx.author.mention
            student_id = str(ctx.author.id)
            q = discord.utils.get(ctx.guild.categories, name="Questions")
            if q is None:
                q = await ctx.guild.create_category("Questions")

            channels = q.channels

            for channel in channels:
                if channel.name == f"private-{student_id}":
                    await ctx.respond(f"{user_mention} You already have a private question open.", delete_after=3)
                    return

            private_role = await ctx.guild.create_role(name=f"{student_id}")

            await ctx.author.add_roles(private_role)

            all_roles = ctx.guild.roles

            ow = {}

            for role in all_roles:
                ow[role] = discord.PermissionOverwrite(read_messages=False)

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                private_role: discord.PermissionOverwrite(read_messages=True),
                discord.utils.get(ctx.guild.roles, name="Educator"): discord.PermissionOverwrite(read_messages=True),
                discord.utils.get(ctx.guild.roles, name="Assistant"): discord.PermissionOverwrite(read_messages=True)
            }

            ow.update(overwrites)

            private_channel = await ctx.guild.create_text_channel(f"Private-{student_id}", category=q, overwrites=ow)

            await ctx.respond("Private question created", delete_after=3)

            await private_channel.send(f"{user_mention} asked: {question}")
        else:
            await ctx.respond("Only Students can ask private questions")

    @bot.slash_command(name='close', description='```/close``` deletes a private question channel')
    async def close(ctx: discord.ApplicationContext):
        channel_name = ctx.channel.name
        category = ctx.channel.category.name
        if category == "Questions" and 'private' in channel_name:
            embed = discord.Embed(title="Close this question?", color=0x00FF00)
            embed.add_field(name="Are you sure you want to close this question?", value="✅ Yes\n❌ No")
            interaction: discord.Interaction = await ctx.respond(embed=embed)
            message: discord.Message = await interaction.original_response()
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            def check(reaction, user):
                return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["✅", "❌"]

            while True:
                reaction, user = await bot.wait_for('reaction_add', check=check)

                # Assign role to user who reacted
                if reaction.emoji == "✅":
                    student_id = ctx.channel.name.split("-")[1]
                    created_role = discord.utils.get(ctx.guild.roles, name=f"{student_id}")
                    await created_role.delete()
                    await ctx.channel.delete(reason=f"Closed by {ctx.author.display_name}")
                if reaction.emoji == "❌":
                    await message.delete()
        else:
            await ctx.respond("You cannot close this channel", delete_after=3)


    @bot.slash_command(name='help', description='```/help``` sends command information to the user')
    async def help(ctx, command_name: str = None):
        if command_name:
            command = bot.get_application_command(command_name)
            if not command:
                await ctx.respond(f"There exists no command named '{command_name}'.")
                return
            await ctx.respond(f"**{command_name}:**\n{command.description}")
        else:
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

    @create.command(name='discussion',
                       description='Creates a new text channel with a prompt for discussion')
    async def discussion(ctx: discord.ApplicationContext):
        modal = create_discussion.create_discussion(bot=bot)
        await ctx.send_modal(modal)

    @create.command(name='assignment',
                       description='```/assignment [start_date] [due_date] [points] (pdf)``` - Creates assignments for students')
    async def assignment(ctx: discord.ApplicationContext, file: discord.Attachment = None):
        modal = create_assignment.create_assignment(bot=bot, file=file)
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
            {"role": "user", "content": f"Give me a {grade} grade quiz on {subject} with 5 questions in less than 150 words, hiding the answers"}
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=150)

        reply = chat.choices[0].message.content

        user = ctx.author

        await ctx.respond("Check DMs", delete_after=3)
        await user.send(f"TutorGPT: {reply}")

        messages.append({"role": "assistant", "content": reply})

        def check(message):
            return message.author == user and message.channel == user.dm_channel

        response = await bot.wait_for('message', check=check)

        content = response.content
        content += "\nNow show me the answers without repeating the questions."

        messages.append(
            {"role": "user", "content": content}
        )

        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=150)
        reply = chat.choices[0].message.content

        await user.send(f"TutorGPT: {reply}")

        messages.append({"role": "assistant", "content": reply})

    async def get_dates_assignments(server_id : str, due_date: str):
        response = supabase.table("Assignment").select('*').lte('dueDate', due_date).execute()
        all_assignments = response.data
        classroom_assignments = []
        for assignment in all_assignments:
            channel = bot.get_channel(int(assignment['channelId']))
            if channel is not None:
                if str(channel.guild.id) == str(server_id):
                    classroom_assignments.append(assignment)
        return classroom_assignments

    async def get_dates_quiz(server_id : str, due_date:str):
        response = supabase.table("Quiz").select('*').lte('dueDate', due_date).execute()
        all_quizzes = response.data
        classroom_quizzes = []
        for quiz in all_quizzes:
            channel = bot.get_channel(int(quiz['channelId']))
            if channel is not None:
                if str(channel.guild.id) == str(server_id):
                    classroom_quizzes.append(quiz)
        return classroom_quizzes

    async def get_dates_discussion(server_id: str, due_date: str):
        response = supabase.table("Discussion").select('*').lte('dueDate', due_date).execute()
        all_discussions = response.data
        classroom_discussions = []
        for disc in all_discussions:
            channel = bot.get_channel(int(disc['channelId']))
            if channel is not None:
                if str(channel.guild.id) == str(server_id):
                    classroom_discussions.append(disc)
        return classroom_discussions
    
    #clears specific category of all channels
    async def clear_upcoming(category: discord.CategoryChannel):
        for channel in category.channels:
            await channel.delete()
    
    #function to lock, but keep visible
    async def lock_but_keep_vis(ctx : discord.ApplicationContext, category):
        student_role = discord.utils.get(ctx.guild.roles, name="Student")
        assistant_role = discord.utils.get(ctx.guild.roles, name="Assistant")
        educator_role = discord.utils.get(ctx.guild.roles, name="Assistant")

        await category.set_permissions(ctx.guild.default_role, connect=False, view_channel=True)
        await category.set_permissions(student_role, connect=False, view_channel=True)
        await category.set_permissions(assistant_role, connect=False, view_channel=True)
        await category.set_permissions(educator_role, connect=False, view_channel=True)
        await category.set_permissions(ctx.guild.owner, connect=False, view_channel=True)

           
    
    #update slash command
    @bot.slash_command(
        name = 'upcoming',
        description = "Updates the 'Upcoming' category to show all schoolwork due before the end date")
    async def update_upcoming(ctx: discord.ApplicationContext,
                              end_date: discord.Option(str, description= "End date in the format YYYY-MM-DD") = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')):

        await ctx.defer()

        category = discord.utils.get(ctx.guild.categories, name='Upcoming')
        if category is None:
            category = await ctx.guild.create_category("Upcoming")

        #clears the current category so that it does not get bloated
        await clear_upcoming(category)

        #runs the get assignment data function
        assignment_date_data = await get_dates_assignments(str(ctx.guild_id), end_date)

        #runs the get date data for quizzes
        quiz_date_data = await get_dates_quiz(str(ctx.guild_id), end_date)

        discussion_date_data = await get_dates_discussion(str(ctx.guild_id), end_date)

         #iterates through all dates collected for quizzes
        for item in quiz_date_data:
            channel_name = str(item['title'])
            points = str(item['points'])

            await ctx.guild.create_voice_channel(
                name = f"❓| {points} Pts. | {channel_name}",
                category = category
            )
        
        #iterates through all dates collected for assignments
        for item in assignment_date_data:
            channel_name = str(item['title'])
            points = str(item['points'])

            await ctx.guild.create_voice_channel(
                name = f"📝| {points} Pts. | {channel_name}",
                category = category
            )

        for item in discussion_date_data:
            channel_name = str(item['title'])
            points = str(item['points'])

            await ctx.guild.create_voice_channel(
                name=f"💬| {points} Pts. | {channel_name}",
                category=category
            )
        
        #adds the icon for the channels
        await lock_but_keep_vis(ctx, category)

        await ctx.respond(f"Upcoming category updated")
    
    @bot.slash_command(name='grade',
                        description='```/grade [discord_id] [task_id] [score]``` - post grades for a student')
    async def grade(ctx: discord.ApplicationContext, discord_id: str, task_id: int, score: int):
        if ctx.author.id != ctx.guild.owner_id:
            await ctx.send("Error")
            return
        studentId_dict = await api.get_member_id(discord_id)
        studentId = studentId_dict["id"]


        grade_dict = {'graderId': studentId, 'taskId': task_id, 'studentId': studentId, 'score': score}
        new_grade = Grade(graderId=grade_dict['graderId'], taskId=grade_dict['taskId'],
                         studentId=grade_dict['studentId'], score=grade_dict['score'] )
        
        #post grade update
        await api.update_grade(new_grade)


        #send grade updated to the student
        student_grade = await api.get_grades(studentId)

        student = bot.get_user(int(discord_id))
        if student is None:
            # Handle the case where the student is not found
            await ctx.channel.send("Could not find the student's Discord user.")
        else:
            # Send the grades to the student's "grades" channel
            channel_name = student.name + "-grades"
            channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
            if channel is None:
                # Create a new text channel for the student
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    student: discord.PermissionOverwrite(read_messages=True)
                }
                channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)


            quiz_scores = []
            assignment_scores = []
            quiz_weight = 0.15 #quiz weight
            assignment_weight = 0.20 
            quiz_weighted_score = 0
            assignment_weighted_score = 0
            # Loop through the list of grades and separate quiz scores and assignment scores
            for grade in student_grade:
                if grade['type'] == 'Quiz':
                    quiz_scores.append(grade['score'])
                elif grade['type'] == 'Assignment':
                    assignment_scores.append(grade['score'])
            if len(quiz_scores) >= 1:
            # Calculate the weighted average of quiz scores
                quiz_weighted_avg = sum(quiz_scores) / sum([g['points'] for g in student_grade if g['type'] == 'Quiz'])
                quiz_weighted_score = quiz_weighted_avg * quiz_weight
            if len(assignment_scores) >= 1:
            # Calculate the weighted average of assignment scores
                assignment_weighted_avg = sum(assignment_scores) / sum([g['points'] for g in student_grade if g['type'] == 'Assignment'])
                assignment_weighted_score = assignment_weighted_avg * assignment_weight

            # Calculate the overall grade
            overall_grade = (quiz_weighted_score + assignment_weighted_score) / (quiz_weight + assignment_weight)
            overall_grade = format(overall_grade, '.2f')

            grade_string = ""
            for grade in student_grade:
                grade_string += f"{grade['type']} - {grade['title']}: {grade['score']}/{grade['points']}\n"

            grade_string+=f"overall grade - {overall_grade}"
            # Send the grades to the student's new channel
            await channel.send(f"Here are your grades, recalculated:\n{grade_string}")
            await ctx.respond("posted grade!")

        

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
