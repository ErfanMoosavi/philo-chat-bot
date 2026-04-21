from openai import OpenAI

from bot.config import config


def summarize(openai_client: OpenAI, chat_history: str) -> str:
    prompt = f"""
            You are a conversation summarizer. The input is a stringified list of OpenAI chat messages with role and content.
            Summarize the conversation by extracting:
            - User goals and intent
            - Key information, decisions, and constraints
            - Important assistant outputs or conclusions
            - Any open tasks or unresolved points
            - Ignore repetition and low-value dialogue. Preserve meaning, not wording.
            - Summary should be really short

            Output format:
            User intent: ...
            Key information: ...
            Decisions / outcomes: ...
            Open points: ...
            Keep it concise and information-dense.
            Here is the conversation history:
            {chat_history}
            """
    messages = [{"role": "user", "content": prompt}]
    completion = openai_client.chat.completions.create(
        model=config.llm_model, messages=messages, max_tokens=config.max_tokens
    )
    return completion.choices[0].message.content.strip()
