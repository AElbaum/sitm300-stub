import serial
import threading
import time


# Adjust this to the virtual serial port created by socat
port_name = '/dev/pts/7'

ser = serial.Serial(port_name, 115200, timeout=1) # Opens the serial port

start_time = time.time()
timeout = 10

while True:
    ser.write(b'CLIENT_READY\n')  # Send a message to the server to indicate readiness
    time.sleep(1)
    if ser.in_waiting > 0: # Checks if there is data in the buffer
        data = ser.readline() # Reads the data from the buffer
        decoded_data = data.decode().strip()
        print(decoded_data) # Decodes the data and prints it
        if decoded_data == "SERVER_READY":
            print("Server has conencted")
            break
    if time.time() - start_time > timeout:
        print("Server not ready, timing out")
        break


def check_serial():
    while True:
        if ser.in_waiting > 0: # Checks if there is data in the buffer
            data = ser.readline() # Reads the data from the buffer
            decoded_data = data.decode().strip()
            print(decoded_data) # Decodes the data and prints it

# Create a separate thread to check for incoming serial messages
threading.Thread(target=check_serial, daemon=True).start()

def commands():
    if ser.out_waiting == 0:
        command = input("Enter a command: ")
        if command in ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]:
            ser.write(command.encode())
            # waiting_for_reply = True
            # time.sleep(3) # Waits for 0.1 seconds before checking again
        else:
            print("Command not recognised, try agian.")

time.sleep(1)

while True:
    commands()