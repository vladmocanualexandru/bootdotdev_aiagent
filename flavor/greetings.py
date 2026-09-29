import random

GREETINGS=[
    "Purr-fect to see you again!",
    "Hope your day is paws-itively wonderful!",
    "Look what the cat dragged in—so glad you're here!",
    "Right meow is a great time to say hello!",
    "Meow there!",
    "Purr-lease to meet you!",
    "Hey there, fur-iend!",
    "Whisker you doing?",
    "Pawsome to see you!",
    "Meowdy, partner!",
    "Hope you’re feline fine!",
    "Well, hello there, handsome paws!",
    "Hey, furball! What’s purring?",
    "Purr-ty good to see you!"
]

def get_random_greeting() -> str:
    return GREETINGS[random.randint(0, len(GREETINGS)-1)]
