FROM python:3.12-slim

WORKDIR /bot

COPY pyproject.toml .
RUN pip install .

COPY . .

CMD ["python", "-m", "main"]
