#!/usr/bin/env python3
"""
Fix the sound classifier to handle stereo audio by converting it to mono.
"""

import os
import logging
import fileinput
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ModelFixer")


def fix_sound_classifier_code():
    """Fix the sound_classifier.py code to handle stereo audio."""
    classifier_file = os.path.join("src", "models", "sound_classifier.py")

    if not os.path.exists(classifier_file):
        logger.error(f"Sound classifier file not found: {classifier_file}")
        return False

    try:
        # Read the file content
        with open(classifier_file, 'r') as f:
            content = f.read()

        # Check if we need to add code to convert stereo to mono
        if "convert_to_mono" not in content:
            # Find the process_audio method
            if "def process_audio" in content:
                # Add code to convert stereo to mono
                modified_content = content.replace(
                    "def process_audio(self, audio_data):",
                    """def process_audio(self, audio_data):
        # Convert stereo to mono if needed
        if len(audio_data.shape) > 1 and audio_data.shape[1] == 2:
            logging.debug("Converting stereo audio to mono")
            audio_data = np.mean(audio_data, axis=1)

        # Ensure audio data is the right shape for the model
        if len(audio_data.shape) != 1:
            logging.warning(f"Unexpected audio shape: {audio_data.shape}, reshaping")
            audio_data = np.reshape(audio_data, -1)"""
                )

                # Write the modified content back
                with open(classifier_file, 'w') as f:
                    f.write(modified_content)

                logger.info(f"Added stereo to mono conversion to {classifier_file}")
                return True
            else:
                logger.warning("Could not find process_audio method in sound classifier")
        else:
            logger.info("Stereo to mono conversion already added")
            return True

    except Exception as e:
        logger.error(f"Error fixing sound classifier: {e}")
        return False


if __name__ == "__main__":
    fix_sound_classifier_code()