from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

text = "dog chases cat"

response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
)

print("Vector Embedding: ",response.data[0].embedding)
print("Length: ",len(response.data[0].embedding))