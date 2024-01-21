import serial
import random

# Adjust this to the virtual serial port created by socat
port_name = '/dev/pts/6'

ser = serial.Serial(port_name, 115200, timeout=1) 

def onStart():
    print("Starting up the simulator")
    serialNumber()
    normalModeDatagram()

# function that sends serial number to client
def serialNumber():
    ser.write(b'SerialNumber\n')

def partNumber():
    ser.write(b'partNumber\n')

def configuration():
    ser.write(b'configuration\n')


def biasTrimOffset():
    ser.write(b'biasTrimOffset\n')

def error():
    ser.write(b'error\n')

def reset():
    ser.write(b'reset\n')

def serviceMode():
    ser.write(b'serviceMode\n')

def utilityMode():
    ser.write(b'utilityMode\n')

def normalModeDatagram():
    # Status bits
    status = 0b10101111
    # Gyro output
    gyro_x, gyro_y, gyro_z = [random.uniform(-300, 300) for _ in range(3)]  # Gyro data    # Gyro status byte
    # Accel output
    # Accel status byte
    # Inclinometer output
    # Inclinometer status byte
    # Gyro temp data
    # Gyro temp status byte
    # Accel temp data
    # Accel temp status byte
    # Inclinometer temp data
    # Inclinometer temp status byte
    # Aux output
    # Aux status byte
    # Counter
    #Latency
    #CRC
    # CR
    # LF

while True:
    if ser.in_waiting > 0:  # Checks if there is data in the buffer
        data = ser.readline()  # Reads the data from the buffer
        command = data.decode().strip()
        print("Received message: ", command)  # Decodes the data and prints it
        if command == "N":
            partNumber()
        elif command == "I":
            serialNumber()
        elif command == "C":
            configuration()
        elif command == "T":
            biasTrimOffset()
        elif command == "E":
            error()
        elif command == "R":
            reset()
        elif command == "SERVICEMODE":
            serviceMode()
        elif command == "UTILITYMODE":
            utilityMode()
        else:
            print("Command not recognised, try again.")