from app.ai.models.together import TogetherLLM


llm = TogetherLLM()

response = llm.generate(
    [
        {
            "role": "system",
            "content": "You are a helpful employee assistant.",
        },
        {
            "role": "user",
            "content": "Say hello in one short sentence.",
        },
    ]
)

print(response)