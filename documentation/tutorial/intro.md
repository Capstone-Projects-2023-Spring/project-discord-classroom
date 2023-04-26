---
sidebar_position: 1
---

## Getting Started

Get started by cloning the **[repository](https://github.com/Capstone-Projects-2023-Spring/project-discord-classroom)**.

### What you'll need

- [Python](https://www.python.org/downloads/) version 3.8 or above

- [Discord Bot Token](https://discord.com/developers/applications)
  - For a guide to create a discord application [click here](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot)

- [Supabase Token](https://supabase.com/)
  - For a guide to create a supabase project [click here](https://egghead.io/lessons/supabase-create-a-new-supabase-project)

- [OpenAI API Token](https://openai.com/)
  - For a guide to generate an OpenAI Token [click here](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/)

## Setting up the enviornment

**Navigate to the Python folder**

Install requirements with
`pip install -r requirements.txt`

**Create a file instead of the Python folder called config.json**

The config.json should contain five values: DiscordToken, Prefix, SupaUrl, SupaKey, GPTKey

For example: {"DiscordToken": "xxx", "Prefix": "x", "SupaUrl": "xxx", "SupaKey": "xxx", "GPTKey": "xxx"}

DiscordToken is the Discord Bot Token, Prefix is any character use for bot commands, SupaUrl is the Supabase project URL, SupaKey is the Supabase project key, and GPTKey is the OpenAI API token.


## Start up the bot

In the Python directory run:
`python3 main.py`

Congradulations! Your Classroom Bot is now running!
