# Multi model agent with console formatting and model routing ✨
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are an helpfull AI assistant who is specialized in resolving user query. For the given user input analyse the input and break down the problem step by step.

The steps are: "analyse", "think", "output", "validate", and "result".

Rules:
1. Output MUST follow JSON format: {"step":"...", "content":"..."}
2. Only one step at a time.
3. Carefully analyse user input before proceeding.

Example:
Input: what is 2 + 2
→ {"step":"analyse", "content":"The user is asking a basic arithmetic question"}
→ {"step":"think", "content":"To solve 2 + 2, I add both numbers"}
→ {"step":"output", "content":"4"}
→ {"step":"validate", "content":"4 is correct for 2 + 2"}
→ {"step":"result", "content":"The answer is 4, calculated by basic addition."}
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

query = input("📝 Prompt: ")
print(f"\n🧾 Question: {query}")
messages.append({"role": "user", "content": query})
current_step = None

emojis = {
    "analyse": "🧠",
    "think": "🧠",
    "output": "🧠",
    "validate": "🧠",
    "result": "🤖"
}

while True:
    # Select model based on step
    if current_step == "result":
        model = "gpt-4.1"
    elif current_step in ["output", "validate"]:
        model = "gpt-4.1-mini"
    else:
        model = "gpt-4.1-nano"

    # API call
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=messages
    )

    content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": content})

    try:
        parsed = json.loads(content)
        current_step = parsed.get("step")
        step_content = parsed.get("content")
        emoji = emojis.get(current_step, "💬")

        if current_step == "result":
            print(f"\n{emoji} RESULT: {step_content}")
        else:
            print(f"\t{emoji} {current_step.upper()}: {step_content}")
    except Exception as e:
        print("⚠️ Failed to parse:", e)
        break

    # After final result, ask next steps
    if current_step == "result":
        print("\n✅ Completed.")
        followup = input("📌 Do you have another question related to this topic? (yes/no): ").strip().lower()

        if followup == "yes":
            more = input("💬 Add info or new follow-up: ")
            messages.append({"role": "user", "content": more})
            continue

        new_topic = input("🆕 Want to start a new topic? (yes/no): ").strip().lower()
        if new_topic == "yes":
            query = input("📝 New prompt: ")
            print(f"\n🧾 Question: {query}")
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.append({"role": "user", "content": query})
            current_step = None
            continue

        print("👋 See you next time!")
        break
