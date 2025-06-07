#!/usr/bin/env python3
"""
pi_i2c_client.py

Example client for talking to a CircuitPython I2CTarget on a Pico W
(listening at 0x42, GP5=SCL, GP4=SDA).  

– Send “TEMP” → get back temperature in °C  
– Send “ID”   → get back Pico’s UID (hex string)  
– Send anything else → get back your last message
"""

import time
from smbus2 import SMBus, i2c_msg

I2C_BUS    = 1       # Raspberry Pi’s I2C bus (usually 1)
I2C_ADDR   = 0x42    # same as on your Pico’s code
MAX_LENGTH = 32      # must match the target’s buffer size

def send_command(bus, cmd: str):
    data = cmd.encode("ascii")
    write = i2c_msg.write(I2C_ADDR, data)
    bus.i2c_rdwr(write)

def read_response(bus, length=MAX_LENGTH) -> bytes:
    read = i2c_msg.read(I2C_ADDR, length)
    bus.i2c_rdwr(read)
    raw = bytes(read)
    # strip any trailing nulls
    return raw.rstrip(b'\x00')

def main():
    print(f"Opening I2C bus {I2C_BUS}, target address 0x{I2C_ADDR:02X}")
    with SMBus(I2C_BUS) as bus:
        while True:
            cmd = input("Enter command (TEMP, ID, or message; Q to quit): ").strip()
            if not cmd:
                continue
            if cmd.upper() in ("Q", "QUIT", "EXIT"):
                print("Bye!")
                break

            # send and read back
            send_command(bus, cmd)
            time.sleep(0.05)  # give the target a moment
            resp = read_response(bus)

            # try to decode as text, else show raw
            try:
                print("←", resp.decode("utf-8"))
            except UnicodeDecodeError:
                print("← (raw)", resp)

if __name__ == "__main__":
    main()

