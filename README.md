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
4. Install pip install crcmod
5. pip install keyboard


## Running the Code

1. Download a zip of the files and unzip, or clone the repo
2. Open Terminal in the directory of the repo
3. run: "chmod +x setup.sh
4. run: "chmod +x run_client.sh
5. run: "chmod +x run_GUI.sh
6. To start the code, first run "./setup.sh", this creates the virtual serial connection
7. Next, to either start client or GUI, enter "./run_client" or "./run_GUI"

