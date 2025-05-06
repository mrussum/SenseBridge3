import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SpeechFixer")


def fix_speech_config():
    """Update speech recognition configuration to be more sensitive."""
    user_prefs_file = os.path.join("config", "user_prefs.json")

    try:
        with open(user_prefs_file, 'r') as f:
            user_prefs = json.load(f)

        if "speech_to_text" not in user_prefs:
            user_prefs["speech_to_text"] = {}

        # Make speech recognition much more sensitive
        user_prefs["speech_to_text"]["enabled"] = True
        user_prefs["speech_to_text"]["energy_threshold"] = 50  # Lower threshold
        user_prefs["speech_to_text"]["dynamic_energy_threshold"] = True
        user_prefs["speech_to_text"]["pause_threshold"] = 0.3  # Shorter pause
        user_prefs["speech_to_text"]["phrase_threshold"] = 0.1  # Lower phrase threshold
        user_prefs["speech_to_text"]["non_speaking_duration"] = 0.3  # Shorter non-speaking
        user_prefs["speech_to_text"]["timeout"] = 10  # Longer timeout
        user_prefs["speech_to_text"]["phrase_time_limit"] = 10  # Longer phrase time

        with open(user_prefs_file, 'w') as f:
            json.dump(user_prefs, f, indent=2)

        logger.info(f"Updated speech recognition settings in {user_prefs_file}")
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")


if __name__ == "__main__":
    fix_speech_config()