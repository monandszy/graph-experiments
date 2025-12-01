from ai_enchancer import *
from e_amr_parser import *
from amr_turtle_parser import *
from graphdb_inserter import *
from config import configure_logging, G_PROMPT, G_INPUT_SENTENCE
import logging

logger = logging.getLogger(__name__)

def main():
  configure_logging()
  logger.info("Running...")
  amr = parse_english(G_INPUT_SENTENCE)
  for graph in amr:  
    logger.info("AMR graph:\n%s", graph)
    turtle_data = amr_to_rdf(graph)
    logger.info("Turtle data:\n%s", turtle_data)
    upload_turtle_to_graphdb(turtle_data)
    ai_input = G_PROMPT + graph
    enchanced = generate(ai_input)
    logger.info("AI enhancement result: %s", getattr(enchanced, "text", str(enchanced)))

if __name__ == "__main__":
    main()