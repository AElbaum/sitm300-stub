# Description: This file is used to test the datagram format without having to use serial connections

import random
import struct
import random

def generate_crc(datagram):
    crc = random.randint(0, 65535)
    return crc

def normalMode():
    # Status bits
    status = 0b10101111
    # Gyro output
    # gyro_x, gyro_y, gyro_z = [random.uniform(-300, 300) for _ in range(3)]  # Gyro data    # Gyro status byte
    gyro_data = [random.uniform(-300, 300) for _ in range(3)]  # Gyro data for X, Y, Z axes
    # Accel output
    accel_data = [random.uniform(-300, 300) for _ in range(3)]  # Accel data for X, Y, Z axes
    # Accel status byte
    # Inclinometer output
    inclinometer_data = [random.uniform(-300, 300) for _ in range(3)]  # Inclinometer data for X, Y, Z axes
    # Inclinometer status byte
    # Gyro temp data which is 16 bits long
    gyro_temp_data = 
    # Gyro temp status byte
    # Accel temp data
    # Accel temp status byte
    # Inclinometer temp data
    # Inclinometer temp status byte
    # Aux output
    # Aux status byte
    # Counter
    #Latency
    datagram = struct.pack('>Bffffff', status, *gyro_data, *accel_data, *inclinometer_data)
    #CRC
    crc = generate_crc(datagram)
    datagram += struct.pack('>H', crc)
    # CR
    # LF
    return datagram


def print_dynamic_datagram(datagram):
    datagram_format = '>BfffH'

    # Unpack the datagram based on the specified format
    unpacked_data = struct.unpack(datagram_format, datagram)

    # Dynamically print each element of the datagram
    print("Datagram Content:")
    for i, value in enumerate(unpacked_data):
        if i == 0:
            print(f"Status Byte: {value}")
        elif i < len(unpacked_data) - 1:  # Assuming the last value is CRC
            print(f"Data {i}: {value}")
        else:
            print(f"CRC: {value}")


# 


datagram = normalMode()
print_dynamic_datagram(datagram)

# status, gyro_x, gyro_y, gyro_z = struct.unpack('>Bfff', datagram)
