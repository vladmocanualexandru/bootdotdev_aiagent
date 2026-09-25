import sys, os, argparse, json
from dotenv import load_dotenv
from openai import OpenAI

from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function
from config import (
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)

def generate_content(client, messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=available_functions
    )

    answer = response.choices[0].message
    content = answer.content
    tool_calls = answer.tool_calls

    if not response.usage:
        raise RuntimeError("Missing answer usage metadata - possible failed API request")

    return (content, tool_calls, {"prompt_tokens":response.usage.prompt_tokens, "completion_tokens":response.usage.completion_tokens})

def generate_content_mock():
    return ("LLM API CALL SKIPPED", None, {"prompt_tokens":0, "completion_tokens":0})

def main():
    if len(sys.argv) <= 1:
        print("AI Agent app")
        print('Usage: python main.py "<user prompt>" [--verbose, --mock, --local]')
        print('Example: python main.py "How do you make lemonade? Just the ingredients, 10 words max."')
        print('[--verbose: Enable verbose output]')
        print('[--mock: If set to true, LLM API call will be skipped]')
        print('[--local: Use the local Ollama model instead of OpenRouter]')
        return

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--mock", action="store_true", help="If set to true, LLM API call will be skipped")
    parser.add_argument("--local", action="store_true", help="Use the local Ollama model instead of OpenRouter")
    args = parser.parse_args()

    user_prompt:str = args.user_prompt
    verbose:bool = args.verbose
    mock:bool = args.mock
    local:bool = args.local

    load_dotenv()

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
        {"role": "user", "content": user_prompt},
    ]

    answer, tool_calls, usage_meta = generate_content(client, messages, model) if not mock else generate_content_mock()

    if not tool_calls or len(tool_calls) == 0:
        print(f"Answer: {answer}")
    else:
        for tool_call in tool_calls:
            result = call_function(tool_call=tool_call, verbose=verbose)

            if not result['content'] or result['content'] == "":
                raise Exception("Empty call function result content")

            if verbose:
                print(f"-> {result['content']}")


    if verbose:
        print(f"Model: {model}")
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage_meta["prompt_tokens"]}")
        print(f"Response tokens: {usage_meta["completion_tokens"]}")

if __name__ == "__main__":
    main()
