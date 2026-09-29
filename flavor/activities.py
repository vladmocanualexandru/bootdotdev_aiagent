import random

ACTIVITIES=[
    "Occupying the keyboard",
    "Assessing the box",
    "Zooming at 3am",
    "Staring into the void",
    "Relocating to the sunbeam",
    "Knocking things off the edge",
    "Forming a loaf",
    "Composing a hairball",
    "Blinking judgmentally",
    "Retracting toe beans",
    "Hunting the laser dot",
    "Scaling the curtains",
    "Invading a lap",
    "Negotiating with purrs",
    "Manipulating for treats",
    "Chittering at birds",
    "Transcending on catnip",
    "Kneading biscuits",
    "Slow-blinking",
    "Demanding chin scratches",
    "Ambushing the feather toy",
    "Surveilling from the windowsill",
    "Shredding cardboard",
    "Flicking my tail",
    "Ignoring the human",
    "Evading the vet carrier",
    "Setting the belly trap",
    "Counter-surfing",
    "Commandeering the laptop",
    "Yowling at 5am",
]

def get_random_activity() -> str:
    return ACTIVITIES[random.randint(0, len(ACTIVITIES)-1)]
