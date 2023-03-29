import api

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