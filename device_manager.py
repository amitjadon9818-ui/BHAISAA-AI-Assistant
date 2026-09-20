import json


DEVICES_FILE = "devices.json"


def load_devices():
    """Load all registered devices."""

    with open(DEVICES_FILE, "r") as file:
        data = json.load(file)

    return data["devices"]


def search_device(search_term):
    """Return devices matching a search term in name, type, or id."""

    query = (search_term or "").strip().lower()
    devices = load_devices()

    if not query:
        return devices

    matching_devices = []
    for device in devices:
        name = str(device.get("name", "")).lower()
        device_type = str(device.get("type", "")).lower()
        device_id = str(device.get("id", "")).lower()

        if query in name or query in device_type or query in device_id:
            matching_devices.append(device)

    return matching_devices


def search_devices(search_term):
    """Alias for searching devices by text."""

    return search_device(search_term)


def get_device_count():
    """Return the number of registered devices."""

    devices = load_devices()

    return len(devices)


def list_devices():
    """Return the registered devices."""

    return load_devices()


def add_device(name, device_type):
    """Add a new device to the registry."""

    devices = load_devices()

    import uuid

    device_id = str(uuid.uuid4())

    new_device = {
        "id": device_id,
        "name": name,
        "type": device_type,
        "trusted": False
    }

    devices.append(new_device)

    data = {
        "devices": devices
    }

    with open(DEVICES_FILE, "w") as file:
        json.dump(data, file, indent=4)

    return new_device

import secrets


def trust_device(device_id):
    """Mark a device as trusted after successful pairing."""
    devices = load_devices()

    for device in devices:
        if device["id"] == device_id:
            device["trusted"] = True

            data = {
                "devices": devices
            }

            with open(DEVICES_FILE, "w") as file:
                json.dump(data, file, indent=4)

            return True

    return False


def generate_pairing_code():
    """Generate a temporary 6-digit pairing code."""
    return str(secrets.randbelow(900000) + 100000)