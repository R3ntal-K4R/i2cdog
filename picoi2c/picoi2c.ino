# code.py for Raspberry Pi Pico
# This script configures the Pico as an I2C peripheral device.
# It will listen for requests from the controller (the Raspberry Pi).

import board
import microcontroller
import i2cperipheral
import time

# --- Configuration ---
# Define the I2C address for the Pico. This must match the address used by the
# controller. 7-bit addresses are standard. 0x42 is just an example.
PICO_I2C_ADDRESS = 0x42

# Define the I2C pins.
# You can use any I2C-capable pins on the Pico.
# board.GP5 is SCL, board.GP4 is SDA for I2C0
i2c_scl_pin = board.GP5
i2c_sda_pin = board.GP4

# --- State ---
# Create a buffer to hold data received from the controller.
# We'll make it 32 bytes for this example.
received_data = bytearray(32)

# Create a message to send back to the controller when it requests data.
# This must be bytes.
message_to_send = b"Hello from Pico!"

# --- Setup ---
# Initialize the I2C peripheral object.
# The 'i2cperipheral' library is built into modern versions of CircuitPython.
try:
    i2c = i2cperipheral.I2CPeripheral(
        scl=i2c_scl_pin,
        sda=i2c_sda_pin,
        address=PICO_I2C_ADDRESS
    )
    print(f"I2C Peripheral listening on address: {hex(PICO_I2C_ADDRESS)}")
except ValueError:
    print("I2C pins already in use. This can happen on soft reloads.")
    # On a soft-reload, board.I2C() may still be in use.
    # A hard reset (unplug/replug) will fix this.
    # For this script, we'll try to deinit and re-init.
    board.I2C().deinit()
    i2c = i2cperipheral.I2CPeripheral(
        scl=i2c_scl_pin,
        sda=i2c_sda_pin,
        address=PICO_I2C_ADDRESS
    )


# --- Main Loop ---
while True:
    # i2c.request() waits for an I2C transaction from the controller.
    # It returns an object representing the request, or None if there's a timeout.
    request = i2c.request()

    if request:
        print("-" * 20)
        # Check if the controller wants to write data to us
        if not request.is_read:
            print(f"Controller wrote {request.address} (our address)")
            # Read the data sent by the controller into our buffer
            bytes_read = request.read(n=len(received_data))
            if bytes_read:
                # Decode the bytes into a string for printing
                message = received_data[:bytes_read].decode()
                print(f"Received {bytes_read} bytes: '{message}'")
                # You could add logic here to parse commands, e.g., if message == "LED_ON":

        # Check if the controller wants to read data from us
        elif request.is_read:
            print(f"Controller read from {request.address} (our address)")
            # Write our predefined message back to the controller
            bytes_written = request.write(message_to_send)
            print(f"Sent {bytes_written} bytes: '{message_to_send.decode()}'")

        # The 'with' block automatically handles closing the request.

    # A small delay to prevent the loop from running too fast
    time.sleep(0.01)

