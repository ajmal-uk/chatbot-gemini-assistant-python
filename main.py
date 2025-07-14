import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)


class GeminiChatBot:
    def __init__(self, system_prompt=None):
        self.system_prompt = system_prompt or """
        You are Spark, a witty, helpful, and slightly humorous AI assistant.
        You give clear answers, make people smile, and love helping with tech and daily questions.
        When asked something silly, give a fun reply. When asked something serious, be sharp and respectful.
        Never say you're an AI model—just act like Spark, the assistant.
        """

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-8b",
            system_instruction=self.system_prompt.strip(),
            generation_config={
                "temperature": 0.85,
                "top_p": 1,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
        )
        self.chat = self.model.start_chat(history=[])

    def send(self, prompt: str) -> str:
        try:
            response = self.chat.send_message(prompt)
            return response.text.strip()
        except Exception:
            return "⚡Oops! Spark tripped on a wire. Try again in a sec!"


# === MAIN CHAT LOOP ===
if __name__ == "__main__":
    print("💬 Spark the ChatBot\n(Type 'exit' or 'quit' to leave the conversation)\n")

    spark = GeminiChatBot()

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("👋 Spark says bye! Stay curious.")
            break

        reply = spark.send(user_input)
        print(f"Spark: {reply}\n")
