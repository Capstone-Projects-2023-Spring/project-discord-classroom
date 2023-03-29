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
from create_classes import Discussion


def create_discussion(bot):
    class DiscussionModal(discord.ui.Modal):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.bot = bot

            title = discord.ui.InputText(label="Title", style=discord.InputTextStyle.short,
                                         placeholder="ex: 'Introductions'", max_length=32)
            description = discord.ui.InputText(label="Description",
                                               placeholder="ex: 'Introduce yourself to your fellow classmates.'",
                                               style=discord.InputTextStyle.long)
            points = discord.ui.InputText(label="Points", style=discord.InputTextStyle.short,
                                          placeholder="ex: '20'")
            start_date = discord.ui.InputText(label="Start Date", style=discord.InputTextStyle.short,
                                              placeholder="ex: '2023-05-25'",
                                              value=f"{datetime.date.today().strftime('%Y-%m-%d')}")
            due_date = discord.ui.InputText(label="Due Date", style=discord.InputTextStyle.short,
                                            placeholder="ex: '2023-05-30'",
                                            value=f"{(datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')}")
            self.add_item(title)
            self.add_item(description)
            self.add_item(points)
            self.add_item(start_date)
            self.add_item(due_date)

        async def callback(self, interaction: discord.Interaction):

            title = self.children[0].value

            e = discord.Embed(title=f"{title}")

            description = self.children[1].value

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

            e.add_field(name="Description", value=description, inline=False)
            e.add_field(name="Points", value=str(points), inline=False)
            e.add_field(name="Start Date", value=start_date, inline=False)
            e.add_field(name="Due Date", value=due_date, inline=False)

            discussions_category = discord.utils.get(interaction.guild.categories, name='Discussions')
            if discussions_category is None:
                discussions_category = await interaction.guild.create_category('Discussions')

            new_discussion_channel = await interaction.guild.create_text_channel(f"{self.children[0].value}",
                                                                      category=discussions_category)

            await new_discussion_channel.send(embed=e)

            new_discussion = Discussion(title=title, start=str(start_date),
                                        due=str(due_date), points=points,
                                        channel=new_discussion_channel.id)

            await api.create_discussion(new_discussion, server_id=str(interaction.guild_id))

            await interaction.response.send_message('Discussion channel created.')

    modal = DiscussionModal(title="Creating a Discussion")
    return modal
