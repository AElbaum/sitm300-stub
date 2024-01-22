# sitm300-Interface
Testing interface for a sample IMU

## Overview of Code

# Simulator

The simulator simulates the STIM300, sending data over serial conenction to the client or the GUI.
It uses the `serial` library to create a virtual serial port.
The simulator generates the serial number and normal mode datagrams that are sent to the client.
CRC is also implemented as per the STIM300 datasheet.
The simulator continuisly listens for commands and responds to them.

# Client
The client communicates with the simulator over serial. A handshake occurs on startup to ensure that both parties have connected correctly.
Once connected, the client receives the serial number from the simulator, a sample "Normal Mode Datagram" and then prompts the user to input a frequency to poll the normal mode datagram at. Unfortunately, there is a bug where if the frequency is too high, a delay between the data received and the data proccessed results in the CRC becoming invalid. This bug will be solved in the future, but was outside the scope.

# GUI
The graphical user interface is built with tkinter and proviues a user-friender method for interacting with the simulator.
The GUI communicates with the simulator in a similar way to the client, over serial, but instead of dumping data in the termninal, the information is displayed on screen in the GUI.



## Steps for clean Ubuntu 22.04:

1. Install pip with
    sudo apt install python3-pip
2. Install pyserial
    pip install pyserial
3. Install socat
    sudo apt install socat
    Configure socat
        socat -d -d pty,raw,echo=0 pty,raw,echo=0
4. Install pip install crcmod
5. pip install keyboard


## Running the Code

1. Download a zip of the files and unzip, or clone the repo
2. Run the following command in terminal and leave the terminal open:
    socat -d -d pty,raw,echo=0 pty,raw,echo=0
    
    Note the ports that are created, the first time this is run, the ports will be /dev/pts/3 and /dev/pts/4,
    but if it has been run before you will need to note down the new port numbers and edit the scripts accordingly.
3. Open a terminal in the same directory as the code

