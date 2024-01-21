#!/bin/bash

# Start socat to create virtual serial ports
socat -d -d pty,raw,echo=0 pty,raw,echo=0 &

SOCAT_PID=$!
echo "socat started with PID $SOCAT_PID"

# Start the simulator script
echo "Starting simulator..."
python3 /home/ariel/Documents/sitm300-stub/simulator_serial.py &

SIMULATOR_PID=$!
echo "Simulator started with PID $SIMULATOR_PID"

# Open the client script in a new terminal window
echo "Starting client in a new terminal..."
gnome-terminal -- /home/ariel/Documents/sitm300-stub/client_serial.py

CLIENT_PID=$!
echo "Client started with PID $CLIENT_PID"

# Wait for any process to exit
wait -n

# Once any process exits, kill the others
kill $SOCAT_PID
kill $SIMULATOR_PID
kill $CLIENT_PID

