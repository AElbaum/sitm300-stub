import tkinter
import serial
import tkinter.scrolledtext as st
import time
import threading

# from client_serial import loop
port_name = '/dev/pts/7'

ser = serial.Serial(port_name, 115200, timeout=1) # Opens the serial port

start_time = time.time()
timeout = 10

m = tkinter.Tk()
m.title("STIM300 Stub GUI")
# m.geometry("500x500")


output = st.ScrolledText(m)
output.pack()

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
            decoded_data = data.decode().strip()
            print(decoded_data) # Decodes the data and prints it
            output.insert(tkinter.END, f"Received: {decoded_data}\n")

# Create a separate thread to check for incoming serial messages
threading.Thread(target=check_serial, daemon=True).start() # As requested, a GUI "that refreshes automatically when the data comes into the simulator"



options = ["N", "I", "C", "T", "E", "R", "SERVICEMODE", "UTILITYMODE"]
for command in options:
    button = tkinter.Button(m, text=command, command=lambda cmd=command: commands(cmd))
    button.pack()

m.mainloop()
