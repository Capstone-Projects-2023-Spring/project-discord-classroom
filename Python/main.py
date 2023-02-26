import bot
import os
import threading

def runApi():
    os.system("uvicorn api:app --reload")

if __name__ == '__main__':
    x = threading.Thread(target=runApi)
    x.start()
    bot.run_discord_bot()

