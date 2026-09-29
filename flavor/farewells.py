import random

FAREWELLS=[
    "Are you kitting me? I can't believe you're leaving!",
    "Hope to catch you fur-round later!",
    "It’s been paws-itively great knowing you. See you soon!",
    "Have a paws-some next adventure!",
    "Paw-don me, but I’ve gotta go!",
    "Meow for now!",
    "Purr-haps I’ll see you later!",
    "Stay pawsitive—see you soon!",
    "Fur now, farewell!",
    "Gotta scat—catch you later!",
    "Whisker you later!",
    "Paws and reflect until next time!",
    "Don’t be a stranger—come back and purr!",
    "I’m feline a little sad to go. Bye fur now!"
]

def get_random_farewell() -> str:
    return FAREWELLS[random.randint(0, len(FAREWELLS)-1)]
