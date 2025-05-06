#!/usr/bin/env python3
"""
Fix the audio_processor.py to convert stereo to mono before sending to the model.
"""

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AudioFixer")


def fix_audio_processor():
    """Fix the audio_processor.py to convert stereo to mono."""
    audio_file = os.path.join("src", "audio", "audio_processor.py")

    if not os.path.exists(audio_file):
        logger.error(f"Audio processor file not found: {audio_file}")
        return False

    try:
        # Read the file content
        with open(audio_file, 'r') as f:
            content = f.read()

        # Check if the conversion code is already there
        if "convert_to_mono" not in content:
            # Get indentation level
            lines = content.split("\n")
            import_line = None
            for line in lines:
                if "import numpy" in line:
                    import_line = line
                    break

            # If numpy is not imported, add it
            if not import_line:
                for i, line in enumerate(lines):
                    if "import" in line:
                        lines.insert(i + 1, "import numpy as np")
                        break

            # Add conversion function
            for i, line in enumerate(lines):
                if "class AudioProcessor" in line:
                    for j in range(i + 1, len(lines)):
                        if "def" in lines[j] and "process_audio" in lines[j]:
                            # Get the indentation
                            indentation = lines[j].split("def")[0]

                            # Add conversion code after the function definition
                            process_line = j + 1
                            while process_line < len(lines) and not lines[process_line].strip():
                                process_line += 1

                            # Add the conversion code
                            conversion_code = [
                                f"{indentation}    # Convert stereo to mono if needed",
                                f"{indentation}    if len(audio_data.shape) > 1 and audio_data.shape[1] > 1:",
                                f"{indentation}        audio_data = np.mean(audio_data, axis=1)"
                            ]

                            for k, code_line in enumerate(conversion_code):
                                lines.insert(process_line + k, code_line)

                            break
                    break

            # Write the modified content back
            with open(audio_file, 'w') as f:
                f.write("\n".join(lines))

            logger.info(f"Added stereo to mono conversion to {audio_file}")
            return True
        else:
            logger.info("Stereo to mono conversion already added")
            return True

    except Exception as e:
        logger.error(f"Error fixing audio processor: {e}")
        return False


if __name__ == "__main__":
    fix_audio_processor()