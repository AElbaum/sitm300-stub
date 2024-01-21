import serial
import time


# Adjust this to the virtual serial port created by socat
port_name = '/dev/pts/7'

ser = serial.Serial(port_name, 115200, timeout=1) # Opens the serial port

def loop():
    if ser.in_waiting > 0: # Checks if there is data in the buffer
        data = ser.readline() # Reads the data from the buffer
        print(data.decode().strip()) # Decodes the data and prints it
    elif ser.out_waiting == 0:
    # Accept input from the terminal
        command = input("Enter a command: ")
        if command in ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]:
            ser.write(command.encode())
            time.sleep(3) # Waits for 0.1 seconds before checking again
        else:
            print("Command not recognised, try agian.")
        # Transmit the command over serial
        

    time.sleep(0.1) # Waits for 0.1 seconds before checking again

while True:
    loop()
    

# Commands in server mode