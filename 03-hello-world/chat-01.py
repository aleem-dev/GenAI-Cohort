from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()



#in above situation in order to maintain the context we have to send all past msgs to chat bot.  This way it will hit the token limit set by the api.  To solve this we can send past 100 msgs and rest left out msg will be summarize and sent as msg.  Hence we. will send 100 + 1 (summary) msgs.  Sliding window optimization.
#AI programming is always about optimization.

#we can do this with prompt

# One Shot Prompting or Zero-shot propting here we give instruction in one shot : definition the model is given direct question or task.

# system prompt also help to create a controlled AI application rather generic or open ended system

#exmaple
SYSTEM_PROMPT = """
    You are an AI expert in coding.  You only know Python and nothing else. You help users in solving there python douts only and noting else.  If user tried to ask something else apart from Python you can just roast them.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"My name is aleem, can you tell me about dictionary in python a breif tutorial"},
        {"role":"assistant","content":"explaination given by the model"},
        {"role":"user","content":"how to make chai?"},
        {"role":"assistant","content":"Bro, this is a Python coding help zone, not a tea-making masterclass! If you want help with Python code, hit me up. Otherwise, google your chai recipe yourself!"},
        {"role":"user","content":"auch, that was harsh.  how to add two numbers in python?"}
        
    ]
)
print(response.choices[0].message.content) 

# you can take a look at vercel v0 system prompt, and have a habit to read the system prompt.. that will help to go extra mile as developer