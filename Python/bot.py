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
        await guild.create_text_channel("Private", category=questions)

    # Gives new users the Student role
    @bot.event
    async def on_member_join(member):
        role = discord.utils.get(member.guild.roles, name="Student")
        await member.add_roles(role)

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

    @bot.slash_command(name='poll',
                       description="creates poll (max 8 options)",
                       help='!poll [prompt] [option 1] [option 2] *[option 3] ... [*option n] - Creates a poll where students vote through reactions.')
    async def poll(ctx: discord.ApplicationContext, topic: str, option1: str, option2: str, option3: str = None,
                   option4: str = None, option5: str = None, option6: str = None, option7: str = None,
                   option8: str = None):

        options = []
        if option1 != None:
            options.append(option1)
        if option2 != None:
            options.append(option2)
        if option3 != None:
            options.append(option3)
        if option4 != None:
            options.append(option4)
        if option5 != None:
            options.append(option5)
        if option6 != None:
            options.append(option6)
        if option7 != None:
            options.append(option7)
        if option8 != None:
            options.append(option8)

        # Create the poll embed
        embed = discord.Embed(title=topic, description=' '.join(
            [f'{chr(0x1f1e6 + i)} {option}\n' for i, option in enumerate(options)]))

        # Send the poll message and add reactions
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(chr(0x1f1e6 + i))

        await ctx.respond("Success", delete_after=0)

        return 1

    @bot.slash_command(
        name='attendance',
        description='take attendance',
        help='!attendance - Creates a simple poll with one option prompting user to react to prove they are attending the class. ')
    @commands.has_any_role("Educator", "Assistant")
    async def attendance(ctx: discord.ApplicationContext, time: float = 5):
        await ctx.respond("Success", delete_after=0)
        date = datetime.datetime.now().strftime("%m - %d - %y %I:%M %p")
        embed = discord.Embed(title="Attendance", description='React to this message to check into today\'s attendance')
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
        users = [user.nick for user in users if not user.bot]

        response = f"Attendance for {date}:\n" + '\n'.join(users)
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
                       help='!section [prompt] [option 1] *[option 2] ... *[option n] - Creates a roles for each section of the class.')
    @commands.has_role("Educator")
    async def section(ctx: discord.ApplicationContext, roles: str):
        # Create roles for each section
        options = roles.split()
        for i in range(len(options)):
            await ctx.guild.create_role(name=options[i])

        await ctx.respond("Success", delete_after=0)

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

        await ctx.respond("Success", delete_after=0)

        await private_channel.send(f"{user} asked: {question}")

    create = bot.create_group("create", "create school work")

    @create.command(name='quiz',
                    description='creates a quiz (date format: yyyy-mm-dd)',
                    help='creates a quiz for students to take')
    async def quiz(ctx, questions: discord.Attachment = None):

        class QuizModal(discord.ui.Modal):

            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                title = discord.ui.InputText(label="Title", style=discord.InputTextStyle.short,
                                             placeholder="ex: 'Parts of the Cell'", value="Test")
                points = discord.ui.InputText(label="Points", style=discord.InputTextStyle.short,
                                              placeholder="ex: '50'", value=20, required=False)
                start_date = discord.ui.InputText(label="Start Date", style=discord.InputTextStyle.short,
                                                  placeholder="ex: '2023-05-25'", value="2023-06-01")
                due_date = discord.ui.InputText(label="Due Date", style=discord.InputTextStyle.short,
                                                placeholder="ex: '2023-05-30'", value="2023-06-08")
                time_limit = discord.ui.InputText(label="Time Limit (minutes)", placeholder="ex: '30'",
                                                  style=discord.InputTextStyle.short, required=False)
                self.add_item(title)
                self.add_item(points)
                self.add_item(start_date)
                self.add_item(due_date)
                self.add_item(time_limit)

            async def callback(self, interaction: discord.Interaction):
                e = discord.Embed(title="Creating Quiz...")
                title = self.children[0].value
                if self.children[1].value != "":
                    try:
                        points = int(self.children[1].value)
                    except ValueError:
                        return await interaction.response.send_message("Invalid points")
                try:
                    start_date = datetime.datetime.strptime(self.children[2].value, "%Y-%m-%d").date()
                except ValueError:
                    return await interaction.response.send_message("Invalid start date format")
                try:
                    due_date = datetime.datetime.strptime(self.children[3].value, "%Y-%m-%d").date()
                except ValueError:
                    return await interaction.response.send_message("Invalid due date format")
                print(self.children[4].value)
                if self.children[4].value != "":
                    try:
                        time_limit = int(self.children[4].value)
                    except ValueError:
                        return await interaction.response.send_message("Invalid time limit")

                e.add_field(name="Title", value=title, inline=False)
                if self.children[1].value != "":
                    e.add_field(name="Points", value=str(points), inline=False)
                    even_points = 1
                else:
                    e.add_field(name="Points", value="TBD", inline=False)
                    even_points = 0
                e.add_field(name="Start Date", value=start_date.strftime('%B %d, %Y'), inline=False)
                e.add_field(name="Due Date", value=due_date.strftime('%B %d, %Y'), inline=False)
                if self.children[4].value != "":
                    e.add_field(name="Time Limit", value=str(time_limit), inline=False)
                else:
                    e.add_field(name="Time Limit", value="None", inline=False)
                e.add_field(name="Number of Questions", value="0", inline=False)
                e.add_field(name="Sections", value="None", inline=False)

                server = interaction.guild
                classroom_id = await api.get_classroom_id(server.id)
                response = await api.get_sections(classroom_id['id'])
                sections = []
                for r in response:
                    sections.append(r['name'])
                sec_str = ""
                for i, section in enumerate(sections):
                    sec_str += f'{chr(0x1f1e6 + i)} {section}\n'

                current_slide = e
                slides = [e]
                print("current slide set to e:", e)

                class QuestionModal(discord.ui.Modal):
                    def __init__(self, quiz_view, *args, **kwargs) -> None:
                        super().__init__(*args, **kwargs)
                        self.quiz_view = quiz_view
                        question = discord.ui.InputText(label="Question", style=discord.InputTextStyle.short,
                                                        placeholder="ex: 'Who was the first U.S. President?'",
                                                        value="2+2")
                        answer = discord.ui.InputText(label="Answer", style=discord.InputTextStyle.short,
                                                      placeholder="ex: 'George Washington'",
                                                      required=False, value="4")
                        wrong = discord.ui.InputText(label="Wrong Options", style=discord.InputTextStyle.short,
                                                     placeholder="ex: 'Ben Franklin, Thomas Jefferson, John Adams'",
                                                     required=False, value="5, 6, 7")
                        self.add_item(question)
                        self.add_item(answer)
                        self.add_item(wrong)
                        if even_points == 0:
                            ques_points = discord.ui.InputText(label="Points", style=discord.InputTextStyle.short,
                                                               placeholder="ex: '5'")
                            self.add_item(ques_points)

                    async def callback(self, interaction: discord.Interaction):
                        nonlocal current_slide
                        add_e = discord.Embed(title=f"Question {len(slides)}")
                        add_e.add_field(name="Question", value=self.children[0].value)
                        if self.children[1].value != "":
                            add_e.add_field(name="Answer", value=self.children[1].value)
                        else:
                            add_e.add_field(name="Answer", value="None")
                        if self.children[2].value != "":
                            add_e.add_field(name="Wrong Options", value=self.children[2].value)
                        else:
                            add_e.add_field(name="Wrong Options", value="None")
                        if even_points == 0:
                            add_e.add_field(name="Points", value=self.children[3].value)
                        else:
                            add_e.add_field(name="Points", value=str(points/len(slides)))
                        await interaction.response.edit_message(embed=add_e)
                        slides.append(add_e)
                        current_slide = add_e
                        await self.quiz_view.update_buttons(interaction)

                class EditModal(discord.ui.Modal):
                    def __init__(self, view, modal_embed: discord.Embed, *args, **kwargs) -> None:
                        super().__init__(*args, **kwargs)
                        self.quiz_view = view
                        self.modal_embed = modal_embed
                        self.quiz_edit = 1 if self.modal_embed.fields[0].name == "Title" else 0
                        new_its = []
                        for it in self.modal_embed.fields:
                            if even_points == 1 and it.name == "Points" and self.quiz_edit == 0:
                                continue
                            if (it.name == "Points" or it.name == "Time Limit") and self.quiz_edit == 1:
                                new_its.append(discord.ui.InputText(label=it.name, style=discord.InputTextStyle.short, value=it.value, required=False))
                            else:
                                new_its.append(discord.ui.InputText(label=it.name, style=discord.InputTextStyle.short, value=it.value))
                        for it in new_its:
                            if len(self.children) < 5:
                                self.add_item(it)

                    async def callback(self, interaction: discord.Interaction):
                        nonlocal current_slide
                        nonlocal even_points
                        nonlocal points
                        index = slides.index(self.modal_embed)
                        for i, field in enumerate(self.modal_embed.fields):
                            if i < len(self.children):
                                field.value = self.children[i].value

                        if self.quiz_edit == 1:
                            if self.children[1].value != "" and self.children[1].value != "TBD":
                                even_points = 1
                                try:
                                    points = int(self.children[1].value)
                                except ValueError:
                                    return await interaction.response.send_message("Invalid points")
                            else:
                                even_points = 0
                                points = None

                        current_slide = self.modal_embed
                        slides[index] = current_slide
                        await interaction.response.edit_message(embed=current_slide)
                        await self.quiz_view.update_buttons(interaction)


                class QuizView(discord.ui.View):
                    async def update_buttons(self, interaction2):
                        left = self.get_item("left")
                        right = self.get_item("right")
                        done = self.get_item("done")
                        trash = self.get_item("trash")
                        first = self.get_item("first")

                        if len(slides) > 1:
                            done.disabled = False
                        else:
                            done.disabled = True

                        if current_slide != slides[0]:
                            # Turns off left arrow if current embed is the first embed
                            first.disabled = False
                            left.disabled = False
                        else:
                            first.disabled = True
                            left.disabled = True

                        if current_slide != slides[len(slides) - 1]:
                            # Turns off right arrow if current embed is the last embed
                            right.disabled = False
                        else:
                            right.disabled = True

                        if current_slide != slides[0]:
                            trash.disabled = False
                        else:
                            trash.disabled = True

                        e.set_field_at(index=5, name="Number of Questions", value=str(len(slides) - 1), inline=False)
                        self.update_points()

                        await interaction2.followup.edit_message(embed=current_slide, message_id=interaction2.message.id, view=self)

                    def update_points(self):
                        total_points = 0
                        for i, slide in enumerate(slides):
                            if i != 0:
                                if even_points == 1:
                                    slide.set_field_at(3, name="Points", value=str(points/(len(slides) - 1)))
                                else:
                                    total_points += float(slide.fields[3].value)
                                slide.title = f"Question {i}"
                        if even_points == 0:
                            slides[0].fields[1].value = str(total_points)


                    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label="<<", disabled=True,
                                       custom_id="first")
                    async def first_button_callback(self, button, interaction):
                        nonlocal current_slide

                        current_slide = e
                        await interaction.response.edit_message(embed=current_slide)
                        await self.update_buttons(interaction)

                    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label="<", disabled=True,
                                       custom_id="left")
                    async def left_button_callback(self, button, interaction):
                        nonlocal current_slide

                        current_slide = slides[slides.index(current_slide) - 1]
                        await interaction.response.edit_message(embed=current_slide)
                        await self.update_buttons(interaction)

                    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label=">", disabled=True,
                                       custom_id="right")
                    async def right_button_callback(self, button, interaction):
                        nonlocal current_slide

                        current_slide = slides[slides.index(current_slide) + 1]
                        await interaction.response.edit_message(embed=current_slide)
                        await self.update_buttons(interaction)

                    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label=">>", disabled=True,
                                       custom_id="last")
                    async def last_button_callback(self, button, interaction):
                        nonlocal current_slide

                        current_slide = slides[len(slides) - 1]
                        await interaction.response.edit_message(embed=current_slide)
                        await self.update_buttons(interaction)

                    @discord.ui.button(label="Add Question", row=1, style=discord.ButtonStyle.secondary, emoji="➕", custom_id="add")
                    async def add_button_callback(self, button, interaction):
                        await interaction.response.send_modal(QuestionModal(self, title="Create a Question"))

                    @discord.ui.button(label="Remove", row=1, style=discord.ButtonStyle.secondary, emoji="🗑",
                                       disabled=True, custom_id="trash")
                    async def remove_button_callback(self, button, interaction):
                        nonlocal current_slide
                        slides.remove(current_slide)
                        current_slide = slides[len(slides) - 1]
                        await interaction.response.edit_message(embed=current_slide)
                        await self.update_buttons(interaction)

                    @discord.ui.button(label="Done", row=2, style=discord.ButtonStyle.success, emoji="✅", disabled=True,
                                       custom_id="done")
                    async def done_button_callback(self, button, interaction):
                        await interaction.response.send_message("Created the Quiz!")

                    @discord.ui.button(label="Edit", row=2, style=discord.ButtonStyle.primary, emoji="✂",
                                       custom_id="edit")
                    async def edit_button_callback(self, button, interaction):
                        await interaction.response.send_modal(EditModal(view=self, modal_embed=current_slide, title="Editing Modal"))
                        #await interaction.response.send_message("Editing the Quiz!")

                    @discord.ui.button(label="Cancel", row=2, style=discord.ButtonStyle.danger, emoji="✖",
                                       custom_id="cancel")
                    async def cancel_button_callback(self, button, interaction):
                        await interaction.response.edit_message(delete_after=0)
                        await interaction.followup.send("Cancelled Quiz Creation")

                    self.timeout = None

                # await interaction.response.send_message("Success", delete_after=0)
                await interaction.response.send_message(embed=current_slide, view=QuizView())
                quiz_message = await interaction.original_response()

                for i in range(len(sections)):
                    await quiz_message.add_reaction(chr(0x1f1e6 + i))

        modal = QuizModal(title="Creating a Quiz")
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
