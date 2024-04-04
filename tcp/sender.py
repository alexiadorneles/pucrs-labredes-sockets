import socket

# Server configuration
SERVER_HOST = '192.168.64.3'  # Server's IP address
SERVER_PORT = 12345        # Port to connect to

def send_file(filename):
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # Send the file
        with open(filename, 'rb') as f:
            print(f"Sending file '{filename}'")
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
        print("File sent successfully")

if __name__ == "__main__":
    send_file("../large_file.txt")
