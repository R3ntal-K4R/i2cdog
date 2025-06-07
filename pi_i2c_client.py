#!/usr/bin/env python3
import time
from smbus2 import SMBus, i2c_msg

I2C_BUS    = 1
I2C_ADDR   = 0x42
MAX_LEN    = 32

def send(bus, msg: str):
    bus.i2c_rdwr(i2c_msg.write(I2C_ADDR, msg.encode('ascii')))

def read(bus, n=MAX_LEN) -> bytes:
    read = i2c_msg.read(I2C_ADDR, n)
    bus.i2c_rdwr(read)
    return bytes(read).rstrip(b'\x00')

def main():
    with SMBus(I2C_BUS) as bus:
        print(f"I2C bus {I2C_BUS}, target 0x{I2C_ADDR:02X}")
        while True:
            cmd = input("CMD (TEMP, ID, or text; Q to quit): ").strip()
            if cmd.upper() in ('Q','QUIT','EXIT'):
                break
            if not cmd:
                continue
            send(bus, cmd)
            time.sleep(0.05)
            resp = read(bus)
            try:
                print("←", resp.decode())
            except:
                print("← (raw)", resp)

