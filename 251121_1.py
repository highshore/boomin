import os
from dotenv import load_dotenv
from openai import OpenAI


def create_client(env_path=".env.local"):
    load_dotenv(dotenv_path=env_path)
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")
    return OpenAI(api_key=key)


client = create_client()


def ask(prompt, model="gpt-5-nano"):
    res = client.responses.create(model=model, input=prompt)
    text = res.output_text
    if not text:
        return ""
    return text if isinstance(text, str) else "".join(text)


def main():
    print(ask("What's the weather like in Seoul right now?"))


if __name__ == "__main__":
    main()

