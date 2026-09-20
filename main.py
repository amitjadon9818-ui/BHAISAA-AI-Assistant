import json
from datetime import datetime

from device_manager import get_device_count, list_devices, add_device, generate_pairing_code, trust_device

# ==========================================
# CONFIGURATION
# ==========================================

def load_config():

    with open("config.json", "r") as file:
        return json.load(file)


config = load_config()


# ==========================================
# BHAISAA IDENTITY
# ==========================================

ASSISTANT_NAME = config["assistant"]["name"]
OWNER_NAME = config["user"]["name"]

DEVICE_NAME = config["device"]["name"]
DEVICE_TYPE = config["device"]["type"]

LANGUAGE = config["assistant"]["language"]


# ==========================================
# RESPONSE SYSTEM
# ==========================================

def speak(message):
    print(f"{ASSISTANT_NAME}: {message}")


# ==========================================
# COMMAND ENGINE
# ==========================================

def process_command(command):

    command = command.lower().strip()

    if command in ["hello", "hi", "hey"]:

        speak(
            f"Ram Ram {OWNER_NAME}! "
            f"How can I help you?"
        )

    elif command == "status":

        speak(
            f"All core systems are online. "
            f"I am running on {DEVICE_NAME}."
        )

    elif command == "time":

        current_time = datetime.now().strftime("%I:%M %p")

        speak(
            f"The current time is {current_time}."
        )

    elif command in ["who are you", "what are you"]:

        speak(
            f"I am {ASSISTANT_NAME}, "
            f"your personal AI assistant."
        )

    elif command in ["device", "what device is this"]:

        speak(
            f"This is your {DEVICE_NAME}. "
            f"Device type: {DEVICE_TYPE}."
        )
        
    elif command in ["devices", "my devices", "show devices"]:
        devices = list_devices()

        if len(devices) == 0:
            speak("There are currently no registered devices.")
        else:
            speak(f"I have {len(devices)} registered device(s).")

            for device in devices:
                if device["trusted"]:
                    status = "Trusted"
                else:
                    status = "Not trusted"

                speak(
                    f"{device['name']} ({device['type']}) — {status}"
                )

    elif command in ["add device", "add a device"]:
        name = input("BHAISAA: What should I call this device? ").strip()
        device_type = input("BHAISAA: What type of device is it? ").strip()

        if not name or not device_type:
            speak("Device name and type cannot be empty.")
            return True

        device = add_device(name, device_type)
        speak(f"I registered {device['name']} as a {device['type']}.")
        speak("The device is not trusted yet. Secure pairing will be required.")

    elif command in ["pair device", "pair a device"]:
        devices = list_devices()
        untrusted_devices = [device for device in devices if not device["trusted"]]

        if len(untrusted_devices) == 0:
            speak("There are no untrusted devices available for pairing.")
        else:
            speak("Available devices for pairing:")

            for index, device in enumerate(untrusted_devices, start=1):
                speak(f"{index}. {device['name']} ({device['type']})")

            choice = input("BHAISAA: Enter the device number: ")

            if choice.isdigit() and 1 <= int(choice) <= len(untrusted_devices):
                selected_device = untrusted_devices[int(choice) - 1]
                pairing_code = generate_pairing_code()

                speak(f"Your pairing code is: {pairing_code}")
                entered_code = input("BHAISAA: Enter the pairing code to confirm: ").strip()

                if entered_code == pairing_code:
                    if trust_device(selected_device["id"]):
                        speak(f"{selected_device['name']} has been successfully paired.")
                        speak(f"{selected_device['name']} is now trusted.")
                    else:
                        speak("I could not update the device trust status.")
                else:
                    speak("Incorrect pairing code. The device remains untrusted.")
            else:
                speak("Invalid device selection.")

    elif command in ["config", "show config"]:

        speak(
            f"My name is {ASSISTANT_NAME}. "
            f"Your name is {OWNER_NAME}. "
            f"My current language is {LANGUAGE}. "
            f"I am running on {DEVICE_NAME} ({DEVICE_TYPE})."
        )

    elif command in ["exit", "quit"]:

        speak(
            f"Goodbye, {OWNER_NAME}."
        )

        return False

    else:

        speak(
            "I don't understand that command yet."
        )

    return True


# ==========================================
# START BHAISAA
# ==========================================

print("=" * 50)

print(f"              {ASSISTANT_NAME}")

print("=" * 50)

speak("System initialized.")

speak(
    f"I am running on {DEVICE_NAME}."
)

speak("Waiting for your command...")

print("=" * 50)


# ==========================================
# MAIN LOOP
# ==========================================

running = True

while running:

    command = input("\nYOU: ")

    running = process_command(command)

