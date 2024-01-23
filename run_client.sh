#!/bin/bash


# Start the simulator script with port1
echo "Starting simulator..."
gnome-terminal -- bash -c "python3 /home/ariel/Documents/sitm300-stub/simulator_serial.py" &

SIMULATOR_PID=$!

sleep 1

# Start the client with port2
echo "Starting the client"
gnome-terminal -- bash -c "python3 /home/ariel/Documents/sitm300-stub/client_serial.py"

CLIENT_PID=$!

