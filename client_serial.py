import serial
import threading
import time
from struct import unpack
import sys
import crcmod
from pprint import pprint
import queue



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


def decode(datagram):
    # Assuming the CRC is 4 bytes, CR and LF are 1 byte each
    datagram_without_crc_cr_lf = datagram[:-6]
    crc_received = unpack('>I', datagram[-6:-2])[0]

    if not verify_crc(datagram_without_crc_cr_lf, crc_received):
        # raise ValueError("CRC check failed")
        print("CRC check failed, likely because of asynchronous serial communication")

    # Unpack the datagram - adjust the format string to match your datagram structure
    byte_count = len(datagram_without_crc_cr_lf)
    # print("Byte count: ", byte_count)
    # Use the byte count in the format string
    datagram_format = '>' + str(byte_count) + 'B'
    data = unpack(datagram_format, datagram_without_crc_cr_lf)

    # Check if serial datagram
    if byte_count == 18:
        serial_number = data[1:byte_count-1]  # Example: bytes 2 to (byte_count-1) contain the serial number
        # Convert bytes to a human-readable format if necessary
        serial_number_str = chr(serial_number[0]) + ''.join(format(byte, '02x') for byte in serial_number[1:])
        serial_number_str = serial_number_str.upper()  # Convert to uppercase

        print(serial_number_str)
        return serial_number_str

    elif byte_count == 23:

        datagram_dict = {
            "Datagram identifier": data[0],
            "Gyro output": data[1:4],
            "Gyro status byte": data[4],
            "Accel output": data[5:8],
            "Accel status byte": data[8],
            "Inclinometer output": data[9:12],
            "Inclinometer status byte": data[12],
            "Gyro temp data": data[13],
            "Gyro temp status byte": data[14],
            "Accel temp data": data[15],
            "Accel temp status byte": data[16],
            "Inclinometer temp data": data[17],
            "Inclinometer temp status byte": data[18],
            "Aux output": data[19],
            "Aux status byte": data[20],
            "Counter": data[21],
            "Random byte": data[22]
        }
        pprint(datagram_dict)
    return datagram_dict

while True:
    ser.write(b'CLIENT_READY\n')  # Send a message to the server to indicate readiness
    time.sleep(1)
    if ser.in_waiting > 0: # Checks if there is data in the buffer
        data = ser.readline() # Reads the data from the buffer
        if data[-2:] == b'\r\n':
            decoded_data = decode(data)
            print(decoded_data)
        else:
            decoded_data = data.decode().strip()
            if decoded_data == "SERVER_READY":
                print("Server has connected")
                break
    if time.time() - start_time > timeout:
        print("Server not ready, stopping script")
        sys.exit()

data_queue = queue.Queue()

stop_thread = threading.Event()
def check_serial():
    while True:
        if ser.in_waiting > 0: # Checks if there is data in the buffer
            data = ser.readline() # Reads the data from the buffer
            data_queue.put(data)
            # print("The last two values are ", data[-2:])
            if data[-2:] == b'\r\n':
                # print("datagram detected")
                # print(data)
                data = data_queue.get()
                decoded_data = decode(data)
                # print(decoded_data)
            elif data[-1:] == b'\n':
                data = data_queue.get()
                print(data)
            else:
                # print("Data is not a datagram")
                # print(data)
                data = data_queue.get()
                decoded_data = data.decode().strip()
                # print(decoded_data)



# Create a separate thread to check for incoming serial messages
thread = threading.Thread(target=check_serial, daemon=True)
thread.start()

time.sleep(1)

# if ser.out_waiting == 0:
frequency = float(input("Enter a frequency (Hz) less than 1 for normal datagram requests: "))
interval = 1.0 / frequency  # Convert frequency to interval in seconds

while True:
    # stop_thread.set()
    # time.sleep(interval)
    # Send message with "Normal Mode" command and the interval length
    command = f'NormalMode {interval}\n'.encode()
    ser.write(command)


