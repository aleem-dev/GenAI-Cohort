from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Few-shot prompting: here we also give example with the prompt so that it can give much better output

#exmaple
SYSTEM_PROMPT = """
    You are an AI expert in coding.  You only know Python and nothing else. You help users in solving there python douts only and noting else.  If user tried to ask something else apart from Python you can just dont roast them.

    Examples:
    user: How to make a tea?
    assistant: some polite answer

    Examples:
    user: How to write a function in python
    assistant: def fn_name(x:int) -> int: pass# logic of the function
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"My name is aleem, can you tell me about dictionary in python a breif tutorial"},
        {"role":"assistant","content":"explaination given by the model"},
        {"role":"user","content":"How to make a tea"},
        
        
        
                
    ]
)
print(response.choices[0].message.content) 

# you can take a look at vercel v0 system prompt, and have a habit to read the system prompt.. that will help to go extra mile as developer

# Always use examples, as you can see in above system prompt we have rood prompt example.. if we change the eample the behaviour of the ai will change.  Go to Vercel V0 system prompt and read the examples they have used.