import api
import asyncio

async def test():
    await api.get_question(26)

asyncio.run(test())
