#!/usr/bin/env python3
"""
pi_i2c_client.py

Talk to your Pico W at 0x42:
  – Send "TEMP" → get back temperature in °C
  – Send "ID"   → get back Pico’s UID (hex string)
  – Send anything else → get back your last message
"""

import time
from smbus2 import SMBus, i2c_msg

I2C_BUS  = 1
I2C_ADDR = 0x42
MAX_LEN  = 32

def send(bus, msg: str):
    write = i2c_msg.write(I2C_ADDR, msg.encode('ascii'))
    bus.i2c_rdwr(write)

def read(bus, length=MAX_LEN) -> bytes:
    read = i2c_msg.read(I2C_ADDR, length)
    bus.i2c_rdwr(read)
    return bytes(read).rstrip(b'\x00')

def main():
    print(f"+++ STARTING pi_i2c_client.py +++", flush=True)
    with SMBus(I2C_BUS) as bus:
        print(f"I2C bus {I2C_BUS}, target 0x{I2C_ADDR:02X}", flush=True)
        while True:
            cmd = input("CMD (TEMP, ID, or text; Q to quit): ").strip()
            if cmd.upper() in ('Q', 'QUIT', 'EXIT'):
                print("Bye!")
                break
            if not cmd:
                continue

            print(f">>> Sending: {cmd!r}", flush=True)
            send(bus, cmd)
            time.sleep(0.05)

            print(">>> Reading response…", flush=True)
            resp = read(bus)
            try:
                print("←", resp.decode('utf-8'), flush=True)
            except UnicodeDecodeError:
                print("← (raw)", resp, flush=True)

if __name__ == "__main__":
    main()
