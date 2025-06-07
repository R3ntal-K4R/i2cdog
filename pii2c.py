# controller.py for Raspberry Pi
# This script configures the Pi as an I2C controller to communicate with the Pico.

import smbus2
import time

# --- Setup ---
# On your Raspberry Pi, you must first enable the I2C interface.
# You can do this by running `sudo raspi-config` in the terminal,
# navigating to 'Interface Options', and enabling 'I2C'.

# You also need to install the smbus2 library:
# pip install smbus2

# --- Configuration ---
# I2C bus number. On most modern Raspberry Pi models (2, 3, 4, Zero), this is 1.
# On the original Model B (rev 1), it was 0.
I2C_BUS_NUM = 1

# The I2C address of the Pico peripheral. This MUST match the address
# set in the Pico's CircuitPython code.
PICO_I2C_ADDRESS = 0x42


def write_to_pico(bus, message):
    """Sends a string message to the Pico."""
    try:
        # Convert the string to a list of bytes (ASCII values)
        data = [ord(c) for c in message]
        print(f"Attempting to write to {hex(PICO_I2C_ADDRESS)}: '{message}'")
        # The write_i2c_block_data function sends a block of data.
        # It takes the address, a command byte (0 here), and the data list.
        bus.write_i2c_block_data(PICO_I2C_ADDRESS, 0, data)
        print("Write successful.")
    except OSError as e:
        print(f"Error writing to I2C device: {e}")
        print("Is the Pico connected and running the correct code?")

def read_from_pico(bus, num_bytes):
    """Reads a specified number of bytes from the Pico."""
    try:
        print(f"Attempting to read {num_bytes} bytes from {hex(PICO_I2C_ADDRESS)}...")
        # The read_i2c_block_data function reads a block of data.
        # It takes the address, a command byte (0 here), and the number of bytes to read.
        data = bus.read_i2c_block_data(PICO_I2C_ADDRESS, 0, num_bytes)
        # Convert the list of bytes back into a string
        message = "".join([chr(b) for b in data])
        print(f"Read successful. Received: '{message}'")
        return message
    except OSError as e:
        print(f"Error reading from I2C device: {e}")
        print("Is the Pico connected and running the correct code?")
        return None

def main():
    """Main function to run the I2C communication."""
    try:
        # Initialize the SMBus object for the specified I2C bus.
        bus = smbus2.SMBus(I2C_BUS_NUM)
        print(f"I2C Bus {I2C_BUS_NUM} opened.")
    except FileNotFoundError:
        print(f"Error: I2C bus {I2C_BUS_NUM} not found.")
        print("Please ensure the I2C interface is enabled in raspi-config.")
        return

    # Use a 'with' statement to ensure the bus is closed properly
    with bus:
        # --- Communication Loop ---
        try:
            while True:
                # 1. Write a message to the Pico
                write_to_pico(bus, "Hi from RPi!")

                # Wait a moment
                time.sleep(2)

                # 2. Read the response from the Pico
                # We expect "Hello from Pico!", which is 16 characters.
                read_from_pico(bus, 16)

                # Wait before repeating
                print("\n--- Waiting 5 seconds before next cycle ---")
                time.sleep(5)

        except KeyboardInterrupt:
            print("\nProgram stopped by user.")

if __name__ == "__main__":
    mai
