import speech_recognition as sr

# Create a recognizer
r = sr.Recognizer()

# List available microphones
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone {index}: {name}")

# Try to use the default microphone
print("\nTesting microphone access...")
try:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        print("Got it! Now recognizing...")
        text = r.recognize_google(audio)
        print(f"You said: {text}")
except Exception as e:
    print(f"Error: {e}")