import pigpio

# Frequency definitions for binary encoding
FREQ_ONE = 1200  # Frequency for binary "1"
FREQ_ZERO = 1000  # Frequency for binary "0"
START_MARKER = 1500  # Frequency for start marker
STOP_MARKER = 1300  # Frequency for stop marker
BIT_DURATION = 0.05  # Duration of each bit in seconds

# GPIO pins
#OUTPUT_GPIO = 4  # GPIO pin for frequency generation
OUTPUT_GPIO = 13 # PWM GPIO pin for frequency generation
INPUT_GPIO = 17  # GPIO pin for frequency reading

# Pigpio instance
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit()

def encode_string_to_binary(message):
    """Convert a string to its binary representation."""
    return ''.join(format(ord(c), '08b') for c in message)


def decode_binary_to_string(binary):
    """Convert binary data back into a string."""
    return ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))

