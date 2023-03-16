import api
import asyncio

async def test():
    await api.get_quiz(str(1085416795789340803))

asyncio.run(test())
