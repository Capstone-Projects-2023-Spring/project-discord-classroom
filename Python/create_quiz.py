import asyncio
import discord
import json
from typing import Optional, List
import datetime
import api
from create_classes import Quiz, Question
import random
import time
import io
import re


class EditModal(discord.ui.Modal):
    def __init__(self, task_dict: dict, message: discord.Message, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type = task_dict['type']
        self.message = message
        self.channel_id = task_dict['channelId']
        val_title = task_dict['title']
        val_points = task_dict['points']
        val_start_date = task_dict['start']
        val_due_date = task_dict['due']

        title = discord.ui.InputText(label="Title", style=discord.InputTextStyle.short,
                                     placeholder="ex: 'Introductions'", max_length=32, value=val_title)
        self.add_item(title)

        if 'details' in task_dict:
            details = task_dict['details']
            details = discord.ui.InputText(label="Details",
                                           placeholder="ex: 'Introduce yourself to your fellow classmates.'",
                                           style=discord.InputTextStyle.long, value=details)
            self.add_item(details)

        elif 'time' in task_dict:
            val_time_limit = task_dict['time']
            time_limit = discord.ui.InputText(label="Time Limit",
                                              placeholder="ex: '30' for 30 minutes or '0' for no time limit",
                                              style=discord.InputTextStyle.short, value=val_time_limit)
            self.add_item(time_limit)

        points = discord.ui.InputText(label="Points", style=discord.InputTextStyle.short,
                                      placeholder="ex: '20'", value=val_points)
        start_date = discord.ui.InputText(label="Start Date", style=discord.InputTextStyle.short,
                                          placeholder="ex: '2023-05-25'", value=val_start_date)
        due_date = discord.ui.InputText(label="Due Date", style=discord.InputTextStyle.short,
                                        placeholder="ex: '2023-05-30'", value=val_due_date)

        self.add_item(points)
        self.add_item(start_date)
        self.add_item(due_date)

    async def callback(self, interaction: discord.Interaction):
        e = discord.Embed(title=f"{self.type}")
        title = self.children[0].value
        points = self.children[2].value
        start_date = self.children[3].value
        due_date = self.children[4].value

        update_json = {'title': title, 'points': int(float(points)), 'startDate': start_date,
                       'dueDate': due_date}

        e.add_field(name="Title", value=title, inline=False)
        if self.type == "Quiz":
            time_limit = self.children[1].value
            e.add_field(name="Time Limit", value=time_limit, inline=False)
            update_json['timeLimit'] = time_limit
        else:
            details = self.children[1].value
            e.add_field(name="Details", value=details, inline=False)
        e.add_field(name="Points", value=points, inline=False)
        e.add_field(name="Start Date", value=start_date, inline=False)
        e.add_field(name="Due Date", value=due_date, inline=False)

        if self.type == "Assignment":
            await api.update_assignment(update_json, self.channel_id)
        if self.type == "Quiz":
            await api.update_quiz(update_json, self.channel_id)

        await self.message.edit(embed=e)

        await interaction.response.send_message(f"{self.type} Successfully Edited", delete_after=3, ephemeral=True)

class InputModal(discord.ui.Modal):
    def __init__(self, embed: discord.Embed, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.embed = embed
        answer = discord.ui.InputText(label="Answer", style=discord.InputTextStyle.long,
                                      placeholder="Type answer here...")
        self.add_item(answer)

    async def callback(self, interaction: discord.Interaction):
        self.embed.set_field_at(index=1, name="Answer", value=f"```{self.children[0].value}```", inline=False)
        await interaction.response.edit_message(embed=self.embed)


class TakeQuiz(discord.ui.View):
    def __init__(self, embed_ques: List[discord.Embed], quiz_dict: dict, answers: List[str], points: List[float]):
        super().__init__(timeout=None)
        self.eq = embed_ques
        self.this_question = embed_ques[0]
        self.quiz_title = quiz_dict['title']
        self.quiz_total_points = quiz_dict['points']
        self.answers = answers
        self.was_submitted = False
        self.points = points
        right_button = self.get_item('right')
        last_button = self.get_item('last')
        self.has_answer = []
        for q in embed_ques:
            self.has_answer.append(False)
        if len(embed_ques) > 1:
            right_button.disabled = False
            last_button.disabled = False
        if self.this_question.fields[1].name == "Options":
            num_of_options = len(self.this_question.fields[1].value.split("\n")) - 1
            self.get_item("A").disabled = False
            self.get_item("B").disabled = False
            if num_of_options >= 3:
                self.get_item("C").disabled = False
            if num_of_options >= 4:
                self.get_item("D").disabled = False
            if num_of_options >= 5:
                self.get_item("E").disabled = False
        elif self.this_question.fields[1].name == "Answer":
            self.get_item("A").disabled = True
            self.get_item("B").disabled = True
            self.get_item("C").disabled = True
            self.get_item("D").disabled = True
            self.get_item("E").disabled = True
            self.get_item("input").disabled = False

    async def update_arrows(self, interaction: discord.Interaction):
        first = self.get_item("first")
        left = self.get_item("left")
        right = self.get_item("right")
        last = self.get_item("last")

        if self.this_question != self.eq[0]:
            first.disabled = False
            left.disabled = False
        else:
            first.disabled = True
            left.disabled = True

        if self.this_question != self.eq[len(self.eq) - 1]:
            right.disabled = False
            last.disabled = False
        else:
            right.disabled = True
            last.disabled = True

        if self.this_question.fields[1].name == "Options":
            self.get_item("input").disabled = True
            num_of_options = len(self.this_question.fields[1].value.split("\n")) - 1
            self.get_item("A").disabled = False
            self.get_item("B").disabled = False
            if num_of_options >= 3:
                self.get_item("C").disabled = False
            if num_of_options >= 4:
                self.get_item("D").disabled = False
            if num_of_options >= 5:
                self.get_item("E").disabled = False
        elif self.this_question.fields[1].name == "Answer":
            self.get_item("A").disabled = True
            self.get_item("B").disabled = True
            self.get_item("C").disabled = True
            self.get_item("D").disabled = True
            self.get_item("E").disabled = True
            self.get_item("input").disabled = False

        await self.update_letters(interaction)
        await interaction.followup.edit_message(view=self, message_id=interaction.message.id)

    async def update_letters(self, interaction: discord.Interaction, letter: str = None):

        self.get_item("A").style = discord.ButtonStyle.secondary
        self.get_item("B").style = discord.ButtonStyle.secondary
        self.get_item("C").style = discord.ButtonStyle.secondary
        self.get_item("D").style = discord.ButtonStyle.secondary
        self.get_item("E").style = discord.ButtonStyle.secondary

        if letter is not None:
            letter_clicked = self.get_item(letter)
            letter_clicked.style = discord.ButtonStyle.success

        await self.update_submit(interaction)
        await interaction.followup.edit_message(view=self, message_id=interaction.message.id)

    async def update_submit(self, interaction: discord.Interaction):

        if all(self.has_answer):
            submit_button = self.get_item("submit")
            submit_button.disabled = False
            await interaction.followup.edit_message(view=self, message_id=interaction.message.id)

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label="<<", disabled=True,
                       custom_id="first")
    async def first_button_callback(self, button, interaction):
        self.this_question = self.eq[0]
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_arrows(interaction)

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label="<", disabled=True,
                       custom_id="left")
    async def left_button_callback(self, button, interaction):
        self.this_question = self.eq[self.eq.index(self.this_question) - 1]
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_arrows(interaction)

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label=">", disabled=True,
                       custom_id="right")
    async def right_button_callback(self, button, interaction):
        self.this_question = self.eq[self.eq.index(self.this_question) + 1]
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_arrows(interaction)

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label=">>", disabled=True,
                       custom_id="last")
    async def last_button_callback(self, button, interaction):
        self.this_question = self.eq[len(self.eq) - 1]
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_arrows(interaction)

    @discord.ui.button(row=1, style=discord.ButtonStyle.secondary, emoji="🇦", disabled=True, custom_id="A")
    async def a_button_callback(self, button, interaction: discord.Interaction):
        options = self.this_question.fields[1]
        answer = options.value.split("\n")[0].split("🇦 ")[1]
        self.this_question.set_field_at(index=2, name="Answer", value=f"```{answer}```", inline=False)
        self.has_answer[self.eq.index(self.this_question)] = True
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_letters(interaction, "A")

    @discord.ui.button(row=1, style=discord.ButtonStyle.secondary, emoji="🇧", disabled=True, custom_id="B")
    async def b_button_callback(self, button, interaction: discord.Interaction):
        options = self.this_question.fields[1]
        answer = options.value.split("\n")[1].split("🇧 ")[1]
        self.this_question.set_field_at(index=2, name="Answer", value=f"```{answer}```", inline=False)
        self.has_answer[self.eq.index(self.this_question)] = True
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_letters(interaction, "B")

    @discord.ui.button(row=1, style=discord.ButtonStyle.secondary, emoji="🇨", disabled=True, custom_id="C")
    async def c_button_callback(self, button, interaction: discord.Interaction):
        options = self.this_question.fields[1]
        answer = options.value.split("\n")[2].split("🇨 ")[1]
        self.this_question.set_field_at(index=2, name="Answer", value=f"```{answer}```", inline=False)
        self.has_answer[self.eq.index(self.this_question)] = True
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_letters(interaction, "C")

    @discord.ui.button(row=1, style=discord.ButtonStyle.secondary, emoji="🇩", disabled=True, custom_id="D")
    async def d_button_callback(self, button, interaction: discord.Interaction):
        options = self.this_question.fields[1]
        answer = options.value.split("\n")[3].split("🇩 ")[1]
        self.this_question.set_field_at(index=2, name="Answer", value=f"```{answer}```", inline=False)
        self.has_answer[self.eq.index(self.this_question)] = True
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_letters(interaction, "D")

    @discord.ui.button(row=1, style=discord.ButtonStyle.secondary, emoji="🇪", disabled=True, custom_id="E")
    async def e_button_callback(self, button, interaction: discord.Interaction):
        options = self.this_question.fields[1]
        answer = options.value.split("\n")[4].split("🇪 ")[1]
        self.this_question.set_field_at(index=2, name="Answer", value=f"```{answer.strip()}```", inline=False)
        self.has_answer[self.eq.index(self.this_question)] = True
        await interaction.response.edit_message(embed=self.this_question)
        await self.update_letters(interaction, "E")

    @discord.ui.button(row=2, style=discord.ButtonStyle.secondary, emoji="⌨", label="Type Answer", disabled=True,
                       custom_id="input")
    async def input_button_callback(self, button, interaction: discord.Interaction):
        response = await interaction.response.send_modal(InputModal(self.this_question, title="Type Answer"))
        self.has_answer[self.eq.index(self.this_question)] = True
        await self.update_submit(interaction)

    async def submit_quiz(self, interaction: discord.Interaction, from_timer: bool):
        submissions_category = None

        for category in interaction.guild.categories:
            if category.name == "Submissions":
                submissions_category = category

        res = await api.get_user_id(interaction.user.id)
        user_id = res['id']
        res = await api.get_quiz(interaction.channel_id)
        quiz_id = res['quiz']['id']

        self.was_submitted = True

        new_channel = await interaction.guild.create_text_channel(
            f"❓{self.quiz_title}-{interaction.user.display_name}", category=submissions_category)

        message = ""
        questions = []
        student_answers = []

        for eq in self.eq:
            for field in eq.fields:
                if field.name == "Question":
                    questions.append(field.value)
                if field.name == "Answer":
                    student_answers.append(field.value.split("```")[1])

        message += f"**Quiz - {self.quiz_title}**\t{self.quiz_total_points} Pts.\nStudent: {interaction.user.display_name}\n\n"

        for i, ques in enumerate(questions):
            if student_answers[i].lower().strip() == self.answers[i].lower().strip():
                message += f"Question {i + 1}.\t{self.points[i]} Pts.\n{ques}\nStudent's Answer: ✅```{student_answers[i]}```\nCorrect Answer: ```{self.answers[i]}```\n\n"
            elif self.answers[i] == "None":
                message += f"Question {i + 1}.\t{self.points[i]} Pts.\n{ques}\nStudent's Answer: ⚠️```{student_answers[i]}```\nCorrect Answer: ```{self.answers[i]}```\n\n"
            else:
                message += f"Question {i + 1}.\t{self.points[i]} Pts.\n{ques}\nStudent's Answer: ❌```{student_answers[i]}```\nCorrect Answer: ```{self.answers[i]}```\n\n"
        if not from_timer:
            await interaction.response.edit_message(content="Quiz Submitted", embed=None, view=None)
        await new_channel.send(f"ID: Q-{quiz_id}-{user_id}")
        await new_channel.send(message)

    @discord.ui.button(row=3, style=discord.ButtonStyle.success, emoji="✅", label="Submit Quiz", disabled=True,
                       custom_id="submit")
    async def submit_button_callback(self, button, interaction: discord.Interaction):
        await self.submit_quiz(interaction, False)


