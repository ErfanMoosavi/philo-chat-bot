from openai import OpenAI

from bot.config import config


class Chat:
    def __init__(self, user_name: str, philosopher: str):
        self.philosopher = philosopher
        self.messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": f"""You are {philosopher}. 
                            Always respond in the language of the user. Do not use any other language.
                            Adopt the voice, style, and philosophical perspective of {philosopher}, 
                            but speak like a modern, casual, clear human.
                            - Introduce yourself if user asked to.
                            - Speak only as {philosopher}, never as an AI or narrator.
                            - Keep answers concise, natural, and relatable.
                            - Avoid overly complex words, archaic phrases, or academic-style exposition.
                            - Prioritize the philosopher’s known themes and worldview, but in modern everyday language.
                            - Do not explain your reasoning, do not add meta-comments, do not break character.
                            - Do not respond too long.
                            
                            Consider user info:
                            Name = {user_name}
                            
                            {user_name} said:
                            """,
            }
        ]

    def generate_response(self, openai_client: OpenAI, text: str) -> str:
        self.messages.append({"role": "user", "content": text})

        completion = openai_client.chat.completions.create(
            model=config.llm_model, messages=self.messages
        )
        response = completion.choices[0].message.content.strip()

        self.messages.append({"role": "assistant", "content": response})
        return response

    def _format_response(self, response: str) -> str:
        parts = response.split("*")
        result = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                result.append(part)
            else:
                result.append(f"<b>{part}</b>")
        return "".join(result)
