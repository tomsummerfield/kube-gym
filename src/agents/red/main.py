import requests
import logging
import sys

def test_connection():
    # Configure logging to output to stdout without buffering
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)
    logger.info("Testing connection to API Service for Red Agent")
    try:
        response = requests.get("http://api-service:8000/")
        logger.info(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error testing connection to API Service: {e}")

if __name__ == "__main__":
    test_connection()