class StartQuiz(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(row=0, style=discord.ButtonStyle.success, label="Start Quiz", disabled=True, custom_id="start")
    async def start_button_callback(self, button, interaction: discord.Interaction):
        student_role = discord.utils.get(interaction.guild.roles, name="Student")
        if student_role not in interaction.user.roles:
            return await interaction.response.send_message("Only students can take quizzes", ephemeral=True)
        quiz = await api.get_quiz(interaction.channel_id)
        user_id = await api.get_user_id(interaction.user.id)

        #Checks if the user already took the quiz
        submissions_category = discord.utils.get(interaction.guild.categories, name="Submissions")
        if submissions_category:
            for channel in submissions_category.channels:
                if isinstance(channel, discord.TextChannel):
                    channel_name = channel.name
                    display_name_split = re.split(r'[-\s]', interaction.user.display_name)
                    if channel_name[0] == '❓':
                        submission_title = channel_name.split('❓')[1]
                        if channel_name.split('-')[-1] == display_name_split[-1].lower() and submission_title.startswith(interaction.channel.name):
                            try:
                                first_message = await channel.history(oldest_first=True, limit=1).next()
                                first_message_split = first_message.content.split('-')
                                channel_quiz_id = first_message_split[1]
                                channel_user_id = first_message_split[2]
                                if str(channel_quiz_id) == str(quiz['quiz']['id']) and str(channel_user_id) == str(user_id['id']):
                                    return await interaction.response.send_message("You already took this quiz", ephemeral=True)
                            except Exception as e:
                                print(f"Error fetching first message in channel {channel_name}")

        quiz_time = quiz['quiz']['timeLimit']
        quiz_id = quiz['quiz']['id']
        due = quiz['quiz']['dueDate']
        start_button = self.get_item("start")
        refresh_button = self.get_item("refresh")
        if datetime.datetime.strptime(due, '%Y-%m-%d') < datetime.datetime.now():
            self.remove_item(start_button)
            self.remove_item(refresh_button)
            embed = interaction.message.embeds[0]
            embed.add_field(name="", value="```diff\n- Quiz is no longer available```", inline=False)
            return await interaction.response.edit_message(embed=embed, view=self)
        request = await api.get_questions(quiz_id)
        question_json = request['questions']
        answers = []
        points = []
        questions_as_embed = []
        for i, question in enumerate(question_json):
            answers.append(question['answer'])
            points.append(question['points'])
            embed = discord.Embed(
                title=f"Question {i + 1}/{len(question_json)}.\t\t\t\t{str(question['points'])} Pts.")
            embed.add_field(name="Question", value=question['question'], inline=False)
            if question['wrong'][0] != "None":
                options = [question['answer']]
                for w in question['wrong']:
                    options.append(w)
                options = random.sample(options, len(options))
                options_string = ""
                for j, opt in enumerate(options):
                    options_string += f"{chr(0x1f1e6 + j)} {opt}\n"
                embed.add_field(name="Options", value=options_string, inline=False)
            embed.add_field(name="Answer", value="``` ```", inline=False)
            questions_as_embed.append(embed)
        current_question = questions_as_embed[0]
        take_quiz = TakeQuiz(questions_as_embed, quiz['quiz'], answers, points)
        await interaction.response.send_message(embed=current_question, ephemeral=True, view=take_quiz)

        if quiz_time > 0:
            num_seconds = quiz_time * 60
            start_time = time.time()

            # Update Timer
            while time.time() - start_time < num_seconds and take_quiz.was_submitted == False:
                time_remaining = int(num_seconds - (time.time() - start_time))
                minutes, seconds = divmod(time_remaining, 60)
                time_format = '{:02d}:{:02d}'.format(minutes, seconds)
                await interaction.edit_original_response(content=f"⏳ {str(time_format)}")
                await asyncio.sleep(1)

            if take_quiz.was_submitted == False:
                await interaction.edit_original_response(content=f"TIME'S UP! - Quiz Submitted", embed=None, view=None)
                await take_quiz.submit_quiz(interaction, True)

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, emoji='🔃', custom_id="refresh")
    async def refresh_button_callback(self, button, interaction):
        quiz = await api.get_quiz(interaction.channel_id)
        start = quiz['quiz']['startDate']
        start_button = self.get_item("start")
        if datetime.datetime.strptime(start, '%Y-%m-%d') <= datetime.datetime.now():
            start_button.disabled = False
            refresh_button = self.get_item("refresh")
            self.remove_item(refresh_button)
        await interaction.response.edit_message(view=self)


