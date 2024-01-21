import serial
import time

# Adjust this to the virtual serial port created by socat
port_name = '/dev/pts/6'

ser = serial.Serial(port_name, 115200, timeout=1)

while True:
    ser.write(b'Hello from STIM300 simulator\n')
    time.sleep(1)  # Adjust delay as needed
