import asyncio

import discord
import json
import os
from discord.ext import commands
from typing import Optional, List
import datetime
import api
from cr_classes import Quiz
from cr_classes import Question


def create_quiz(bot):
    class QuizModal(discord.ui.Modal):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.bot = bot

            title = discord.ui.InputText(label="Title", style=discord.InputTextStyle.short,
                                         placeholder="ex: 'Parts of the Cell'", value="Test")
            points = discord.ui.InputText(label="Points", style=discord.InputTextStyle.short,
                                          placeholder="ex: '50'", value=20, required=False)
            start_date = discord.ui.InputText(label="Start Date", style=discord.InputTextStyle.short,
                                              placeholder="ex: '2023-05-25'", value="2023-06-01")
            due_date = discord.ui.InputText(label="Due Date", style=discord.InputTextStyle.short,
                                            placeholder="ex: '2023-05-30'", value="2023-06-08")
            time_limit = discord.ui.InputText(label="Time Limit (minutes)", placeholder="ex: '30' for 30 minutes or '0' for no time limit",
                                              style=discord.InputTextStyle.short, value="0")
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
            e.add_field(name="Start Date", value=start_date, inline=False)
            e.add_field(name="Due Date", value=due_date, inline=False)
            e.add_field(name="Time Limit", value=str(time_limit), inline=False)
            e.add_field(name="Number of Questions", value="0", inline=False)

            server = interaction.guild
            classroom_id = await api.get_classroom_id(server.id)
            response = await api.get_sections(classroom_id['id'])
            sections = []
            for r in response['sections']:
                sections.append(r['name'])
            sec_str = ""
            for i, section in enumerate(sections):
                sec_str += f'{section}\n'

            e.add_field(name="Sections", value=str(sec_str), inline=False)

            current_slide = e
            slides = [e]

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
                        add_e.add_field(name="Points", value=str(points / len(slides)))
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
                            new_its.append(
                                discord.ui.InputText(label=it.name, style=discord.InputTextStyle.short, value=it.value,
                                                     required=False))
                        else:
                            new_its.append(
                                discord.ui.InputText(label=it.name, style=discord.InputTextStyle.short, value=it.value))
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
                def __init__(self):
                    super().__init__(timeout=None)

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

                    if interaction2.message is not None:
                        await interaction2.followup.edit_message(embed=current_slide,
                                                                 message_id=interaction2.message.id,
                                                                 view=self)
                    else:
                        await interaction2.followup.edit_message(embed=current_slide,
                                                                 message_id=quiz_message.id,
                                                                 view=self)

                def update_points(self):
                    total_points = 0
                    for i, slide in enumerate(slides):
                        if i != 0:
                            if even_points == 1:
                                slide.set_field_at(3, name="Points", value=str(points / (len(slides) - 1)))
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

                @discord.ui.button(label="Add Question", row=1, style=discord.ButtonStyle.secondary, emoji="➕",
                                   custom_id="add")
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
                    fields = slides[0].fields
                    quiz_dict = {'title': fields[0].value, 'points': float(fields[1].value), 'start': fields[2].value,
                                 'due': fields[3].value, 'time': fields[4].value,
                                 'sections': fields[6].value.split("\n")}

                    for section in quiz_dict['sections']:
                        if section == "":
                            quiz_dict['sections'].remove(section)

                    question_list = []

                    for i, question in enumerate(slides):
                        if i > 0:
                            fields = question.fields
                            wrong = fields[2].value.split(",")
                            question_dict = Question(question=fields[0].value, answer=fields[1].value,
                                                     wrong=wrong, points=float(fields[3].value))
                            question_list.append(question_dict)

                    await interaction.response.defer()

                    url = str(await api.create_questions(question_list))

                    new_quiz = Quiz(title=quiz_dict['title'], points=quiz_dict['points'], start=quiz_dict['start'],
                                    due=quiz_dict['due'], time=quiz_dict['time'], questions=url,
                                    sections=quiz_dict['sections'])

                    server = interaction.guild_id

                    await api.create_quiz(new_quiz, server_id=server)

                    quizzes_category = None

                    for category in interaction.guild.categories:
                        if category.name == "Quizzes":
                            quizzes_category = category

                    new_channel = await interaction.guild.create_text_channel(f"{quiz_dict['title']}", category=quizzes_category)

                    slides[0].title = "Quiz"
                    await new_channel.send(embed=slides[0])
                    student_role = discord.utils.get(interaction.guild.roles, name="Student")
                    await new_channel.send(f"{student_role.mention} Type '/start' to take the Quiz")

                    await interaction.followup.send("Created the Quiz!")

                @discord.ui.button(label="Edit", row=2, style=discord.ButtonStyle.primary, emoji="✂",
                                   custom_id="edit")
                async def edit_button_callback(self, button, interaction):
                    await interaction.response.send_modal(
                        EditModal(view=self, modal_embed=current_slide, title="Editing Modal"))

                @discord.ui.button(label="Cancel", row=2, style=discord.ButtonStyle.danger, emoji="✖",
                                   custom_id="cancel")
                async def cancel_button_callback(self, button, interaction):
                    await interaction.response.edit_message(delete_after=0)
                    await interaction.followup.send("Cancelled Quiz Creation")

            # await interaction.response.send_message("Success", delete_after=0)
            quiz_view = QuizView()
            await interaction.response.send_message(embed=current_slide, view=quiz_view)
            quiz_message = await interaction.original_response()

            for i in range(len(sections)):
                await quiz_message.add_reaction(chr(0x1f1e6 + i))

            def check(reaction, user):
                return user == interaction.user and reaction.message.id == quiz_message.id

            section_array = []

            while True:
                tasks = [
                    asyncio.create_task(self.bot.wait_for("reaction_add", check=check), name="radd"),
                    asyncio.create_task(self.bot.wait_for("reaction_remove", check=check), name="rrem")
                ]

                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

                finished = list(done)[0]

                action = finished.get_name()
                result = finished.result()

                if action == "radd":
                    reaction, user = result
                    for i in range(len(sections)):
                        if reaction.emoji == chr(127462 + i):
                            section_array.append(sections[i])
                            section_string = ""
                            for i, sec in enumerate(section_array):
                                section_string += f'{sec}\n'
                            slides[0].set_field_at(index=6, name="Sections", value=str(section_string))
                    current_slide = slides[0]
                    await interaction.followup.edit_message(message_id=quiz_message.id, embed=current_slide)
                    await QuizView.update_buttons(quiz_view, interaction2=interaction)


                elif action == "rrem":
                    reaction, user = result
                    for i in range(len(sections)):
                        if reaction.emoji == chr(127462 + i):
                            section_array.remove(sections[i])
                            section_string = ""
                            for k, sec in enumerate(section_array):
                                section_string += f'{sec}\n'
                            if len(section_array) > 0:
                                e.set_field_at(index=6, name="Sections", value=str(section_string))
                            else:
                                e.set_field_at(index=6, name="Sections", value=str(sec_str))
                    slides[0] = e
                    current_slide = slides[0]
                    await interaction.followup.edit_message(message_id=quiz_message.id, embed=current_slide)
                    await QuizView.update_buttons(quiz_view, interaction)

    modal = QuizModal(title="Creating a Quiz")
    return modal
