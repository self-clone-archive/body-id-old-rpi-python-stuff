import time
import pigpio
from common import pi, OUTPUT_GPIO, FREQ_ONE, FREQ_ZERO, START_MARKER, STOP_MARKER, BIT_DURATION, encode_string_to_binary

PASSWORD = "x4ef"

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


def transmit_binary(data):
    """Transmit binary data with START and STOP markers."""
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


def main():
    try:
        while True:
            user_input = PASSWORD  # Replace with user input or fixed value
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

