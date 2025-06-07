# Test for i2c communications with a Raspberry Pi Pico and Arduino
import smbus
from time import sleep

# I2C channel 1 is connected to the GPIO pins
channel = 1
# Address of the Pico
p_address = 0x3E
# Address of the Arduino
a_address = 0x3F

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

i=1000
while 1:
    print ("Start loop "+str(i)+"\n")
    sleep (1)

    print ("Communicating with the Pico")
    try:
        print ("Writing data "+str(i))
        # Write out I2C command: address, cmd, msg[0]
        bus.write_i2c_block_data(p_address, i&0xff, [i>>8])
    except Exception as e:
        print ("Writing Error "+str(e))
        continue
    read = 0
    while read == 0:
        try:
            print ("Reading data")
            rx_bytes = bus.read_i2c_block_data(p_address, 0, 2)
        except Exception as e:
            print ("Read Error "+str(e))
            continue
        read = 1
    print ("Read "+str(rx_bytes))
    value = rx_bytes[0] + (rx_bytes[1] << 8)
    print ("Read value "+str(value))
    print ("\n")
    sleep(1)

    print ("Communicating with the Arduino")
    try:
        print ("Writing data "+str(i))
        # Write out I2C command: address, byte0, msg[0]
        bus.write_i2c_block_data(a_address, i&0xff, [i>>8])
    except Exception as e:
        print ("Writing Error "+str(e))
        continue
    read = 0
    while read == 0:
        try:
            print ("Reading data")
            #rx_bytes = bus.read_i2c_block_data(address, 7, 1)
            rx_bytes[0] = bus.read_byte(a_address);
            rx_bytes[1] = bus.read_byte(a_address);
        except Exception as e:
            print ("Read Error "+str(e))
            continue
        read = 1
    print ("Read "+str(rx_bytes))
    value = rx_bytes[0] + (rx_bytes[1] << 8)
    print ("Read value "+str(value))
    print ("\n")


    i+=1