#!/usr/bin/env python3
import time
from smbus2 import SMBus, i2c_msg

I2C_BUS  = 1
I2C_ADDR = 0x42
MAX_LEN  = 32

def send(bus, msg: str):
    bus.i2c_rdwr(i2c_msg.write(I2C_ADDR, msg.encode('ascii')))

def read(bus, length=MAX_LEN) -> bytes:
    msg = i2c_msg.read(I2C_ADDR, length)
    bus.i2c_rdwr(msg)
    raw = bytes(msg)
    # strip any trailing 0xFF or 0x00 padding
    return raw.rstrip(b'\xff').rstrip(b'\x00')

def main():
    print("+++ PI CLIENT START +++", flush=True)
    with SMBus(I2C_BUS) as bus:
        print(f"I2C bus {I2C_BUS}, target 0x{I2C_ADDR:02X}", flush=True)
        while True:
            cmd = input("CMD (TEMP, ID, or text; Q to quit): ").strip()
            if cmd.upper() in ('Q','QUIT','EXIT'):
                break
            if not cmd:
                continue

            print(">>> Sending:", cmd, flush=True)
            send(bus, cmd)
            time.sleep(0.05)

            print(">>> Reading response…", flush=True)
            resp = read(bus)
            if not resp:
                print("← (no data!)")
            else:
                try:
                    print("←", resp.decode('utf-8'), flush=True)
                except UnicodeDecodeError:
                    print("← (raw)", resp, flush=True)

if __name__ == "__main__":
    main()
