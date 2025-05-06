# download_yamnet.py
import os
import urllib.request
import logging
import sys
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("ModelDownloader")


def download_yamnet_model():
    """Download the YAMNet model file if it doesn't exist."""
    model_dir = os.path.join("models", "yamnet_model")
    model_file = os.path.join(model_dir, "yamnet.tflite")

    # Create directory if it doesn't exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)
        logger.info(f"Created directory: {model_dir}")

    # Create __init__.py if it doesn't exist
    init_file = os.path.join(model_dir, "__init__.py")
    if not os.path.exists(init_file):
        open(init_file, 'a').close()
        logger.info(f"Created file: {init_file}")

    # Check if model already exists
    if os.path.exists(model_file):
        logger.info(f"YAMNet model already exists at {model_file}")
        return True

    # Download the model
    logger.info("Downloading YAMNet model file...")
    try:
        # Use a proper User-Agent to avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # URLs to try - sometimes the original URL might be blocked
        urls = [
            "https://storage.googleapis.com/download.tensorflow.org/models/tflite/yamnet/yamnet.tflite",
            "https://github.com/tensorflow/models/raw/master/research/audioset/yamnet/yamnet.tflite",
            "https://tfhub.dev/google/lite-model/yamnet/classification/tflite/1?lite-format=tflite"
        ]

        success = False
        for url in urls:
            try:
                logger.info(f"Trying to download from: {url}")
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as response, open(model_file, 'wb') as out_file:
                    data = response.read()
                    out_file.write(data)
                success = True
                logger.info(f"YAMNet model downloaded successfully to {model_file}")
                break
            except Exception as e:
                logger.warning(f"Failed to download from {url}: {str(e)}")
                time.sleep(1)  # Wait a bit before trying the next URL

        if not success:
            logger.error("Failed to download YAMNet model from all sources.")
            return False

        return True
    except Exception as e:
        logger.error(f"Error downloading YAMNet model: {str(e)}")
        return False


if __name__ == "__main__":
    logger.info("Starting YAMNet model download script")
    success = download_yamnet_model()
    if success:
        logger.info("YAMNet model setup completed successfully")
        sys.exit(0)
    else:
        logger.error("YAMNet model setup failed")
        sys.exit(1)