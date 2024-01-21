import tkinter
import serial
import tkinter.scrolledtext as st
import time
# from client_serial import loop
port_name = '/dev/pts/7'

ser = serial.Serial(port_name, 115200, timeout=1) # Opens the serial port

waiting_for_reply = False

def commands(cmd):
    global waiting_for_reply
    if ser.out_waiting == 0:
        if not waiting_for_reply: # Checks if the client is waiting for a reply
            # command = input("Enter a command: ")
            if cmd in ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]:
                ser.write(cmd.encode())
                waiting_for_reply = True
                output.insert(tkinter.END, f"Sending command: {cmd}\n")
            else:
                print("Command not recognised, try agian.")
                output.insert(tkinter.END, "Command not recognised, try again.\n")
    while waiting_for_reply:
        if ser.in_waiting > 0: # Checks if there is data in the buffer
            data = ser.readline() # Reads the data from the buffer
            decoded_data = data.decode().strip()
            print(decoded_data) # Decodes the data and prints it
            output.insert(tkinter.END, f"Received: {decoded_data}\n")
            waiting_for_reply = False


m = tkinter.Tk()

output = st.ScrolledText(m)
output.pack()

options = ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]
for command in options:
    button = tkinter.Button(m, text=command, command=lambda cmd=command: commands(cmd))
    button.pack()

m.mainloop()
