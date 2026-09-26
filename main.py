import sys, os, argparse
from dotenv import load_dotenv
from openai import OpenAI

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

def main():
    if len(sys.argv) <= 1:
        print("AI Agent app")
        print('Usage: python main.py "<user prompt>" [--verbose, --mock, --local]')
        print('Example: python main.py "How do you make lemonade? Just the ingredients, 10 words max."')
        print('[--verbose: Enable verbose output]')
        print('[--local: Use the local Ollama model instead of OpenRouter]')
        return

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--local", action="store_true", help="Use the local Ollama model instead of OpenRouter")
    args = parser.parse_args()

    user_prompt:str = args.user_prompt
    verbose:bool = args.verbose
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

    answer_found = False
    for _ in range(MAX_LLM_ITERATIONS):
        answer, usage = generate_content(client, messages, model)
        messages.append(answer)
        tool_calls =  answer.tool_calls

        if not tool_calls or len(tool_calls) == 0:
            print(f"Answer: {answer.content}")
            answer_found = True
            break
        else:
            for tool_call in tool_calls:
                tool_result = call_function(tool_call=tool_call, verbose=verbose)

                if not tool_result['content'] or tool_result['content'] == "":
                    raise Exception("Empty call function result content")

                if verbose:
                    print(f"-> {tool_result['content']}")

                messages.append(tool_result)

        if verbose:
            # print(f"Model: {model}")
            # print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {usage.prompt_tokens}")
            print(f"Response tokens: {usage.completion_tokens}")

    if not answer_found:
        print(f"Maximum number of iterations threshold ({MAX_LLM_ITERATIONS}) reached!")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
