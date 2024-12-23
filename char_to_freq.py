#!/usr/bin/env python

import time
import pigpio
import threading

# GPIO pins
OUTPUT_GPIO = 4  # GPIO pin for frequency generation
INPUT_GPIO = 17  # GPIO pin for frequency reading

ACTIVE_TIME = 0.1
PASSIVE_TIME = 0.1

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit()

# Configure GPIO modes
pi.set_mode(OUTPUT_GPIO, pigpio.OUTPUT)
pi.set_mode(INPUT_GPIO, pigpio.INPUT)

NULL = '\0'

# Character-to-frequency mapping
CHAR_TO_FREQ = {chr(65 + i): 1000 + i * 50 for i in range(26)}  # A-Z
CHAR_TO_FREQ.update({chr(97 + i): 2300 + i * 50 for i in range(26)})  # a-z
CHAR_TO_FREQ.update({str(i): 3500 + i * 50 for i in range(10)})  # 0-9
CHAR_TO_FREQ[NULL] = 4000  # Terminator character
FREQ_TO_CHAR = {v: k for k, v in CHAR_TO_FREQ.items()}  # Reverse mapping for decoding
TOLERANCE = 25  # Frequency tolerance in Hz

# Generate square wave
def generate_square_wave(frequency, duty_cycle=0.5):
    period_us = int(1e6 / frequency)
    high_time = int(period_us * duty_cycle)
    low_time = period_us - high_time

    wave = [
        pigpio.pulse(1 << OUTPUT_GPIO, 0, high_time),
        pigpio.pulse(0, 1 << OUTPUT_GPIO, low_time)
    ]
    pi.wave_add_generic(wave)
    wave_id = pi.wave_create()
    return wave_id

# Measure frequency from input GPIO
def measure_frequency(duration=0.1):
    tick_list = []

    def cb_func(gpio, level, tick):
        if level == 1:  # Rising edge
            tick_list.append(tick)

    callback = pi.callback(INPUT_GPIO, pigpio.RISING_EDGE, cb_func)
    time.sleep(duration)  # Measure for `duration` seconds
    callback.cancel()

    if len(tick_list) < 2:
        return 0  # Not enough edges to calculate frequency

    # Calculate frequency
    intervals = [tick_list[i] - tick_list[i - 1] for i in range(1, len(tick_list))]
    average_interval = sum(intervals) / len(intervals)
    frequency = 1e6 / average_interval  # Convert microseconds to Hz
    return frequency

# Decode a frequency into a character
def decode_frequency(frequency):
    for freq, char in FREQ_TO_CHAR.items():
        if abs(frequency - freq) <= TOLERANCE:
            return char
    return None

# Transmit a string
def transmit_string(string):
    print(f"Transmitting string: {string}")
    for char in string:
        freq = CHAR_TO_FREQ.get(char)
        if freq:
            wave_id = generate_square_wave(freq)
            pi.wave_send_repeat(wave_id)
            print(f"Sent '{char}' as {freq} Hz")
            time.sleep(ACTIVE_TIME)
            pi.wave_tx_stop()
            pi.wave_delete(wave_id)
            time.sleep(PASSIVE_TIME)  # Pause between characters
        else:
            print(f"Unsupported character: '{char}'")

# Continuous receiver
def continuous_receiver():
    decoded_string = ""
    print("Receiver started. Waiting for signals...")

    while True:
        freq = measure_frequency(duration=ACTIVE_TIME)
        if freq > 0:
            char = decode_frequency(freq)
            if char:
                if char == NULL:  # Terminator character
                    print(f"Received string: {decoded_string}")
                    decoded_string = ""  # Reset for the next message
                else:
                    decoded_string += char
                    print(f"Received '{char}' (frequency: {freq:.2f} Hz)")
        time.sleep(PASSIVE_TIME)  # Small delay to avoid excessive CPU usage

# Main function
def main():
    # Start the continuous receiver in a separate thread
    receiver_thread = threading.Thread(target=continuous_receiver, daemon=True)
    receiver_thread.start()

    try:
        while True:
            user_input = input("Enter a string to transmit (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            # Append the terminator character to the message
            transmit_string(user_input + NULL)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pi.wave_tx_stop()
        pi.stop()

if __name__ == "__main__":
    main()

