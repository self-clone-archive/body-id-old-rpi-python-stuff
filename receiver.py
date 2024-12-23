import time
from threading import Lock
import pigpio
from common import pi, INPUT_GPIO, FREQ_ONE, FREQ_ZERO, START_MARKER, STOP_MARKER, BIT_DURATION, decode_binary_to_string

PASSWORD = "x4ef"

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

    # Apply noise filtering: only consider frequencies within expected ranges
    if not (FREQ_ZERO - 100 <= frequency <= START_MARKER + 100):
        return 0
    return frequency


def decode_frequencies():
    """Decode received frequencies into binary data."""
    binary_data = ""
    decoding = False
    start_time = time.time()

    while True:
        freq = measure_frequency(BIT_DURATION * 2)

        if freq == 0:  # Skip noise
            continue

        if abs(freq - START_MARKER) <= 50:  # Start marker detected
            decoding = True
            binary_data = ""
            start_time = time.time()
            continue

        if decoding:
            if abs(freq - STOP_MARKER) <= 50:  # Stop marker detected
                return binary_data

            if abs(freq - FREQ_ONE) <= 50:
                binary_data += "1"
            elif abs(freq - FREQ_ZERO) <= 50:
                binary_data += "0"
            else:
                print(f"[WARNING] Unknown frequency: {freq:.2f} Hz")

            # Timeout for decoding session
            if time.time() - start_time > 5:
                print("[ERROR] Decoding timeout.")
                return ""


def receiver_thread():
    """Thread for continuously receiving and decoding messages."""
    while True:
        binary_data = decode_frequencies()
        if binary_data:
            try:
                decoded_message = decode_binary_to_string(binary_data)
                if decoded_message == PASSWORD:
                    print(f"[AUTHENTICATED]")
                else:
                    print(f"[FAIL] Received password: {decoded_message}")
            except Exception as e:
                print(f"[ERROR] Decoding error: {e}")


def main():
    try:
        receiver_thread()
    except KeyboardInterrupt:
        print("\n[INFO] Exiting...")
    finally:
        pi.stop()


if __name__ == "__main__":
    main()

