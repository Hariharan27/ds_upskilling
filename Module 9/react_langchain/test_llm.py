from app.agent import create_llm

llm = create_llm()

response = llm.invoke("Say hello in one sentence.")

print(response.content)