#!/usr/bin/env python3
import time
from smbus2 import SMBus, i2c_msg

I2C_BUS  = 1
I2C_ADDR = 0x42
MAX_LEN  = 32

def send(bus, msg: str):
    bus.i2c_rdwr(i2c_msg.write(I2C_ADDR, msg.encode('ascii')))

def read(bus, length=MAX_LEN) -> bytes:
    # Read exactly `length` bytes; SDA will float high (0xFF) if the slave
    # didn’t drive all of them.
    msg = i2c_msg.read(I2C_ADDR, length)
    bus.i2c_rdwr(msg)
    raw = bytes(msg)
    # Strip trailing 0xFF (bus idle) and 0x00 padding
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

            # 1) send
            print(f">>> Sending: {cmd!r}", flush=True)
            send(bus, cmd)
            time.sleep(0.05)

            # 2) read raw
            raw = read(bus)
            print(f">>> Raw bytes: {raw!r}", flush=True)

            # 3) attempt to decode
            try:
                s = raw.decode('ascii')
            except UnicodeDecodeError:
                s = None

            # 4) parse by command
            if cmd.upper() == "TEMP" and s is not None:
                # Expect something like "28.3C"
                print("← Temperature:", s)
            elif cmd.upper() == "ID" and s is not None:
                # UID is hex; group it nicely if you like
                uid = s.lower()
                print("← Pico UID:", uid)
            elif s is not None:
                # Echo case
                print("← Echoed message:", s)
            else:
                # Non-text or empty
                print("← (uninterpretable data)", raw)

if __name__ == "__main__":
    main()
