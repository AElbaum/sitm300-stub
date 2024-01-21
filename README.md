# sitm300-Interface
Testing Interface for a sample IMU


Steps for clean Ubuntu 22.04:

1. Install pip with
    sudo apt install python3-pip
2. Install pyserial
    pip install pyserial
3. Install socat
    sudo apt install socat
    Configure socat
        socat -d -d pty,raw,echo=0 pty,raw,echo=0