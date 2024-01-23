import serial
import random
import time
from struct import pack
import sys
import crcmod

counter = 0

# Adjust this to the virtual serial port created by socat
# port_name = sys.argv[0]
port_name = '/dev/pts/1'

ser = serial.Serial(port_name, 115200, timeout=1) 


start_time = time.time()
timeout = 20 

def calculate_crc(data):
    # From 5.5.7: x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1
    # This is represented in hexadecimal as 0x104C11DB7
    poly = 0x104C11DB7

    # Create a crc function with the specified polynomial and seed
    crc_func = crcmod.mkCrcFun(poly, initCrc=0xFFFFFFFF, rev=False)

    # Calculate CRC
    crc = crc_func(data)
    # print("CRC: ", crc)

    return crc





# function that sends serial number to client
def serialNumber():
    # print("Serial Number triggered")
# Define the datagram structure
    datagram_format = ">18B"
    
# Create the datagram data
    data = [ # Serial number: N0123456789ABCDEF
        0xB7,  # Datagram identifier (without CR+LF termination)
        0x4E,  # ASCII character for letter "N"
        0x01,  
        0x23,  
        0x45,  
        0x67,  
        0x89,  
        0xAB,  
        0xCD,
        0xEF,
        0x00,  # For future use
        0x00,  # For future use
        0x00,  # For future use
        0x00,  # For future use
        0x00,  # For future use
        0x00,  # For future use
        0x00,  # For future use
        0x00,  # For future use
        # CRC byte 1
        # CRC byte 2
        # 0x0D,  # CR to be appended later
        # 0x0A,  # LF to be appended later
    ]

    # Convert the data to bytes
    datagram_bytes = pack(datagram_format, *data)
    # print("Datagram: ", datagram_bytes)
    # Calculate CRC
    crc = calculate_crc(datagram_bytes)

    # Append CRC to the datagram
    datagram_with_crc = datagram_bytes + pack(">I", crc) + b'\x0D\x0A'

    ser.write(b'SerialNumber:\n')
    ser.write(datagram_with_crc)
    # return datagram_with_crc
    
def normalModeDatagram():
    global counter  

    datagram_format = ">23B"

    gyro_x, gyro_y, gyro_z = (int(random.uniform(0, 255)) for _ in range(3))
    accel_x, accel_y, accel_z = (int(random.uniform(0, 10)) for _ in range(3))
    inclinometer_x, inclinometer_y, inclinometer_z = (int(random.uniform(0, 3)) for _ in range(3))
    gyro_temp = int(random.uniform(0, 100))
    accel_temp = int(random.uniform(0, 100))
    inclinometer_temp = int(random.uniform(0, 100))
    aux_output = int(random.uniform(0, 3))

    data = [
        0b10101111, # Datagram identifier
        gyro_x, gyro_y, gyro_z, # Gyro output
        0b00000000, # Gyro status byte
        accel_x, accel_y, accel_z, # Accel output
        0b00000000, # Accel status byte
        inclinometer_x, inclinometer_y, inclinometer_z, # Inclinometer output
        0b00000000, # Inclinometer status byte
        gyro_temp, # Gyro temp data
        0b00000000, # Gyro temp status byte
        accel_temp, # Accel temp data
        0b00000000,    # Accel temp status byte
        inclinometer_temp, # Inclinometer temp data
        0b00000000, # Inclinometer temp status byte
        aux_output, # Aux output
        0b00000000, # Aux status byte
        counter, # Counter
        random.randint(0, 255)
        #random.randint(0, 65535), # Latency as unsigned word
        # CRC byte 1
        # CRC byte 2
        # 0x0D,  # CR to be appended later
        # 0x0A,  # LF to be appended later
    ]

    counter = (counter + 1) % 256 # Increment counter and wrap around at 256


    # Convert the data to bytes
    datagram_bytes = pack(datagram_format, *data)
    # print("Datagram: ", datagram_bytes)
    # Calculate CRC
    crc = calculate_crc(datagram_bytes)

    # Append CRC to the datagram
    datagram_with_crc = datagram_bytes + pack(">I", crc) + b'\x0D\x0A'

    ser.write(b'NormalMode:\n')
    ser.write(datagram_with_crc)
    # print(datagram_with_crc)

def partNumber():
    ser.write(b'Part Number datagram is unavailable, try a different command\n')

def configuration():
    ser.write(b'Configuration datagram\n')

def biasTrimOffset():
    ser.write(b'Bias Trim Offset datagram is unavailable, try a different command\n')

def error():
    ser.write(b'Error datagram is unavailable, try a different command\n')

def reset():
    ser.write(b'Reset datagram is unavailable, try a different command\n')

def serviceMode():
    ser.write(b'Service mode is unavailable, try a different command\n')

def utilityMode():
    ser.write(b'Utility mode is unavailable, try a different command\n')




print("Starting up the simulator")
while True:
    global command
    if ser.in_waiting > 0:
        data = ser.readline()
        command = data.decode().strip()
        # print(command)
        if command == "CLIENT_READY":
            print("Client has connected")
            ser.write(b'SERVER_READY\n')
            ser.reset_input_buffer()
            serialNumber() 
            normalModeDatagram()
            break
    if time.time() - start_time > timeout:
        print("Server not ready, exiting script")
        sys.exit()



while True:
    if ser.in_waiting > 0:  # Checks if there is data in the buffer
        data = ser.readline()  # Reads the data from the buffer
        command = data.decode().strip()
        print("Received message: ", command)  # Decodes the data and prints it
        if command.startswith("NormalMode"):
            interval = float(command.split()[1])
            time.sleep(interval)
            normalModeDatagram()
            # time.sleep(2)
        elif command == "N":
            partNumber()
        elif command == "I":
            serialNumber()
        elif command == "C":
            configuration()
        elif command == "T":
            biasTrimOffset()
        elif command == "E":
            error()
        elif command == "R":
            reset()
        elif command == "SERVICEMODE":
            serviceMode()
        elif command == "UTILITYMODE":
            utilityMode()
        else:
            print("Command not recognised, try again.")
