#!/bin/bash


# Start the simulator script
echo "Starting simulator..."
python3 /home/ariel/Documents/sitm300-stub/simulator_serial.py &

SIMULATOR_PID=$!
echo "Simulator started with PID $SIMULATOR_PID"

# Open the client script in a new terminal window
echo "Starting GUI in a new terminal..."
gnome-terminal -- /home/ariel/Documents/sitm300-stub/GUI.py

CLIENT_PID=$!
echo "Client started with PID $CLIENT_PID"

# Wait for any process to exit
wait -n

# Once any process exits, kill the others
kill $SOCAT_PID
kill $SIMULATOR_PID
kill $CLIENT_PID

