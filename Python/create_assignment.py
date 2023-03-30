import discord
from create_classes import Assignment
import io
import asyncio
import discord
import json
import os
from discord.ext import commands
from typing import Optional, List
import datetime
import api
from create_classes import Quiz, Question
import random
import time


def create_assignment(bot, file=None, preset=None):
    class AssignmentModal(discord.ui.Modal):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.bot = bot
            self.file = file

            val_title = None
            val_details = None
            val_points = None
            val_start_date = datetime.date.today().strftime('%Y-%m-%d')
            val_due_date = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            if preset:
                val_title = preset['title']
                val_details = preset['details']
                val_points = preset['points']
                val_start_date = preset['start_date']
                val_due_date = preset['due_date']

            title = discord.ui.InputText(label="Title", style=discord.InputTextStyle.short,
                                         placeholder="ex: 'To Kill a Mockingbird Essay'", max_length=32, value=val_title)
            details = discord.ui.InputText(label="Details",
                                           placeholder="ex: 'Write a 700 word essay on the symbolism in To Kill a Mockingbird in MLA format.'",
                                           style=discord.InputTextStyle.long, value=val_details)
            points = discord.ui.InputText(label="Points", style=discord.InputTextStyle.short,
                                          placeholder="ex: '40'", value=val_points)
            start_date = discord.ui.InputText(label="Start Date", style=discord.InputTextStyle.short,
                                              placeholder="ex: '2023-05-25'", value=val_start_date)
            due_date = discord.ui.InputText(label="Due Date", style=discord.InputTextStyle.short,
                                            placeholder="ex: '2023-06-14'", value=val_due_date)
            self.add_item(title)
            self.add_item(details)
            self.add_item(points)
            self.add_item(start_date)
            self.add_item(due_date)

        async def callback(self, interaction: discord.Interaction):
            title = self.children[0].value

            e = discord.Embed(title=f"{title}")

            details = self.children[1].value

            try:
                points = int(self.children[2].value)
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

            e.add_field(name="Details", value=details, inline=False)
            e.add_field(name="Points", value=str(points), inline=False)
            e.add_field(name="Start Date", value=start_date, inline=False)
            e.add_field(name="Due Date", value=due_date, inline=False)

            assignments_category = discord.utils.get(interaction.guild.categories, name='Assignments')
            if assignments_category is None:
                assignments_category = await interaction.guild.create_category('Assignments')

            assignment_channel = discord.utils.get(assignments_category.channels, name=title)
            if assignment_channel is None:
                new_assignment_channel = await interaction.guild.create_text_channel(f"{self.children[0].value}",
                                                                                 category=assignments_category)
            else:
                return await interaction.response.send_message('An Assignment with that name already exists')

            await new_assignment_channel.send(embed=e)

            if file:
                file_data = await file.read()
                await new_assignment_channel.send(file=discord.File(io.BytesIO(file_data), filename=file.filename))

            student_role = discord.utils.get(interaction.guild.roles, name="Student")

            await new_assignment_channel.send(f"{student_role.mention} use the `/submit` command to submit your assignment")

            res = await api.get_classroom_id(interaction.guild.id)
            classroom_id = res['id']

            new_assignment = Assignment(title=title, start=str(start_date),
                                        due=str(due_date), points=points,
                                        classroomId=classroom_id, channelId=new_assignment_channel.id)

            await api.create_assignment(new_assignment)

            data = {
                'type': 'Assignment',
                'title': title,
                'details': details,
                'points': points,
                'start_date': start_date.isoformat(),
                'due_date': due_date.isoformat()
            }

            json_str = json.dumps(data, indent=4)

            json_bytes = io.BytesIO(json_str.encode('utf-8'))
            json_bytes.seek(0)

            await interaction.response.send_message(
                'Assignment created.\nYou can use this file with `/create upload` to quickly make tasks.',
                file=discord.File(json_bytes, f'Assignment-{title}.json'))

    modal = AssignmentModal(title="Creating an Assignment")
    return modal
