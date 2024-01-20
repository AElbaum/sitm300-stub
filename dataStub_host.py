# Test code to simulate a STIM300 IMU sending data
import socket
import time

def create_server(host, port): # Create a server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening on {host}:{port}")
    return server

def main(): # Accept a connection and send data
    host = '127.0.0.1'  # Localhost
    port = 65432        # Non-privileged port

    server = create_server(host, port)
    
    while True:
        conn, addr = server.accept()
        print(f"Connected by {addr}")
        try:
            while True:
                # Simulate sending data - this is where you'd format your STIM300 datagram
                data = "Hello World"
                conn.sendall(data.encode())
                time.sleep(1)  # Pause for a bit before sending the next message
        except socket.error:
            print("Connection closed.")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
