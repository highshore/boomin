import os

from openai import OpenAI


def main():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")
    client = OpenAI(api_key=key)
    res = client.responses.create(
        model="gpt-5-nano",
        input="Say hello in one sentence."
    )
    print(res.output[0].content[0].text)


if __name__ == "__main__":
    main()

