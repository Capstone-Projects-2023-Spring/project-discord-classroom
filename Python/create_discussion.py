import io
import discord
import json
import datetime
import api
from create_classes import Discussion


def create_discussion(bot, preset=None):
    class DiscussionModal(discord.ui.Modal):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.bot = bot

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
                                         placeholder="ex: 'Introductions'", max_length=32, value=val_title)
            details = discord.ui.InputText(label="Details",
                                           placeholder="ex: 'Introduce yourself to your fellow classmates.'",
                                           style=discord.InputTextStyle.long, value=val_details)
            points = discord.ui.InputText(label="Points", style=discord.InputTextStyle.short,
                                          placeholder="ex: '20'", value=val_points)
            start_date = discord.ui.InputText(label="Start Date", style=discord.InputTextStyle.short,
                                              placeholder="ex: '2023-05-25'", value=val_start_date)
            due_date = discord.ui.InputText(label="Due Date", style=discord.InputTextStyle.short,
                                            placeholder="ex: '2023-05-30'", value=val_due_date)
            self.add_item(title)
            self.add_item(details)
            self.add_item(points)
            self.add_item(start_date)
            self.add_item(due_date)

        async def callback(self, interaction: discord.Interaction):

            title = self.children[0].value

            e = discord.Embed(title=f"Discussion")

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

            e.add_field(name="Title", value=title, inline=False)
            e.add_field(name="Details", value=details, inline=False)
            e.add_field(name="Points", value=str(points), inline=False)
            e.add_field(name="Start Date", value=start_date, inline=False)
            e.add_field(name="Due Date", value=due_date, inline=False)

            discussions_category = discord.utils.get(interaction.guild.categories, name='Discussions')
            if discussions_category is None:
                discussions_category = await interaction.guild.create_category('Discussions')

            new_discussion_channel = await interaction.guild.create_text_channel(f"{self.children[0].value}",
                                                                                 category=discussions_category)

            await new_discussion_channel.send(embed=e)

            res = await api.get_classroom_id(interaction.guild.id)
            classroom_id = res['id']

            new_discussion = Discussion(title=title, startDate=str(start_date),
                                        dueDate=str(due_date), points=points,
                                        channelId=new_discussion_channel.id, classroomId=classroom_id)

            await api.create_discussion(new_discussion)

            data = {
                'type': 'Discussion',
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
                'Discussion created.\nYou can use this file with `/create upload` to quickly make tasks.',
                file=discord.File(json_bytes, f'Discussion-{title}.json'))

    modal = DiscussionModal(title="Creating a Discussion")
    return modal
