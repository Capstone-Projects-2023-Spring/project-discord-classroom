import random

def handle_command(message) -> str:
    command = message.lower()

    if command == 'hello':
        return 'Hey there!'

    if command == 'roll':
        return str(random.randint(1, 6))

    if command == 'help':
        return "I can't help you right now."
