class ConnectionManager:
    """Manage how BHAISAA attempts to connect to devices."""

    def get_connection_strategy(self, device):
        """Choose a connection strategy for a device."""

        if not device["trusted"]:
            return "blocked"

        return "network_independent"


def test_connection_strategy(device):
    """Test the connection strategy for a device."""

    manager = ConnectionManager()

    strategy = manager.get_connection_strategy(device)

    if strategy == "blocked":
        print("Connection blocked: device is not trusted.")

    elif strategy == "network_independent":
        print(
            f"Connection allowed for {device['name']}."
        )
        print(
            "Future connection path: "
            "direct P2P → relay fallback."
        )

    return strategy