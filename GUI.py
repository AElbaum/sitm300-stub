import tkinter
import serial
import tkinter.scrolledtext as st
import time
import threading
import crcmod
from pprint import pprint
from struct import unpack
from tkinter import simpledialog

print("GUI is starting")

# from client_serial import loop
port_name = '/dev/pts/2'

ser = serial.Serial(port_name, 115200, timeout=1) # Opens the serial port

start_time = time.time()
timeout = 10

m = tkinter.Tk()
m.title("STIM300 Stub GUI")
# m.geometry("500x500")


output = st.ScrolledText(m)
output.pack()

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
    datagram_dict = {}
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
        decoded_data = data.decode().strip()
        print(decoded_data) # Decodes the data and prints it
        if decoded_data == "SERVER_READY":
            print("Server has conencted")
            output.insert(tkinter.END, f"Server Connected\n")

            break
    if time.time() - start_time > timeout:
        print("Server not ready, timing out")
        break


def commands(cmd):
    if ser.out_waiting == 0:
        if cmd in ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]:
            ser.write(cmd.encode())
            output.insert(tkinter.END, f"Sending command: {cmd}\n")
        else:
            print("Command not recognised, try agian.")
            output.insert(tkinter.END, "Command not recognised, try again.\n")


def check_serial():
    while True:
        if ser.in_waiting > 0: # Checks if there is data in the buffer
            data = ser.readline() # Reads the data from the buffer
            # print("The last two values are ", data[-2:])
            if data[-2:] == b'\r\n':
                # print("datagram detected")
                # print(data)
                decoded_data = decode(data)
                output.insert(tkinter.END, f"Received: {decoded_data}\n")

                # print(decoded_data)
            elif data[-1:] == b'\n':
                print(data)

                output.insert(tkinter.END, f"Received: {data}\n")

            else:
                # print("Data is not a datagram")
                # print(data)
                decoded_data = data.decode().strip()
                output.insert(tkinter.END, f"Received: {decoded_data}\n")

                # print(decoded_data)


# Create a separate thread to check for incoming serial messages
threading.Thread(target=check_serial, daemon=True).start() # As requested, a GUI "that refreshes automatically when the data comes into the simulator"

# def NormalMode():

# def autoMode():
#     while True:
#         interval = 1
#         command = f'NormalMode {interval}\n'.encode()
#         ser.write(command)

def autoMode():
    interval = prompt_user()
    for i in range(5):
        command = f'NormalMode {interval}\n'.encode()
        ser.write(command)

def prompt_user():
    root = tkinter.Tk()
    root.withdraw()  # Hide the main window
    user_input = simpledialog.askstring(title="Test", prompt="Please enter a Frequency (Hz):")
    return user_input        

options = ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]
for command in options:
    button = tkinter.Button(m, text=command, command=lambda cmd=command: commands(cmd))
    button.pack()

serialButton = tkinter.Button(m, text="Test Serial Command", command=lambda: commands("I"))
# normalButton = tkinter.Button(m, text="Test Normal Mode", command=lambda: normalMode())
autoButton = tkinter.Button(m, text="Test Auto Mode", command=lambda: autoMode())

# normalButton.pack()
serialButton.pack()
autoButton.pack()

m.mainloop()
