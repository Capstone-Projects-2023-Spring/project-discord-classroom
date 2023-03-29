import api

async def add_member_to_table(guild_id, role, nick, discord_id):
        classroom_id = await get_classroom_id(server_id=guild_id)

        # Query 'User' table for member
        response = await get_user_id(discord_id=discord_id)
        if 'message' in response:
            response = await create_user(nick=nick, discord_id=discord_id)
        user_id = response['user_id']

        # Create new row for member in 'Classroom User' table
        await create_classroom_user(classroom_id=classroom_id, user_id=user_id, name=nick, role=role)