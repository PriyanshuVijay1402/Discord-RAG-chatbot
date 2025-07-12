from langchain_huggingface import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="tiiuae/falcon-rw-1b",  # ✅ tested & works
    temperature=0.7,
    max_new_tokens=256
)

response = llm.invoke("What is AI Bootcamp?")
print(response)
