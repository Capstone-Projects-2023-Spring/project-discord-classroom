import api
import re


async def add_member_to_table(guild_id, role, nick, discord_id):
    # Obtain classroom ID
    response = await api.get_classroom_id(server_id=guild_id)
    classroom_id = response['id']

    # Query 'User' table for member and create row if member is not found
    response = await api.get_user_id(discord_id=discord_id)
    if 'message' in response:
        response = await api.create_user(nick=nick, discord_id=discord_id)
    user_id = response['id']

    # Create new row for member in 'Classroom User' table
    await api.create_classroom_user(classroom_id=classroom_id, user_id=user_id, name=nick, role=role)


async def increment_attendance(discord_user_id: int, discord_server_id: int):
    request = await api.get_user_id(discord_user_id)
    user_id = request['id']
    request = await api.get_classroom_id(discord_server_id)
    classroom_id = request['id']
    request = await api.get_user_attendance(user_id, classroom_id)
    current_attendance = request['attendance']
    # print(current_attendance)
    if current_attendance is not None:
        await api.update_user_attendance(current_attendance, user_id, classroom_id)


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix


def get_ordinal_number(user_input: str) -> str:
    try:
        num = int(user_input[:-2])
        suffix = user_input[-2:]
        expected_suffix = ordinal(num)[-2:]
        if suffix == expected_suffix:
            return user_input
        else:
            raise ValueError("Invalid ordinal number")
    except ValueError:
        try:
            num = int(user_input)
            return ordinal(num)
        except ValueError:
            raise ValueError("Invalid input")

def to_discord_channel_name(name: str) -> str:
    # Convert the string to lowercase
    name = name.lower()

    name = name.replace(" ", "-")

    # Replace non-alphanumeric characters (excluding '-') with dashes
    name = re.sub(r"(?:(?<=\w)|(?<=\W))(?:(?<!:)\W(?!\w)|(?<!\w)\W(?!\w))(?:(?<=\w)|(?<=\W))", "-", name)

    # Remove any leading or trailing dashes
    name = name.strip("-")

    # Discord channel names have a maximum length of 100 characters
    return name[:100]