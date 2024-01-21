import serial
import time

# Adjust this to the virtual serial port created by socat
port_name = '/dev/pts/7'

ser = serial.Serial(port_name, 115200, timeout=1)

while True:
    if ser.in_waiting > 0:
        data = ser.readline()
        print(data.decode().strip())
    time.sleep(0.1)  # Adjust delay as needed
