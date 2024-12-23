import RPi.GPIO as GPIO
import time

from pathlib import Path

# Configure GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

def measure_pwm():
    # Variables to store measurement results
    high_time = 0
    low_time = 0

    # Wait for the pin to go HIGH
    while GPIO.input(17) == 0:
        pass

    # Measure HIGH duration
    start_time = time.time()
    while GPIO.input(17) == 1:
        pass
    high_time = time.time() - start_time

    # Measure LOW duration
    start_time = time.time()
    while GPIO.input(17) == 0:
        pass
    low_time = time.time() - start_time

    # Calculate frequency and duty cycle
    period = high_time + low_time
    frequency = 1 / period if period > 0 else 0
    duty_cycle = (high_time / period) * 100 if period > 0 else 0

    return frequency, duty_cycle

VLAD_FREQ = 2000
TEO_FREQ = 500

def decode_frequency(freq):
        if abs(frequency - VLAD_FREQ) < 100:
            return "Vlad"
        elif abs(frequency - TEO_FREQ) < 100:
            return "Teo"
        elif abs(frequency - 0) < 150:
            return ""
        else:
            return ""

try:
    last_person = ""
    image_file_path = Path.home() / ".image"
    while True:
        frequency, duty_cycle = measure_pwm()
        person = decode_frequency(frequency)
        if person:
            if person != last_person:
                print(image_file_path)
                image_file_path.write_text("/home/vlad/workspace/self-clone/id/" + person + ".jpeg" + "\n")
            if person == "Vlad":
                print(f"{person} e cel mai bun baiat al mamei!")
            if person == "Teo":
                print(f"{person} e cea mai buna fata a mamei!")
            #print(f"Frequency: {frequency:.2f} Hz, Duty Cycle: {duty_cycle:.2f}%")
        else:
            #print(f"Frequency: {frequency}")
            pass
        time.sleep(1)  # Adjust the sampling rate if needed
        last_person = person

except KeyboardInterrupt:
    print("\nExiting.")

finally:
    GPIO.cleanup()

