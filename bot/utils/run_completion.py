from openai import OpenAI


def run_completion(base_url: str, api_key: str, llm_model: str, messages: list) -> str:
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        completion_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        completion = client.chat.completions.create(
            model=llm_model, messages=completion_messages
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"Completion failed: {e}")
