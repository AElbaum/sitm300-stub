import serial
import threading
import time
from struct import unpack
import sys
import crcmod


# Adjust this to the virtual serial port created by socat
port_name = '/dev/pts/7'

ser = serial.Serial(port_name, 115200, timeout=1) # Opens the serial port

start_time = time.time()
timeout = 10

def verify_crc(datagram, crc):
    poly = 0x104C11DB7
    crc_func = crcmod.mkCrcFun(poly, initCrc=0xFFFFFFFF, rev=False)
    calculated_crc = crc_func(datagram)
    # print("Calculated CRC: ", calculated_crc)
    return calculated_crc == crc

def decode_serialNumber(datagram):
    # Assuming the CRC is 4 bytes, CR and LF are 1 byte each
    datagram_without_crc_cr_lf = datagram[:-6]
    crc_received = unpack('>I', datagram[-6:-2])[0]

    if not verify_crc(datagram_without_crc_cr_lf, crc_received):
        raise ValueError("CRC check failed")

    # Unpack the datagram - adjust the format string to match your datagram structure
    datagram_format = '>18B'  # Example: 45 data bytes
    data = unpack(datagram_format, datagram_without_crc_cr_lf)
    # Extract the serial number or other relevant parts
    # This depends on how your data is structured
    serial_number = data[1:15]  # Example: bytes 2 to 15 contain the serial number
    # Convert bytes to a human-readable format if necessary
    serial_number_str = chr(serial_number[0]) + ''.join(format(byte, '02x') for byte in serial_number[1:])
    serial_number_str = serial_number_str.upper()  # Convert to uppercase

    return serial_number_str

while True:
    ser.write(b'CLIENT_READY\n')  # Send a message to the server to indicate readiness
    time.sleep(1)
    if ser.in_waiting > 0: # Checks if there is data in the buffer
        data = ser.readline() # Reads the data from the buffer
        if data[-2:] == b'\r\n':
            decoded_data = decode_serialNumber(data)
            print(decoded_data)
        else:
            decoded_data = data.decode().strip()
            if decoded_data == "SERVER_READY":
                print("Server has connected")
                break
    if time.time() - start_time > timeout:
        print("Server not ready, stopping script")
        sys.exit()


def check_serial():
    while True:
        if ser.in_waiting > 0: # Checks if there is data in the buffer
            data = ser.readline() # Reads the data from the buffer
            # print("The last two values are ", data[-2:])
            if data[-2:] == b'\r\n':
                # print("datagram detected")
                decoded_data = decode_serialNumber(data)
                print(decoded_data)

            else:
                # print("Data is not a datagram")
                decoded_data = data.decode().strip()
                print(decoded_data)



# Create a separate thread to check for incoming serial messages
threading.Thread(target=check_serial, daemon=True).start()

time.sleep(1)

def commands():
    if ser.out_waiting == 0:
        command = input("Enter a command: ")
        if command in ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]:
            ser.write(command.encode())
            # waiting_for_reply = True
            time.sleep(2) # Waits for 0.1 seconds before checking again
        else:
            print("Command not recognised, try agian.")


while True:
    commands()