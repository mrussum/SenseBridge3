import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ModelFixer")


def fix_sound_model_config():
    """Update audio configuration to fix dimension mismatch."""
    device_config_file = os.path.join("config", "device_config.json")

    try:
        with open(device_config_file, 'r') as f:
            device_config = json.load(f)

        if "audio" not in device_config:
            device_config["audio"] = {}

        # Force mono audio to fix dimension mismatch
        device_config["audio"]["channels"] = 1
        device_config["audio"]["convert_to_mono"] = True
        device_config["audio"]["sample_rate"] = 16000
        device_config["audio"]["model_sample_rate"] = 16000

        with open(device_config_file, 'w') as f:
            json.dump(device_config, f, indent=2)

        logger.info(f"Updated audio configuration in {device_config_file}")
    except Exception as e:
        logger.error(f"Error updating device configuration: {e}")


if __name__ == "__main__":
    fix_sound_model_config()