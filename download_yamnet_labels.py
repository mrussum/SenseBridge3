import os
import urllib.request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LabelsDownloader")


def download_yamnet_labels():
    """Download the YAMNet labels file if it doesn't exist."""
    model_dir = os.path.join("models", "yamnet_model")
    labels_file = os.path.join(model_dir, "yamnet_labels.txt")

    # Create directory if it doesn't exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)
        logger.info(f"Created directory: {model_dir}")

    # Check if labels file already exists
    if os.path.exists(labels_file):
        logger.info(f"YAMNet labels file already exists at {labels_file}")
        return True

    # URLs to try for the labels file
    urls = [
        "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv",
        "https://storage.googleapis.com/audioset/yamnet_class_map.csv"
    ]

    for url in urls:
        try:
            logger.info(f"Trying to download labels from: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req) as response:
                csv_content = response.read().decode('utf-8')

                # Convert CSV to simple text format expected by YAMNet
                lines = csv_content.strip().split('\n')[1:]  # Skip header line
                labels = [line.split(',')[2].strip('"') for line in lines]

                with open(labels_file, 'w') as f:
                    f.write('\n'.join(labels))

                logger.info(f"YAMNet labels file created at {labels_file}")
                return True

        except Exception as e:
            logger.warning(f"Failed to download from {url}: {str(e)}")

    logger.error("Failed to download YAMNet labels from all sources.")

    # Create a simple fallback labels file with common sounds
    logger.info("Creating fallback labels file...")
    fallback_labels = [
        "Speech",
        "Doorbell",
        "Knock",
        "Microwave beep",
        "Alarm",
        "Water running",
        "Cat meowing",
        "Dog barking",
        "Phone ringing",
        "Music"
    ]

    with open(labels_file, 'w') as f:
        f.write('\n'.join(fallback_labels))

    logger.info("Created fallback labels file")
    return True


if __name__ == "__main__":
    download_yamnet_labels()