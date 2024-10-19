import pigpio
import curses
from time import sleep

# Initialize pigpio and servo pins
pi = pigpio.pi()  # Connect to pigpio daemon
servo1_pin = 18  # First servo pin
servo2_pin = 14  # Second servo pin

# Initial pulse width for both servos (corresponding to 0°)
pulse_width1 = 1500
pulse_width2 = 1500

# Define limits for pulse width
min_pulse_width = 500   # -90 degrees
max_pulse_width = 2500  # +90 degrees
step = 100  # Change the pulse width by 10µs per key press
delay_time = 0.01  # Time delay for each step in seconds

def move_servo(pin, pulse_width):
    """Move the servo to the given pulse width."""
    pi.set_servo_pulsewidth(pin, pulse_width)
    print(f"Moving servo on pin {pin} to pulse width: {pulse_width} µs")

def smooth_move(pin, current_pulse_width, target_pulse_width):
    """Smoothly move to the target pulse width."""
    while current_pulse_width != target_pulse_width:
        if current_pulse_width < target_pulse_width:
            current_pulse_width = min(current_pulse_width + step, target_pulse_width)
        else:
            current_pulse_width = max(current_pulse_width - step, target_pulse_width)
        
        move_servo(pin, current_pulse_width)
        sleep(delay_time)  # Short sleep to allow for smooth movement

    return current_pulse_width  # Return the new current pulse width

def main(stdscr):
    # Initialize curses screen
    curses.cbreak()
    stdscr.keypad(True)

    print("Use the arrow keys to move the servos:")
    print("Left/Right for Servo 1 (GPIO 18)")
    print("Up/Down for Servo 2 (GPIO 14)")
    print("Press 'q' to quit.")

    global pulse_width1, pulse_width2

    while True:
        char = stdscr.getch()  # Get key press

        if char == curses.KEY_RIGHT:
            if pulse_width1 + step <= max_pulse_width:
                pulse_width1 = smooth_move(servo1_pin, pulse_width1, pulse_width1 + step)

        elif char == curses.KEY_LEFT:
            if pulse_width1 - step >= min_pulse_width:
                pulse_width1 = smooth_move(servo1_pin, pulse_width1, pulse_width1 - step)

        elif char == curses.KEY_UP:
            if pulse_width2 + step <= max_pulse_width:
                pulse_width2 = smooth_move(servo2_pin, pulse_width2, pulse_width2 + step)

        elif char == curses.KEY_DOWN:
            if pulse_width2 - step >= min_pulse_width:
                pulse_width2 = smooth_move(servo2_pin, pulse_width2, pulse_width2 - step)

        elif char == ord('q'):  # Quit the program
            print("Exiting...")
            break

        sleep(0.1)  # Short sleep to reduce CPU usage

try:
    curses.wrapper(main)
finally:
    pi.set_servo_pulsewidth(servo1_pin, 1500)  # Turn off the first servo
    pi.set_servo_pulsewidth(servo2_pin, 1500)  # Turn off the second servo
    pi.stop()  # Close pigpio connection
