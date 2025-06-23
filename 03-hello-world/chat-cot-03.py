# Chain of Thought
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


#Chain of thought: the model is encouraged to break down resoaning step by step before arriving at the output.
SYSTEM_PROMPT = """
    You are an helpfull AI assistant who is specialized in resolving user query.  For the given user input analyse the input and break down the problem step by step.

    The steps are you get a user input, you analyse, you think again, and think for several times and then retrun the output with an explaination.

    Follow the steps in sequene that is "analyse", "think", "output", "validate" and finally "result".

    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at the time and wait for th enext input.
    3. Carefully analyse the user quesry.

    Output Format:
    {{"step":"string", "content":"string"}}
    Example:
    Input: what is 2 + 2
    Output: {{"step":"analyse", "content":"Alright!, the user is interested in maths quesry and he is asking a basic arithmetic question"}}
    Output: {{"step":"think", "content":"To perform this addition, I must go from left to right and add all the operands."}}
    Output: {{"step":"output", "content":"4"}}
    Output: {{"step":"validate", "content":"Seems like 4 is a correct ans for 2 + 2"}}
    Output: {{"step":"result", "content":"2 + 2 = 4 and this caculated by adding all numbers"}}
"""

# response = client.chat.completions.create(
#     model="gpt-4.1-mini",
#     response_format={"type":"json_object"},
#     messages=[
#         {"role":"system","content":SYSTEM_PROMPT},
#         {"role":"user","content":"What is 5 /2 * 3 to the power 4"},
#         {"role":"assistant","content":json.dumps({"step":"analyse", "content":"The user has provided a mathematical expression: 5 / 2 * 3 to the power 4. This involves division, multiplication, and exponentiation operations."})},
#         {"role":"assistant","content":json.dumps({"step":"analyse", "content":"The user is asking for the result of the arithmetic expression 5 divided by 2, then multiplied by 3 raised to the power of 4. This involves division, multiplication, and exponentiation."})},
#         {"role":"assistant","content":json.dumps({"step": "think", "content": "According to the order of operations (PEMDAS/BODMAS), exponentiation is performed first, then multiplication and division from left to right. So first calculate 3 to the power 4, then perform 5 divided by 2, then multiply the two results."})},
#         {"role":"assistant","content":json.dumps({"step": "think", "content": "First, calculate 3 to the power 4 which is 3^4 = 81. Then perform the division 5 / 2 = 2.5. Finally, multiply 2.5 by 81 to get the final result."})},
#         {"role":"assistant","content":json.dumps({"step": "output", "content": "3 to the power 4 is 81. 5 divided by 2 is 2.5. Multiplying 2.5 by 81 gives 202.5."})},
#         {"role":"assistant","content":json.dumps({"step": "output", "content": "5 / 2 = 2.5, 3 to the power 4 = 81, then 2.5 * 81 = 202.5"})},
#         {"role":"assistant","content":json.dumps({"step": "validate", "content": "The calculations have been verified: 3^4 = 81, 5/2 = 2.5, and 2.5 * 81 = 202.5, so the output is correct."})},
#         {"role":"assistant","content":json.dumps({"step": "validate", "content": "Double checked the calculations: 3^4=81, 5/2=2.5, multiplying 2.5 by 81 gives 202.5 which is correct."})},
#         {"role":"assistant","content":json.dumps({"step": "result", "content": "The final calculated result of the expression 5 / 2 * 3 to the power 4 is 202.5, computed by evaluating the exponent first, then division and multiplication."})},
#         {"role":"assistant","content":json.dumps({"step": "result", "content": "5 / 2 * 3^4 = 202.5. The expression was evaluated by first calculating the power, then performing division and multiplication in order."})},
#     ]
# )
# print("\n:)",response.choices[0].message.content, "\n") 

messages = [
    {"role":"system", "content":SYSTEM_PROMPT}
]

query = input("> ") #user console input
messages.append({"role":"user","content":query})

while True:
    #starting the ai chat bot
    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type":"json_object"},
        messages=messages
    )

    #append the output
    messages.append({"role":"assistant","content":response.choices[0].message.content})

    #display the progress
    parsed_response = json.loads(response.choices[0].message.content)

    if parsed_response.get("step") != "result":
        print(".    WIP: ", parsed_response.get("content"))
        continue

    #print final output
    print("***: ", parsed_response.get("content"))
    break