from random import random
import sys, os, argparse
from dotenv import load_dotenv
from openai import OpenAI

from flavor.logo import LOGO
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
    MAX_LLM_ITERATIONS
)

def generate_content(client, messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=available_functions
    )

    answer = response.choices[0].message
    # content = answer.content
    # tool_calls = answer.tool_calls

    if not response.usage:
        raise RuntimeError("Missing answer usage metadata - possible failed API request")

    # return (content, tool_calls, {"prompt_tokens":response.usage.prompt_tokens, "completion_tokens":response.usage.completion_tokens})
    return (answer, response.usage)

def llm_interaction_flow(local:bool, verbose:bool, prompt:str, working_directory:str):
    if local:
        model = OLLAMA_MODEL
        client = OpenAI(
            base_url=OLLAMA_BASE_URL,
            api_key="ollama",  # Ollama ignores this, but the OpenAI client requires a value
        )
    else:
        api_key = os.environ.get("OPENROUTER_API_KEY")

        if not api_key:
            raise RuntimeError("Missing OpenRouter API key - create a new one and add it to .env as value for OPENROUTER_API_KEY")

        model = OPENROUTER_MODEL
        client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=api_key,
        )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    answer_found = False
    for _ in range(MAX_LLM_ITERATIONS):
        answer, usage = generate_content(client, messages, model)
        messages.append(answer)
        tool_calls =  answer.tool_calls

        if not tool_calls or len(tool_calls) == 0:
            print(colored(f"{answer.content}", COLORS.CHAT))
            answer_found = True
            break
        else:
            for tool_call in tool_calls:
                tool_result = call_function(tool_call=tool_call, working_directory=working_directory, verbose=verbose)

                # if not tool_result['content'] or tool_result['content'] == "":
                #     raise Exception("Empty call function result content")

                if verbose:
                    print(f"-> {tool_result['content']}")

                messages.append(tool_result)

        if verbose:
            print(f"Prompt tokens: {usage.prompt_tokens}")
            print(f"Response tokens: {usage.completion_tokens}")

    if not answer_found:
        print(f"Maximum number of iterations threshold ({MAX_LLM_ITERATIONS}) reached!")

def main():
    load_dotenv()

    print(LOGO)
    print(colored(get_random_greeting(), COLORS.CHAT))

    verbose = False
    local = False
    working_directory = "./calculator"

    prompt = input("> ")
    while not prompt.startswith("/q"):
        if prompt.startswith("/v"):
            verbose = not verbose
            print(colored(f"\nVerbose mode {verbose}", COLORS.CHAT))
        elif prompt.startswith("/l"):
            local = not local
            print(colored(f"\nLocal model mode {local}", COLORS.CHAT))
        elif prompt.startswith("/w"):
            working_directory = prompt.split(" ")[1]
            print(colored(f"\nWorking directory set to {working_directory}", COLORS.CHAT))
        elif not prompt.startswith("/"):
            print(colored(f"\n{get_random_activity()}...", COLORS.FLAVOR_ACTIVITY))
            llm_interaction_flow(local, verbose, prompt, working_directory)

        prompt = input("> ")

    print(f"\n{colored(get_random_farewell(), COLORS.CHAT)}")

    sys.exit(0)

if __name__ == "__main__":
    main()
