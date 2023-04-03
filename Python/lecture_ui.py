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
import io
import re

class TakeQuiz(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label="Take Attendance", emoji="📋", custom_id="attendance")
    async def attendance_button_callback(self, button, interaction):
        pass

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label="Mute All", emoji="🔇", custom_id="mute")
    async def mute_button_callback(self, button, interaction):
        pass

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label="Breakout Rooms", emoji="🚪", custom_id="rooms")
    async def rooms_button_callback(self, button, interaction):
        pass

    @discord.ui.button(row=0, style=discord.ButtonStyle.secondary, label="Breakout Rooms", emoji="🚪", custom_id="rooms")
    async def rooms_button_callback(self, button, interaction):
        pass
