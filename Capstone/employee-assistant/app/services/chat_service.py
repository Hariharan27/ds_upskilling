from app.ai.models.together import TogetherLLM

class ChatService:
    def __init__(self) -> None:
        self.llm = TogetherLLM()

    def chat(self, message:str) -> str:
        response = self.llm.generate(
            [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful employee assistant. "
                        "Answer clearly and concisely."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ]
        )
        return response