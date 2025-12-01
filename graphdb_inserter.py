import requests
from config import get_graphdb_endpoint
import logging

logger = logging.getLogger(__name__)
GRAPHDB_ENDPOINT = get_graphdb_endpoint()

def upload_turtle_to_graphdb(turtle_data):
  headers = {
      "Content-Type": "text/turtle"
  }
  logger.info("Connecting to GraphDB endpoint: %s", GRAPHDB_ENDPOINT)
      
  try:
    response = requests.post(GRAPHDB_ENDPOINT, data=turtle_data.encode('utf-8'), headers=headers)
    response.raise_for_status()
    logger.info("Successfully uploaded data to GraphDB!")

  except requests.exceptions.RequestException as e:
    logger.error("An error occurred while uploading to GraphDB: %s", e)
    if e.response is not None:
      logger.error("Server responded with: %s", e.response.text)

  except Exception as e:
    logger.exception("Unexpected error when uploading to GraphDB: %s", e)
