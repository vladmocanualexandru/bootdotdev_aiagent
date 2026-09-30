import sys, os, json
from dotenv import load_dotenv
from openai import OpenAI

from agent import llm_interaction_flow

from flavor.interface import LOGO, HELP
from flavor.colors import COLORS
from flavor.greetings import get_random_greeting
from flavor.farewells import get_random_farewell
from flavor.activities import get_random_activity

from termcolor import colored

from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function
from config import (
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    MAX_LLM_ITERATIONS,
    WORKING_DIRECTORY_PREFIX
)

def main():
    load_dotenv()

    print(LOGO)
    print(HELP)
    print(colored(get_random_greeting(), COLORS.CHAT))

    verbose = False
    local = False
    working_directory = WORKING_DIRECTORY_PREFIX

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    prompt = input("> ")

    while not prompt.startswith("/q"):
        if prompt.startswith("/r"):
            print(colored("\nConversation reset", COLORS.CHAT))
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        if prompt.startswith("/h"):
            print(HELP)
        if prompt.startswith("/v"):
            verbose = not verbose
            print(colored(f"\nVerbose mode {verbose}", COLORS.CHAT))
        elif prompt.startswith("/l"):
            local = not local
            print(colored(f"\nLocal model mode {local}", COLORS.CHAT))
        elif prompt.startswith("/w"):
            working_directory = f"{WORKING_DIRECTORY_PREFIX}/{prompt.split(" ")[1]}"
            print(colored(f"\nWorking directory set to {working_directory}", COLORS.CHAT))
        elif not prompt.startswith("/"):
            messages.append({"role": "user", "content": prompt})
            print(colored(f"\n{get_random_activity()}...", COLORS.FLAVOR_ACTIVITY))
            llm_interaction_flow(local, verbose, messages, working_directory)

        prompt = input("> ")

    print(f"\n{colored(get_random_farewell(), COLORS.CHAT)}")

    sys.exit(0)

if __name__ == "__main__":
    main()
