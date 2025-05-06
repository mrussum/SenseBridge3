import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AudioFixer")


def fix_audio_config():
    """Update audio configuration to work better with available hardware."""
    device_config_file = os.path.join("config", "device_config.json")
    user_prefs_file = os.path.join("config", "user_prefs.json")

    # Update device configuration
    try:
        with open(device_config_file, 'r') as f:
            device_config = json.load(f)

        if "audio" not in device_config:
            device_config["audio"] = {}

        # Set more robust audio settings
        device_config["audio"]["sample_rate"] = 16000
        device_config["audio"]["channels"] = 1
        device_config["audio"]["chunk_size"] = 1024
        device_config["audio"]["format"] = "int16"
        device_config["audio"]["retry_on_error"] = True
        device_config["audio"]["device_index"] = -1  # Auto-detect

        with open(device_config_file, 'w') as f:
            json.dump(device_config, f, indent=2)

        logger.info(f"Updated audio configuration in {device_config_file}")
    except Exception as e:
        logger.error(f"Error updating device configuration: {e}")

    # Update user preferences
    try:
        with open(user_prefs_file, 'r') as f:
            user_prefs = json.load(f)

        if "speech_to_text" not in user_prefs:
            user_prefs["speech_to_text"] = {}

        # Enable speech recognition but with more robust settings
        user_prefs["speech_to_text"]["enabled"] = True
        user_prefs["speech_to_text"]["energy_threshold"] = 300
        user_prefs["speech_to_text"]["dynamic_energy_threshold"] = True
        user_prefs["speech_to_text"]["pause_threshold"] = 0.5
        user_prefs["speech_to_text"]["phrase_threshold"] = 0.3

        with open(user_prefs_file, 'w') as f:
            json.dump(user_prefs, f, indent=2)

        logger.info(f"Updated speech recognition settings in {user_prefs_file}")
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")


if __name__ == "__main__":
    fix_audio_config()