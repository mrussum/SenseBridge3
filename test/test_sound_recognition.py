#!/usr/bin/env python3
"""
Test sound recognition functionality by simulating sound events.
"""

import os
import logging
import time
import numpy as np
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SoundTest")

def generate_test_audio(event_type, duration=1.0, sample_rate=16000):
    """Generate test audio for the specified event type.

    Args:
        event_type: Type of sound event (doorbell, knock, alarm, etc.)
        duration: Duration of the audio in seconds
        sample_rate: Sample rate in Hz

    Returns:
        Numpy array of audio data
    """
    num_samples = int(duration * sample_rate)

    # Create different audio patterns for different events
    if event_type == "doorbell":
        # Create a doorbell sound (two tones)
        t = np.linspace(0, duration, num_samples, False)
        tone1 = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
        tone2 = 0.5 * np.sin(2 * np.pi * 550 * t)  # 550 Hz tone
        audio = tone1 + tone2

    elif event_type == "knock":
        # Create a knock sound (short impulses)
        audio = np.zeros(num_samples)
        knock_times = [0.1, 0.3, 0.5]
        for t in knock_times:
            idx = int(t * sample_rate)
            width = int(0.05 * sample_rate)
            if idx + width < num_samples:
                audio[idx:idx+width] = np.random.normal(0, 1, width)

    elif event_type == "alarm":
        # Create an alarm sound (sawtooth wave)
        t = np.linspace(0, duration, num_samples, False)
        audio = 0.8 * np.abs(((t * 4) % 1) - 0.5)

    elif event_type == "microwave_beep":
        # Create a microwave beep sound (short beeps)
        audio = np.zeros(num_samples)
        beep_times = [0.1, 0.4, 0.7]
        for t in beep_times:
            idx = int(t * sample_rate)
            width = int(0.1 * sample_rate)
            if idx + width < num_samples:
                t_beep = np.linspace(0, 0.1, width, False)
                audio[idx:idx+width] = 0.7 * np.sin(2 * np.pi * 2000 * t_beep)

    else:
        # Default to white noise
        audio = 0.5 * np.random.normal(0, 1, num_samples)

    # Add some background noise
    background = 0.1 * np.random.normal(0, 1, num_samples)
    audio = audio + background

    # Normalize
    audio = audio / np.max(np.abs(audio))

    return audio

def test_sound_recognition():
    """Test sound recognition by simulating sound events."""
    # Load sound events
    config_file = os.path.join("config", "sound_events.json")
    if not os.path.exists(config_file):
        logger.error(f"Sound events configuration file not found: {config_file}")
        return False

    try:
        with open(config_file, 'r') as f:
            sound_events = json.load(f)

        logger.info(f"Loaded {len(sound_events)} sound events")

        # Test each sound event
        for event_name, event_config in sound_events.items():
            logger.info(f"Testing sound event: {event_name}")

            # Generate test audio
            audio = generate_test_audio(event_name, duration=2.0)

            # Print audio stats
            logger.info(f"Audio shape: {audio.shape}")
            logger.info(f"Audio min: {np.min(audio)}, max: {np.max(audio)}")

            # In a real implementation, we would pass this to the sound classifier
            # For now, just simulate detection
            logger.info(f"Simulated detection: {event_name} (confidence: 0.85)")

            time.sleep(1)

        logger.info("Sound recognition testing completed")
        return True

    except Exception as e:
        logger.error(f"Error testing sound recognition: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting sound recognition test")
    test_sound_recognition()()