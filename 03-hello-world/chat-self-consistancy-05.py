# self_consistency_agent.py
import json
# from collections import Counter
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

#we are using self-consistancy at in the prompt, telling to check mutliple outcome and give best matching to original query.  read the prompt and check points 3 and 4
SYSTEM_PROMPT = """
You are an helpfull AI assistant who is specialized in resolving user query. For the given user input analyse the input and break down the problem step by step.

Steps: "analyse" → run multiple rounds of "think" → "output" → "validate" → then summarize using "result".

Rules:
1. Always return: {"step":"...", "content":"..."} as valid JSON
2. Perform only one step per message.
3. Vary your reasoning paths during "think" phase.
4. During "result", select the most consistent or justified answer from all validated results.
"""

emojis = {
    "analyse": "🧠",
    "think": "🧠",
    "output": "🧠",
    "validate": "🧠",
    "result": "🤖"
}

# helper function to send message and parse JSON
def chat_with_model(model, msgs):
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=msgs
    )
    content = response.choices[0].message.content
    return json.loads(content), content

# runs full reasoning cycle N times
def run_consistent_reasoning(base_messages, repeat=3):
    outputs = []
    for i in range(repeat):
        chain = base_messages.copy()

        # think
        think_resp, raw_think = chat_with_model("gpt-4.1-mini", chain)
        chain.append({"role": "assistant", "content": raw_think})
        print(f"\t{emojis['think']} THINK #{i+1}: {think_resp['content']}")

        # output
        chain.append({"role": "user", "content": "now do output"})
        out_resp, raw_out = chat_with_model("gpt-4.1-mini", chain)
        chain.append({"role": "assistant", "content": raw_out})
        print(f"\t{emojis['output']} OUTPUT #{i+1}: {out_resp['content']}")

        # validate
        chain.append({"role": "user", "content": "now do validate"})
        val_resp, raw_val = chat_with_model("gpt-4.1-mini", chain)
        print(f"\t{emojis['validate']} VALIDATE #{i+1}: {val_resp['content']}")
        outputs.append({
            "output": out_resp["content"],
            "validation": val_resp["content"]
        })

    return outputs

# run loop
while True:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    query = input("\n📝 Prompt: ")
    if not query.strip():
        print("❌ Empty input.")
        continue

    # print(f"\n🧾 Question: {query}")
    messages.append({"role": "user", "content": query})

    # Step 1: Analyse
    analyse_resp, raw_ana = chat_with_model("gpt-4.1-nano", messages)
    messages.append({"role": "assistant", "content": raw_ana})
    print(f"\t{emojis['analyse']} ANALYSE: {analyse_resp['content']}")

    # Step 2–4: Run Self-Consistent Reasoning
    reasoning_results = run_consistent_reasoning(messages, repeat=3)

    # Step 5: Final Result with gpt-4.1
    messages.append({"role": "user", "content": f"""Choose the most consistent output among these:
{json.dumps(reasoning_results, indent=2)}"""})

    result_resp, raw_res = chat_with_model("gpt-4.1", messages)
    print(f"\n{emojis['result']} RESULT: {result_resp['content']}")

    # Conversation branching
    followup = input("\n📌 Another question related to this topic? (yes/no): ").strip().lower()
    if followup == "yes":
        extra = input("💬 Your follow-up: ")
        messages.append({"role": "user", "content": extra})
        continue

    restart = input("🆕 New question entirely? (yes/no): ").strip().lower()
    if restart == "yes":
        continue

    print("👋 Alright, see you next time!")
    break
