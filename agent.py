import sys, os, json
from dotenv import load_dotenv
from openai import OpenAI

from flavor.colors import COLORS

from termcolor import colored

from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function
from config import (
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    MAX_LLM_ITERATIONS,
)

def generate_content(client, messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=available_functions
    )

    answer = response.choices[0].message

    if not response.usage:
        raise RuntimeError("Missing answer usage metadata - possible failed API request")

    return (answer, response.usage)


def llm_interaction_flow(local:bool, verbose:bool, messages, working_directory:str):
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

    answer_found = False
    for iteration_number in range(MAX_LLM_ITERATIONS):
        answer, usage = generate_content(client, messages, model)
        messages.append(answer)
        tool_calls =  answer.tool_calls

        if not tool_calls or len(tool_calls) == 0:
            print(colored(f"\n{answer.content.strip()}", COLORS.CHAT))
            answer_found = True
        else:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments or "{}")

                if verbose:
                    print(colored(f"{iteration_number+1}/{MAX_LLM_ITERATIONS}: ", COLORS.ITERATION_COUNTER)+colored(f"Calling {function_name}({function_args})...", COLORS.FUNCTION_CALLING))
                else:
                    args_as_string = json.dumps(function_args)
                    print(colored(f"{iteration_number+1}/{MAX_LLM_ITERATIONS}: ", COLORS.ITERATION_COUNTER)+colored(f"Calling {function_name}({args_as_string[:100]+("..." if len(args_as_string)>100 else "")})...", COLORS.FUNCTION_CALLING))


                tool_result = call_function(tool_call=tool_call, working_directory=working_directory, verbose=verbose)

                # if not tool_result['content'] or tool_result['content'] == "":
                #     raise Exception("Empty call function result content")

                if verbose:
                    print(colored(f"{tool_result['content']}", COLORS.VERBOSE))

                messages.append(tool_result)

        if verbose:
            print(colored(f"Prompt tokens: {usage.prompt_tokens}", COLORS.VERBOSE))
            print(colored(f"Response tokens: {usage.completion_tokens}", COLORS.VERBOSE))

        if answer_found:
            break

    if not answer_found:
        print(colored(f"Maximum number of iterations threshold ({MAX_LLM_ITERATIONS}) reached!", COLORS.ERROR))
