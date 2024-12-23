import time
import pigpio
import threading

# GPIO pins
OUTPUT_GPIO = 4  # GPIO pin for frequency generation
INPUT_GPIO = 17  # GPIO pin for frequency reading

# Frequency definitions for binary encoding
FREQ_ONE = 1200  # Frequency for binary "1"
FREQ_ZERO = 1000  # Frequency for binary "0"
START_MARKER = 1500  # Frequency for start marker
STOP_MARKER = 1300  # Frequency for stop marker
BIT_DURATION = 0.1  # Duration of each bit in seconds

pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit()

# Configure GPIO modes
pi.set_mode(OUTPUT_GPIO, pigpio.OUTPUT)
pi.set_mode(INPUT_GPIO, pigpio.INPUT)

# Thread synchronization lock
gpio_lock = threading.Lock()


def generate_square_wave(frequency, duration):
    """Generate a square wave for a specific frequency and duration."""
    period_us = int(1e6 / frequency)
    high_time = period_us // 2
    low_time = period_us - high_time

    wave = [
        pigpio.pulse(1 << OUTPUT_GPIO, 0, high_time),
        pigpio.pulse(0, 1 << OUTPUT_GPIO, low_time),
    ]
    pi.wave_add_generic(wave)
    wave_id = pi.wave_create()
    pi.wave_send_repeat(wave_id)

    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.01)  # Allow CPU to rest

    pi.wave_tx_stop()
    pi.wave_delete(wave_id)


def measure_frequency(duration=BIT_DURATION):
    """Measure the frequency on the input GPIO."""
    tick_list = []

    def cb_func(gpio, level, tick):
        if level == 1:  # Rising edge
            tick_list.append(tick)

    callback = pi.callback(INPUT_GPIO, pigpio.RISING_EDGE, cb_func)
    time.sleep(duration)
    callback.cancel()

    if len(tick_list) < 2:
        return 0  # Insufficient edges detected

    intervals = [tick_list[i] - tick_list[i - 1] for i in range(1, len(tick_list))]
    if not intervals:
        return 0  # No intervals to calculate frequency

    average_interval = sum(intervals) / len(intervals)
    frequency = 1e6 / average_interval  # Convert microseconds to Hz
    return frequency


def transmit_binary(data):
    """Transmit binary data with START and STOP markers."""
    with gpio_lock:
        generate_square_wave(START_MARKER, BIT_DURATION)
        time.sleep(BIT_DURATION)

        for bit in data:
            if bit == '1':
                generate_square_wave(FREQ_ONE, BIT_DURATION)
            elif bit == '0':
                generate_square_wave(FREQ_ZERO, BIT_DURATION)
            else:
                print(f"[ERROR] Invalid bit: {bit}")
            time.sleep(BIT_DURATION)

        generate_square_wave(STOP_MARKER, BIT_DURATION)
        time.sleep(BIT_DURATION)


def decode_frequencies():
    """Decode received frequencies into binary data."""
    binary_data = ""
    decoding = False

    while True:
        freq = measure_frequency(BIT_DURATION * 2)
        if freq == 0:
            continue

        if abs(freq - START_MARKER) <= 50:
            decoding = True
            binary_data = ""
            continue

        if decoding:
            if abs(freq - STOP_MARKER) <= 50:
                return binary_data

            if abs(freq - FREQ_ONE) <= 50:
                binary_data += "1"
            elif abs(freq - FREQ_ZERO) <= 50:
                binary_data += "0"
            else:
                print(f"[WARNING] Unknown frequency: {freq:.2f} Hz")


def encode_string_to_binary(message):
    """Convert a string to its binary representation."""
    return ''.join(format(ord(c), '08b') for c in message)


def decode_binary_to_string(binary):
    """Convert binary data back into a string."""
    return ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))


PASSWORD = "x4ef"


def receiver_thread():
    """Thread for continuously receiving and decoding messages."""
    while True:
        binary_data = decode_frequencies()
        if binary_data:
            decoded_message = decode_binary_to_string(binary_data)
            if decoded_message == PASSWORD:
                print(f"[AUTHENTICATED]")
            print(f"[RESULT] Received message: {decoded_message}")


def main():
    """Main function to handle transmission and reception."""
    receiver = threading.Thread(target=receiver_thread, daemon=True)
    receiver.start()
    time.sleep(3)

    try:
        while True:
            user_input = PASSWORD
            if user_input.lower() == 'exit':
                break

            binary_data = encode_string_to_binary(user_input)
            transmit_binary(binary_data)
    except KeyboardInterrupt:
        print("\n[INFO] Exiting...")
    finally:
        pi.stop()


if __name__ == "__main__":
    main()

