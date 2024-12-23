import pigpio

pi = pigpio.pi()

if not pi.connected:
    print("pigpio daemon not running or connection failed")
    exit()

# Use GPIO 18 for PWM
pwm_pin = 18
frequency = 2000
duty_cycle = 50

# Set PWM frequency and duty cycle
pi.set_PWM_frequency(pwm_pin, frequency)
pi.set_PWM_dutycycle(pwm_pin, duty_cycle)

print(f"PWM set on GPIO {pwm_pin}: Frequency={frequency} Hz, Duty Cycle={duty_cycle}/255")

input("Press Enter to stop...")
pi.stop()

