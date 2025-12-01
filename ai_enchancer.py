import time
from google import genai
from google.genai import types
from functools import wraps
from google.genai.errors import ServerError
from config import AI_API_KEY, GEMINI_MODEL
import logging

logger = logging.getLogger(__name__)

def retry_on_server_error(tries, delay):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      last_exception = None
      for attempt in range(tries):
        try:
          return func(*args, **kwargs)
        except ServerError as e:
          last_exception = e
          logger.warning("Attempt %d failed with ServerError: %s. Retrying in %d seconds...", attempt + 1, e, delay)
          time.sleep(delay)
      raise last_exception
    return wrapper
  return decorator

@retry_on_server_error(tries=5, delay=3)
def generate(instruction: str):
  if not AI_API_KEY:
    raise RuntimeError("AI API key not found. Set `AI_API_KEY` in `config.py` or create an `ai_api_key` file in the repo root.")

  client = genai.Client(api_key=AI_API_KEY)
  model = GEMINI_MODEL

  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text=instruction),
      ],
    ),
  ]

  tools = [
    types.Tool(googleSearch=types.GoogleSearch()),
  ]

  generate_content_config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_budget=-1),
    tools=tools,
  )

  chunk = client.models.generate_content(
    model=model,
    contents=contents,
    config=generate_content_config,
  )

  return chunk
