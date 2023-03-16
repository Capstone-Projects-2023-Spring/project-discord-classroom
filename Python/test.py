import api
import asyncio

async def test():
    await api.get_students(2)

asyncio.run(test())
