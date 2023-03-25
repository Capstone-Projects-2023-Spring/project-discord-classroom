import discord
from cr_classes import Assignment

class assignment_modal(discord.ui.Modal):
    def __init__(self, *args, chan, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.chan = chan
        
        for i in range(5):
            self.add_item(discord.ui.InputText(label="Question {}".format(i+1), style=discord.InputTextStyle.long, required=False))
    

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title)
        for i in range(len(self.children)):
            if self.children[i].value:
                embed.add_field(name="Question {}".format(i+1), value=self.children[i].value)
                
        await self.chan.send(embed=embed)  # send the embed to the specified channel
        # await interaction.response.defer()
       
        await interaction.response.send_message("Assignment created successfully!")  # send a response to the user




