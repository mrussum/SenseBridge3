"""
Speech to text module for SenseBridge.
Converts audio to text using speech recognition.
"""

import logging
import threading
import queue
import time
import sys
import os

logger = logging.getLogger(__name__)

try:
    import speech_recognition as sr

    SR_AVAILABLE = True
except ImportError:
    logger.warning("Speech recognition library not available")
    SR_AVAILABLE = False
    sr = None

from ..utils.config import Config


class SpeechToText:
    """Speech-to-text recognition module."""

    def __init__(self, text_callback=None):
        """Initialize the speech-to-text system.

        Args:
            text_callback: Callback function for recognized text
        """
        self.config = Config()
        self.user_prefs = self.config.get_user_preferences()
        self.speech_config = self.user_prefs.get("speech_to_text", {})

        # Speech recognition settings
        self.enabled = self.speech_config.get("enabled", True)
        self.language = self.speech_config.get("language", "en-US")
        self.timeout = self.speech_config.get("timeout", 5)
        self.phrase_time_limit = self.speech_config.get("phrase_time_limit", 5)
        self.energy_threshold = self.speech_config.get("energy_threshold", 300)
        self.adjust_for_ambient_noise = self.speech_config.get("adjust_for_ambient_noise", True)
        self.pause_threshold = self.speech_config.get("pause_threshold", 0.8)

        # Add detection for simulation mode
        self.in_simulation = "--simulation" in sys.argv or hasattr(sys, 'simulation_mode')

        # Recognizer
        if SR_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = self.energy_threshold
            self.recognizer.pause_threshold = self.pause_threshold
            self.available_mics = self._get_available_microphones()
            logger.info(f"Available microphones: {self.available_mics}")
            self.sr_available = True
        else:
            logger.warning("Speech recognition library not available")
            self.sr_available = False
            self.available_mics = []

        # Microphone
        self.microphone = None
        self.mic_source = None

        # Thread for continuous recognition
        self.listen_thread = None
        self.running = False

        # Queue for recognized text
        self.text_queue = queue.Queue()

        # Callback function for recognized text
        self.callback = text_callback

        logger.info("SpeechToText initialized")
    def start(self):
        """Start listening for speech."""
        if self.running:
            logger.warning("Speech recognition already running")
            return

        self.running = True

        # Skip actual audio processing in simulation mode
        if self.in_simulation:
            logger.info("Running in simulation mode - using mocked speech recognition")
            # Just start a dummy thread that periodically generates fake speech commands for testing
            self.listen_thread = threading.Thread(target=self._simulation_loop)
            self.listen_thread.daemon = True
            self.listen_thread.start()
            logger.info("Speech to text started (simulation mode)")
            return

        # Only try to use microphone if speech recognition is available
        if not self.sr_available:
            logger.warning("Speech recognition not available")
            return

        if not self.enabled:
            logger.info("Speech recognition is disabled in user preferences")
            return

        try:
            # Adjust for ambient noise
            if self.adjust_for_ambient_noise:
                logger.info("Adjusting for ambient noise...")
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                logger.info(f"Energy threshold set to {self.recognizer.energy_threshold}")

            # Start listening thread
            logger.info("Starting continuous speech recognition")
            self.listen_thread = threading.Thread(target=self._listen_loop)
            self.listen_thread.daemon = True
            self.listen_thread.start()

            logger.info("Speech to text started")
        except Exception as e:
            logger.error(f"Error starting speech recognition: {str(e)}")
            self.running = False

    def stop(self):
        """Stop listening for speech."""
        if not self.running:
            return

        self.running = False

        if self.listen_thread:
            self.listen_thread.join(timeout=2.0)

        if self.mic_source:
            try:
                self.mic_source.close()
            except:
                pass
            self.mic_source = None

        logger.info("Speech to text stopped")

    def set_callback(self, callback):
        """Set a callback function for recognized text.

        Args:
            callback: Function to call with recognized text
        """
        self.callback = callback

    def get_text(self, timeout=1.0):
        """Get recognized text from the queue.

        Args:
            timeout: Maximum time to wait for text (seconds)

        Returns:
            Recognized text, or None if no text available
        """
        try:
            return self.text_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def _get_available_microphones(self):
        """Get a list of available microphones.

        Returns:
            List of microphone names
        """
        if not SR_AVAILABLE:
            return []

        try:
            mic_list = sr.Microphone.list_microphone_names()
            return mic_list
        except Exception as e:
            logger.error(f"Error getting microphone list: {str(e)}")
            return []

    def _listen_loop(self):
        """Main loop for continuous speech recognition."""
        if not SR_AVAILABLE:
            logger.error("Speech recognition library not available")
            return

        # Try different microphone indices
        # Try microphone indices that correspond to actual microphones, not audio outputs
        mic_indices_to_try = [13, 14, 15, 16, 5, 4, 1, 0]

        for mic_index in mic_indices_to_try:
            try:
                logger.info(f"Trying microphone with index {mic_index}")
                with sr.Microphone(device_index=mic_index) as source:
                    self.mic_source = source

                    # Test a simple listen with longer adjustment
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                    logger.info(f"Successfully connected to microphone {mic_index}")

                    # Now enter the main recognition loop with this working microphone
                    while self.running:
                        try:
                            audio = self.recognizer.listen(source, timeout=self.timeout,
                                                           phrase_time_limit=self.phrase_time_limit)

                            # Try to recognize the speech
                            try:
                                text = self.recognizer.recognize_google(audio, language=self.language)
                                logger.info(f"Recognized: {text}")

                                # Add to queue
                                self.text_queue.put(text)

                                # Call callback if set
                                if self.callback:
                                    self.callback(text)

                            except sr.UnknownValueError:
                                # Speech was unintelligible
                                pass
                            except sr.RequestError as e:
                                logger.warning(f"Speech recognition service error: {e}")
                                time.sleep(1)  # Wait a bit before retrying

                        except Exception as e:
                            logger.error(f"Error in speech recognition: {str(e)}")
                            time.sleep(0.5)

                    # If we reach here, the loop was exited
                    return

            except Exception as e:
                logger.warning(f"Could not use microphone with index {mic_index}: {str(e)}")

        # If we reach here, none of the microphones worked
        logger.error("Could not connect to any microphone")
    def _simulation_loop(self):
        """Simulation loop that generates fake speech events for testing."""
        test_phrases = [
            "Help me",
            "What was that noise",
            "Turn on the lights",
            "Call for help"
        ]

        recognitions = 0
        max_recognitions = 5  # Limit the number of simulated phrases

        while self.running and recognitions < max_recognitions:
            try:
                # Sleep for a while to simulate waiting for speech
                time.sleep(60)  # One simulated phrase per minute

                # Generate a simulated speech event
                if self.running:
                    phrase = test_phrases[recognitions % len(test_phrases)]
                    logger.info(f"Simulation: Recognized speech: '{phrase}'")

                    # Add to queue
                    self.text_queue.put(phrase)

                    # Call the callback as if real speech was detected
                    if self.callback:
                        self.callback(phrase)

                    recognitions += 1

            except Exception as e:
                logger.error(f"Error in simulation loop: {str(e)}")
                time.sleep(5)

        # After generating the test phrases, just sleep to keep the thread alive
        while self.running:
            time.sleep(10)


def listen_for_command():
    """Listen for a single voice command.

    Returns:
        Recognized text, or None if recognition failed
    """
    if not SR_AVAILABLE:
        logger.error("Speech recognition library not available")
        return None

    try:
        # Create recognizer
        r = sr.Recognizer()

        # Adjust for ambient noise and listen
        with sr.Microphone() as source:
            logger.info("Listening for command...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        # Recognize speech
        try:
            text = r.recognize_google(audio, language="en-US")
            logger.info(f"Recognized command: {text}")
            return text
        except sr.UnknownValueError:
            logger.info("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Recognition error: {e}")
            return None

    except Exception as e:
        logger.error(f"Error listening for command: {str(e)}")
        return None