import serial

# Adjust this to the virtual serial port created by socat
port_name = '/dev/pts/7'

ser = serial.Serial(port_name, 115200, timeout=1) # Opens the serial port

waiting_for_reply = False


def commands():
    global waiting_for_reply
    if ser.in_waiting > 0: # Checks if there is data in the buffer
        data = ser.readline() # Reads the data from the buffer
        print(data.decode().strip()) # Decodes the data and prints it
        waiting_for_reply = False
    elif ser.out_waiting == 0:
    # Accept input from the terminal
        if not waiting_for_reply: # Checks if the client is waiting for a reply
            command = input("Enter a command: ")
            if command in ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]:
                ser.write(command.encode())
                waiting_for_reply = True
                # time.sleep(3) # Waits for 0.1 seconds before checking again
            else:
                print("Command not recognised, try agian.")

while True:
    commands()