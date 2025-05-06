# src/mock/bluetooth.py
# Mock Bluetooth module for simulation mode

# Basic Bluetooth socket class
class BluetoothSocket:
    def __init__(self, protocol=None):
        self.protocol = protocol
        self.connected = False
        self.address = None
        self.timeout = None

    def connect(self, address):
        print(f"Mock Bluetooth: Connected to {address}")
        self.connected = True
        self.address = address

    def settimeout(self, timeout):
        """Set socket timeout."""
        print(f"Mock Bluetooth: Setting timeout to {timeout}")
        self.timeout = timeout

    def send(self, data):
        print(f"Mock Bluetooth: Sent data {data}")
        return len(data)

    def recv(self, size):
        print(f"Mock Bluetooth: Received data (mock)")
        return b'MOCK_DATA'

    def close(self):
        print("Mock Bluetooth: Connection closed")
        self.connected = False


# Standard bluetooth constants
RFCOMM = 1
L2CAP = 2


def discover_devices(duration=8, lookup_names=True):
    print("Mock Bluetooth: Discovering devices")
    # Return a list of mock devices
    return [("00:11:22:33:44:55", "Mock Wearable Device")]