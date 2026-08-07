"""
MODULE 1 · OPTIONAL — the same job through the Claude API.

YOU DO NOT NEED THIS TO COMPLETE THE LAB.
    Steps 1 to 3 run free, with no key and no subscription. This file is the
    instructor demo: it shows what changes when the model is called by code
    instead of by a human pasting into a chat window.

    Read it. You will use this pattern from Module 3 onwards.

WHAT CHANGES WHEN CODE CALLS THE MODEL
    Nothing about the prompt. Everything about the discipline: the same prompt
    runs on every file, unattended, at temperature 0, and every answer lands in
    a file you can audit later.

IF YOU DO HAVE A KEY
    pip install anthropic python-dotenv
    put  ANTHROPIC_API_KEY=sk-ant-...  in a file named .env
    add  .env  to .gitignore BEFORE your first commit
    python3 optional_claude_api.py
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent


def main():
    try:
        import anthropic
        from dotenv import load_dotenv
    except ImportError:
        print(__doc__)
        print("The anthropic package is not installed — that is fine.")
        print("Do the lab with step1, step2 and step3. They need nothing.")
        return

    load_dotenv()
    try:
        client = anthropic.Anthropic()      # reads ANTHROPIC_API_KEY from .env
        client.models.list(limit=1)         # fails fast if there is no key
    except Exception as e:
        print("No usable API key found, so this optional demo cannot run.")
        print(f"  ({type(e).__name__})")
        print("\nThat is expected. Do the lab with step1, step2 and step3 —")
        print("they need no key, no subscription and no internet.")
        return

    prompt = (HERE / "prompt.txt").read_text()
    out_dir = HERE / "output"
    out_dir.mkdir(exist_ok=True)

    for f in sorted((HERE / "excerpts").glob("*.txt")):
        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1500,
            temperature=0,                  # same filing, same answer, every run
            messages=[{
                "role": "user",
                "content": prompt.replace(
                    "<paste the contents of one file from the excerpts folder here>",
                    f.read_text()),
            }],
        )
        text = message.content[0].text
        data = json.loads(text)             # if this throws, the prompt is at fault
        (out_dir / (f.stem + ".json")).write_text(json.dumps(data, indent=2))
        print(f"{f.name:<18} -> output/{f.stem}.json   "
              f"({len(data['periods'])} period(s))")

    print("\nNow run the checker on each one, exactly as in step 2.")
    print("The model being called by code does not make it more trustworthy.")


if __name__ == "__main__":
    main()
