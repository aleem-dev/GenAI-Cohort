from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"user","content":"My name is aleem"},
        {"role":"assistant","content":"Hi Aleem"},
        {"role":"user","content":"What is my name?"},
        {"role":"assistant","content":"Your name is Aleem."},
        {"role":"user","content":"How are you?"},
    ]
)

print(response.choices[0].message.content) 