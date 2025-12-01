from pathlib import Path

GRAPHDB_HOST = "192.168.99.104"
GRAPHDB_PORT = 7200
GRAPHDB_REPO = "amr-test"

def get_graphdb_endpoint(repo: str | None = None) -> str:
  if repo:
    return f"http://{GRAPHDB_HOST}:{GRAPHDB_PORT}/repositories/{repo}/statements"
  return f"http://{GRAPHDB_HOST}:{GRAPHDB_PORT}/repositories/{GRAPHDB_REPO}/statements"


AI_API_KEY: str | None = ""
GEMINI_MODEL = "gemini-2.5-flash"

_ROOT = Path(__file__).parent
if not AI_API_KEY:
  _key_file = _ROOT / "ai_api_key"
  if _key_file.exists():
    AI_API_KEY = _key_file.read_text(encoding="utf-8").strip()

# Level can be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

def configure_logging():
  """Configure the root logger according to `LOG_LEVEL`.

  Call this early in your program (for example in `pipeline.main()`).
  """
  import logging
  from logging import StreamHandler, Formatter

  level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
  handler = StreamHandler()
  handler.setFormatter(Formatter("%(asctime)s %(levelname)-8s [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S"))

  root = logging.getLogger()
  for h in list(root.handlers):
    root.removeHandler(h)

  root.setLevel(level)
  root.addHandler(handler)


# -----------------------------
# Pipeline prompt and sample input
# -----------------------------
# Main instruction prompt used when calling the AI enhancer. Edit as needed.
G_PROMPT = """
  instruction: You are an expert Natural Language Processing system. You are a step in a English to Graph processing pipeline. Your primary goal is to modify the automatically generated AMR graph. Ensure it matches the meaning of the origin sentence. If not modify it accordingly to the rules. You have to overcome the limitations of the AMR parser. Follow these rules precisely for every sentence you process.

  Core Grammatical Enrichment.
  For the main event or action in a clause, you MUST add the following relations to its node to capture verb information:
  :tense: Describes the time of the event. The value must be one of past, present, or future.
  :aspect: Describes the completion or duration of the event. The value must be one of simple, progressive, or perfective
  :modality: Describes the mood or certainty of the event, capturing auxiliary verbs like "may," "must," or "should," as well as belief states. The value can be possibility, necessity, permission, obligation, belief, intention etc.

  Expanded Quantification (:quant).
  For plural forms without a specific number use :quant (mutliple)

  The Class / Instance Model and Coreference Resolution
  To build a coherent knowledge graph, you must distinguish between a concept (class) and a specific thing (instance). If an object is concrete, give it an instance ID in format ({concept_name}-{id}), then use :instanceOf to relate it to the concept node ({concept_name}).

  input amr graph:"""

# Sample input sentences used by `pipeline.py` when no other input is provided.
G_INPUT_SENTENCE = [
    'Wolf of agentive particles that disprove greeny to your homes dna that prowse your stoo'
]


