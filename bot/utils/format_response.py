def format_response(response: str) -> str:
    parts = response.split("*")
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            result.append(part)
        else:
            result.append(f"<b>{part}</b>")
    return "".join(result)
