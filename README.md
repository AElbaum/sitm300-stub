# sitm300-Interface
Testing interface for a sample IMU

For an overview of how the code functions, see SYSTEM_DESIGN.ms



## Steps for clean Ubuntu 22.04:

1. Install pip with
    sudo apt install python3-pip
2. Install pyserial
    pip install pyserial
3. Install socat
    sudo apt install socat
    Configure socat
        socat -d -d pty,raw,echo=0 pty,raw,echo=0
4. Install pip
    pip install crcmod
5. Install Tkinter
    sudo apt install python3-tk

## Running the Code

1. Download a zip of the files and unzip, or clone the repo
2. Open Terminal in the directory of the repo
3. run: "chmod +x setup.sh
4. run: "chmod +x run_client.sh
5. run: "chmod +x run_GUI.sh
6. To start the code, first run "./setup.sh", this creates the virtual serial connection
    Check note of the output, it shoudl look like this:
    2024/01/23 23:50:09 socat[28832] N PTY is /dev/pts/1
    2024/01/23 23:50:09 socat[28832] N PTY is /dev/pts/2
    2024/01/23 23:50:09 socat[28832] N starting data transfer loop with FDs [5,5] and [7,7]

    If the ports are not /dev/pts/1 and /dev/pts/2, then type ctrl+C to kill the program and start it again, this should correct the error
    If this error remains, you may change the ports in the simulator_serial.py and client_serial.py files.



7. Next, to either start client or GUI, enter "./run_client" or "./run_GUI"
    These cannot be run at the same time, so make sure to close both simulator and client terminals before running the run_GUI.sh script
