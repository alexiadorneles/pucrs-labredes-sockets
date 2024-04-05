import socket

# Server configuration
SERVER_HOST = '192.168.64.3'  # Server's IP address
SERVER_PORT = 12345        # Port to send to
BUFFER_SIZE = 1024         # Size of the buffer for sending data
END_MESSAGE = b"END_TRANSFER"  # Message to indicate end of file transfer

def send_file(filename):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Send the file
        with open(filename, 'rb') as f:
            print(f"Sending file '{filename}'")
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                client_socket.sendto(data, (SERVER_HOST, SERVER_PORT))
            # Send end of file signal
            client_socket.sendto(END_MESSAGE, (SERVER_HOST, SERVER_PORT))
        print("File sent successfully")

if __name__ == "__main__":
    send_file("../small_file.txt")
