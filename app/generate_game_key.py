import random
import string

def generate_game_key(length: int = 6) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))
