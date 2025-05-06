#!/usr/bin/env python3
"""
Update the SenseBridge configuration files for simulation mode.
This script updates the configuration to prevent warnings and improve simulation.
"""

import os
import json
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("ConfigUpdater")


def update_device_config():
    """Update the device configuration to prevent warnings."""
    config_file = os.path.join("config", "device_config.json")

    if not os.path.exists(config_file):
        logger.error(f"Configuration file {config_file} not found")
        return False

    try:
        # Read the current config
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Update bluetooth configuration for simulation
        if "bluetooth" not in config:
            config["bluetooth"] = {}

        config["bluetooth"]["simulation_mode"] = True
        config["bluetooth"]["wearable_mac"] = "00:11:22:33:44:55"  # Dummy MAC for simulation
        config["bluetooth"]["device_name"] = "SenseBridge_Simulator"

        # Update audio configuration for simulation
        if "audio" not in config:
            config["audio"] = {}

        config["audio"]["simulation_mode"] = True
        config["audio"]["use_fallback_classification"] = True
        config["audio"]["sample_rate"] = 16000
        config["audio"]["channels"] = 1

        # Update hardware configuration for simulation
        if "hardware" not in config:
            config["hardware"] = {}

        config["hardware"]["simulation_mode"] = True
        config["hardware"]["haptic_pin"] = 18  # Dummy GPIO pin
        config["hardware"]["led_pin"] = 23  # Dummy GPIO pin

        # Write updated config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        logger.info(f"Updated device configuration in {config_file}")
        return True

    except Exception as e:
        logger.error(f"Error updating device configuration: {str(e)}")
        return False


def update_user_prefs():
    """Update user preferences to prevent warnings."""
    config_file = os.path.join("config", "user_prefs.json")

    if not os.path.exists(config_file):
        logger.error(f"Configuration file {config_file} not found")
        return False

    try:
        # Read the current config
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Update speech recognition settings
        if "speech_to_text" not in config:
            config["speech_to_text"] = {}

        config["speech_to_text"]["enabled"] = False  # Disable in simulation to prevent errors
        config["speech_to_text"]["simulation_mode"] = True
        config["speech_to_text"]["language"] = "en-US"
        config["speech_to_text"]["timeout"] = 5
        config["speech_to_text"]["phrase_time_limit"] = 5
        config["speech_to_text"]["energy_threshold"] = 300
        config["speech_to_text"]["adjust_for_ambient_noise"] = True
        config["speech_to_text"]["pause_threshold"] = 0.8

        # Update notifications settings
        if "notifications" not in config:
            config["notifications"] = {}

        config["notifications"]["simulation_mode"] = True
        config["notifications"]["haptic_enabled"] = True
        config["notifications"]["visual_enabled"] = True
        config["notifications"]["smart_home_enabled"] = False  # Disable smart home integration in simulation

        # Update sound detection settings
        if "sound_detection" not in config:
            config["sound_detection"] = {}

        config["sound_detection"]["simulation_mode"] = True
        config["sound_detection"]["enabled"] = True
        config["sound_detection"]["sensitivity"] = 0.7
        config["sound_detection"]["use_fallback"] = True
        config["sound_detection"]["min_confidence"] = 0.6

        # Add smart home section if missing
        if "smart_home" not in config:
            config["smart_home"] = {}
            config["smart_home"]["enabled"] = False
            config["smart_home"]["mqtt_broker"] = "localhost"
            config["smart_home"]["mqtt_port"] = 1883
            config["smart_home"]["mqtt_topic"] = "sensebridge/events"

        # Write updated config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        logger.info(f"Updated user preferences in {config_file}")
        return True

    except Exception as e:
        logger.error(f"Error updating user preferences: {str(e)}")
        return False


def update_sound_events():
    """Update sound events configuration for better simulation."""
    config_file = os.path.join("config", "sound_events.json")

    if not os.path.exists(config_file):
        logger.error(f"Configuration file {config_file} not found")
        return False

    try:
        # Read the current config
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Ensure all required sound events are defined
        required_events = ["doorbell", "knock", "microwave_beep", "alarm"]

        for event in required_events:
            if event not in config:
                config[event] = {
                    "name": event.replace("_", " ").title(),
                    "priority": "high" if event in ["doorbell", "knock", "alarm"] else "medium",
                    "haptic_pattern": "short_double" if event in ["doorbell", "knock"] else "long_single",
                    "visual_pattern": "flash" if event in ["doorbell", "alarm"] else "pulse",
                    "notification_text": f"Detected: {event.replace('_', ' ').title()}",
                    "action": "alert"
                }

        # Write updated config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        logger.info(f"Updated sound events configuration in {config_file}")
        return True

    except Exception as e:
        logger.error(f"Error updating sound events configuration: {str(e)}")
        return False


def ensure_config_directory():
    """Ensure the config directory exists with proper __init__.py."""
    config_dir = "config"

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        logger.info(f"Created config directory: {config_dir}")

    init_file = os.path.join(config_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('"""Configuration module for SenseBridge."""\n')
        logger.info(f"Created {init_file}")

    return True


def update_simulation_config():
    """Main function to update all configurations for simulation."""
    success = True

    logger.info("Updating configuration files for simulation mode")

    if not ensure_config_directory():
        success = False

    if not update_device_config():
        success = False

    if not update_user_prefs():
        success = False

    if not update_sound_events():
        success = False

    return success


if __name__ == "__main__":
    logger.info("Starting configuration update for simulation mode")
    if update_simulation_config():
        logger.info("Configuration updated successfully for simulation mode")
        sys.exit(0)
    else:
        logger.error("Failed to update configuration for simulation mode")
        sys.exit(1)