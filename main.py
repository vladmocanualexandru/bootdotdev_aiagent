import os, argparse
from dotenv import load_dotenv
from openai import OpenAI

def generate_content(client, messages) -> tuple[str, dict[str, int]]:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    answer = response.choices[0].message.content

    if not response.usage:
        raise RuntimeError("Missing answer usage metadata - possible failed API request")

    usage = response.usage

    return (answer, {"prompt_tokens":response.usage.prompt_tokens, "completion_tokens":response.usage.completion_tokens})

def generate_content_mock() -> tuple[str, dict[str, int]]:
    return ("LLM API CALL SKIPPED", {"prompt_tokens":0, "completion_tokens":0})

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("Missing OpenRouter API key - create a new one and add it to .env as value for OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--mock", action="store_true", help="If set to true, LLM API call will be skipped")
    args = parser.parse_args()

    user_prompt:str = args.user_prompt
    verbose:bool = args.verbose
    mock:bool = args.mock

    messages = [
        {"role": "user", "content": user_prompt},
    ]

    answer, usage_meta = generate_content(client, messages) if not mock else generate_content_mock()

    print(f"Answer: {answer}")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage_meta["prompt_tokens"]}")
        print(f"Response tokens: {usage_meta["completion_tokens"]}")



if __name__ == "__main__":
    main()