def create_quiz(bot, preset=None):
    class QuizModal(discord.ui.Modal):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.bot = bot

            val_title = None
            val_time_limit = 0
            val_points = None
            val_start_date = datetime.date.today().strftime('%Y-%m-%d')
            val_due_date = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            if preset:
                val_title = preset['title']
                val_time_limit = preset['time_limit']
                val_points = int(preset['points'])
                val_start_date = preset['start_date']
                val_due_date = preset['due_date']

            title = discord.ui.InputText(label="Title", style=discord.InputTextStyle.short,
                                         placeholder="ex: 'Parts of the Cell'", max_length=32, value=val_title)
            time_limit = discord.ui.InputText(label="Time Limit (minutes)",
                                              placeholder="ex: '30' for 30 minutes or '0' for no time limit",
                                              style=discord.InputTextStyle.short, value=str(val_time_limit))
            points = discord.ui.InputText(label="Points", style=discord.InputTextStyle.short,
                                          placeholder="ex: '50'", required=False, value=val_points)
            start_date = discord.ui.InputText(label="Start Date", style=discord.InputTextStyle.short,
                                              placeholder="ex: '2023-05-25'", value=val_start_date)
            due_date = discord.ui.InputText(label="Due Date", style=discord.InputTextStyle.short,
                                            placeholder="ex: '2023-05-30'", value=val_due_date)
            self.add_item(title)
            self.add_item(time_limit)
            self.add_item(points)
            self.add_item(start_date)
            self.add_item(due_date)

        async def callback(self, interaction: discord.Interaction):
            e = discord.Embed(title="Creating Quiz...")
            title = self.children[0].value
            if self.children[2].value != "":
                try:
                    points = float(self.children[2].value)
                except ValueError:
                    return await interaction.response.send_message("Invalid points")
            try:
                start_date = datetime.datetime.strptime(self.children[3].value, "%Y-%m-%d").date()
            except ValueError:
                return await interaction.response.send_message("Invalid start date format")
            try:
                due_date = datetime.datetime.strptime(self.children[4].value, "%Y-%m-%d").date()
            except ValueError:
                return await interaction.response.send_message("Invalid due date format")
            try:
                time_limit = int(self.children[1].value)
            except ValueError:
                return await interaction.response.send_message("Invalid time limit")

            e.add_field(name="Title", value=title, inline=False)
            e.add_field(name="Time Limit", value=str(time_limit), inline=False)
            if self.children[1].value != "":
                e.add_field(name="Points", value=str(points), inline=False)
                even_points = 1
            else:
                e.add_field(name="Points", value="TBD", inline=False)
                even_points = 0
            e.add_field(name="Start Date", value=start_date, inline=False)
            e.add_field(name="Due Date", value=due_date, inline=False)
            e.add_field(name="Number of Questions", value="0", inline=False)

            current_slide = e
            slides = [e]

            class QuestionModal(discord.ui.Modal):
                def __init__(self, quiz_view, *args, **kwargs) -> None:
                    super().__init__(*args, **kwargs)
                    self.quiz_view = quiz_view
                    question = discord.ui.InputText(label="Question", style=discord.InputTextStyle.short,
                                                    placeholder="ex: 'Who was the first U.S. President?'")
                    answer = discord.ui.InputText(label="Answer", style=discord.InputTextStyle.short,
                                                  placeholder="ex: 'George Washington'",
                                                  required=False)
                    wrong = discord.ui.InputText(label="Wrong Options", style=discord.InputTextStyle.short,
                                                 placeholder="ex: 'Ben Franklin, Thomas Jefferson, John Adams'",
                                                 required=False)
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
                        if len(self.children[2].value.split(", ")) > 4:
                            return await interaction.response.send_message("Max wrong options is five", delete_after=5)
                        add_e.add_field(name="Wrong Options", value=self.children[2].value)
                    else:
                        add_e.add_field(name="Wrong Options", value="None")
                    if self.children[1].value == "" and self.children[2].value != "":
                        return await interaction.response.send_message("Cannot have wrong options without an answer", delete_after=5)
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
                    if preset:
                        preset_questions = preset['questions']
                        for i, question in enumerate(preset_questions):
                            new_embed = discord.Embed(title=f"Question {i+1}.")
                            new_embed.add_field(name="Question", value=question['question'])
                            new_embed.add_field(name='Answer', value=question['answer'])
                            new_embed.add_field(name='Wrong Options', value=question['wrong'])
                            new_embed.add_field(name='Points', value=question['points'])
                            slides.append(new_embed)

                async def update_buttons(self, interaction):
                    left = self.get_item("left")
                    right = self.get_item("right")
                    done = self.get_item("done")
                    trash = self.get_item("trash")
                    first = self.get_item("first")
                    last = self.get_item("last")

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
                        last.disabled = False
                    else:
                        right.disabled = True
                        last.disabled = True

                    if current_slide != slides[0]:
                        trash.disabled = False
                    else:
                        trash.disabled = True

                    e.set_field_at(index=5, name="Number of Questions", value=str(len(slides) - 1), inline=False)
                    self.update_points()

                    if interaction.message is not None:
                        await interaction.followup.edit_message(embed=current_slide,
                                                                 message_id=interaction.message.id,
                                                                 view=self)
                    else:
                        await interaction.followup.edit_message(embed=current_slide,
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
                async def done_button_callback(self, button, interaction: discord.Interaction):
                    quiz_fields = slides[0].fields

                    question_list = []
                    question_data = []

                    for i, question in enumerate(slides):
                        if i > 0:
                            ques = question.fields[0].value
                            answer = question.fields[1].value
                            wrong = question.fields[2].value.split(", ")
                            points = float(question.fields[3].value)
                            new_question = Question(question=ques, answer=answer,
                                                    wrong=wrong, points=points)
                            question_list.append(new_question)
                            question_data.append({'question': ques, 'answer': answer, 'wrong': question.fields[2].value, 'points': points})

                    await interaction.response.defer()

                    request = await api.create_questions(question_list)

                    url = str(request['url'])

                    quizzes_category = None

                    for category in interaction.guild.categories:
                        if category.name == "Quizzes":
                            quizzes_category = category

                    new_channel = await interaction.guild.create_text_channel(f"{quiz_fields[0].value}",
                                                                              category=quizzes_category)

                    res = await api.get_classroom_id(interaction.guild.id)
                    classroom_id = res['id']

                    new_quiz = Quiz(title=quiz_fields[0].value, points=float(quiz_fields[2].value),
                                    startDate=quiz_fields[3].value,
                                    dueDate=quiz_fields[4].value, timeLimit=quiz_fields[1].value, questions=url,
                                    classroomId=classroom_id, channelId=new_channel.id)

                    await api.create_quiz(new_quiz)

                    slides[0].title = "Quiz"
                    await new_channel.send(embed=slides[0], view=StartQuiz())

                    data = {
                        'type': 'Quiz',
                        'title': new_quiz.title,
                        'time_limit': new_quiz.timeLimit,
                        'points': new_quiz.points,
                        'start_date': new_quiz.startDate,
                        'due_date': new_quiz.dueDate,
                        'questions': question_data
                    }

                    json_str = json.dumps(data, indent=4)

                    json_bytes = io.BytesIO(json_str.encode('utf-8'))
                    json_bytes.seek(0)

                    await interaction.followup.send('You can use this file with `/create upload` to quickly make tasks.',
                        file=discord.File(json_bytes, f'Quiz-{title}.json'))

                    await interaction.followup.edit_message(message_id=interaction.message.id,
                                                            content="Created the Quiz!", embed=None, view=None)

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
            await quiz_view.update_buttons(interaction)

    modal = QuizModal(title="Creating a Quiz")
    return modal
