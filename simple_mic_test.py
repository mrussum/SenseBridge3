#!/usr/bin/env python3
"""
Simple microphone test focusing only on the default microphone.
"""

import speech_recognition as sr
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SimpleMicTest")


def test_default_microphone():
    """Test only the default microphone."""
    try:
        # Initialize recognizer
        r = sr.Recognizer()
        r.energy_threshold = 50  # Lower threshold
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.3

        logger.info("Testing default microphone")
        try:
            # Use the default microphone
            with sr.Microphone() as source:
                logger.info("Successfully opened default microphone")
                logger.info("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=2)
                logger.info(f"Energy threshold set to {r.energy_threshold}")

                logger.info("Say something!")
                try:
                    # Listen for 5 seconds
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    logger.info("Got audio, recognizing...")

                    try:
                        text = r.recognize_google(audio)
                        logger.info(f"Recognized: {text}")
                    except sr.UnknownValueError:
                        logger.info("Could not understand audio")
                    except sr.RequestError as e:
                        logger.error(f"Google Speech API error: {e}")

                except sr.WaitTimeoutError:
                    logger.warning("Listening timed out")

            logger.info("Microphone test completed")

        except Exception as e:
            logger.error(f"Error testing default microphone: {e}")

    except Exception as e:
        logger.error(f"Error in microphone test: {e}")


if __name__ == "__main__":
    test_default_microphone()