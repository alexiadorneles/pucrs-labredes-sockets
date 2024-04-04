import socket

# Server configuration
HOST = '127.0.0.1'  # Loopback address
PORT = 12345        # Port to listen on
BUFFER_SIZE = 1024  # Size of the buffer for receiving data

def receive_file(filename):
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))
        # Listen for incoming connections
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        
        # Accept a connection
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        with conn:
            print(f"Receiving file '{filename}'")
            with open(filename, 'wb') as f:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)
            print("File received successfully")

if __name__ == "__main__":
    receive_file("received_file.txt")
