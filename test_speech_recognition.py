#!/usr/bin/env python3
"""
Test speech recognition on different microphones to find the best one.
"""

import speech_recognition as sr
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SpeechTest")


def test_speech_recognition():
    """Test speech recognition with available microphones."""
    try:
        # Initialize recognizer
        r = sr.Recognizer()
        r.energy_threshold = 50  # Lower threshold
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.3
        r.phrase_threshold = 0.1

        # List available microphones
        mic_names = sr.Microphone.list_microphone_names()
        logger.info(f"Found {len(mic_names)} microphones")

        for i, name in enumerate(mic_names):
            logger.info(f"Microphone {i}: {name}")

        # Try different microphones
        for index in [13, 14, 15, 16, 5, 4, 1, 0]:
            if index >= len(mic_names):
                continue

            try:
                logger.info(f"Testing microphone {index}: {mic_names[index]}")
                with sr.Microphone(device_index=index) as source:
                    logger.info("Adjusting for ambient noise...")
                    r.adjust_for_ambient_noise(source, duration=2)
                    logger.info(f"Energy threshold set to {r.energy_threshold}")

                    logger.info("Listening for 10 seconds...")
                    start_time = time.time()

                    try:
                        while time.time() - start_time < 10:
                            logger.info("Say something!")
                            try:
                                audio = r.listen(source, timeout=3, phrase_time_limit=5)
                                try:
                                    text = r.recognize_google(audio)
                                    logger.info(f"Recognized: {text}")
                                except sr.UnknownValueError:
                                    logger.info("Could not understand audio")
                                except sr.RequestError as e:
                                    logger.error(f"Google Speech API error: {e}")
                            except sr.WaitTimeoutError:
                                logger.warning("Listening timed out")
                    except Exception as e:
                        logger.error(f"Error during listening loop: {e}")

                    logger.info(f"Finished testing microphone {index}")

            except Exception as e:
                logger.error(f"Error with microphone {index}: {e}")

    except Exception as e:
        logger.error(f"Error in speech recognition test: {e}")


if __name__ == "__main__":
    test_speech_recognition()