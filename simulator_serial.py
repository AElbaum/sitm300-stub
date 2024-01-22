import serial
import random
import time
from struct import pack
import sys
import crcmod




# Adjust this to the virtual serial port created by socat
port_name = '/dev/pts/6'

ser = serial.Serial(port_name, 115200, timeout=1) 


start_time = time.time()
timeout = 10  # 10 seconds

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

def normalModeDatagram():
    
    # Status bits
    status = 0b10101111
    # Gyro output
    gyro_x, gyro_y, gyro_z = [random.uniform(-300, 300) for _ in range(3)]  # Gyro data    # Gyro status byte
    # Accel output
    # Accel status byte
    # Inclinometer output
    # Inclinometer status byte
    # Gyro temp data
    # Gyro temp status byte
    # Accel temp data
    # Accel temp status byte
    # Inclinometer temp data
    # Inclinometer temp status byte
    # Aux output
    # Aux status byte
    # Counter
    #Latency
    #CRC
    # CR
    # LF
    ser.write(b'normalModeDatagram\n')


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
        if command == "N":
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
