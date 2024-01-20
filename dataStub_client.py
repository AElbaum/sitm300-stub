# Test code to simulate a STIM300 IMU receiving data
import socket

def create_client(host, port): # Create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client

def main(): # Connect to the server and print the data received
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 65432        # The port used by the servers

    client = create_client(host, port)

    try:
        while True:
            data = client.recv(1024)  # Buffer size is 1024 bytes
            if not data:
                break
            print("Received:", data.decode())
    finally:
        client.close()

if __name__ == "__main__":
    main()
