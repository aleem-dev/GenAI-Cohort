import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o") #getting the encoder gpt-4o

text = "Hello, I am Aleem Shaikh"
tokens = enc.encode(text)

print("Tokens:", tokens)