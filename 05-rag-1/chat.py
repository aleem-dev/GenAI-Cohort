from langchain_openai import OpenAIEmbeddings   #Vector Embedding
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore #Store connection
from openai import OpenAI # bot

load_dotenv() # Vectore Embeding
client = OpenAI() # bot

# Note Query, Venctor Embeding, Store Connection, Search Similarity with loop create basic chat bot
# Then we will add the system prompt to it

while True: #looping
    # Query
    print('input your query')
    query = input("> ")

    # Vectore Embeding
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    embeding = embeddings.embed_query(query)

    # Store connection
    vector_store = QdrantVectorStore.from_existing_collection(
        #documents=query,
        url="http://localhost:6333/", #database url
        collection_name = "learning_vector", #database collection name
        embedding=embeddings
    )

    # Search vactore similarity of Query
    results = vector_store.similarity_search_by_vector(embeding)
         
    # **** create chat_agent/bot to help based on context and prompt
    # Context
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in results])

    # Prompt + Context
    SYSTEM_PROMPT = f"""
    You are a helpfull AI Assistant who asnweres user query based on the available context
    retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user
    to open the right page number to know more.

    Context:
    {context}
    """

    # bot call llm
    chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": query },
    ]
    )

    #formated output
    print("\n\nTotal references found:", len(results))

    for i, doc in enumerate(results, start=1):
        print(f"\nReference {i} of {len(results)}")
        print("📖 Response:")
        print(doc.page_content.strip())

        print("\n📄 Page Number:", doc.metadata.get("page_label", "N/A"))
        print("📂 File Location:", doc.metadata.get("source", "N/A"))
        print("👤 Author:", doc.metadata.get("author", "Unknown"))
        print("📚 Total Pages:", doc.metadata.get("total_pages", "N/A"))
        print("🆔 Document ID:", doc.metadata.get("_id", "N/A"))
        print("-" * 80)

    print('Do you have more question with same context?')
    loop_again = input('Y/N >') #Looping
    if 'Y'==loop_again.strip().upper():
        continue
    else:
        break