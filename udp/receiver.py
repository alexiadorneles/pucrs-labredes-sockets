import socket

# Server configuration
HOST = '127.0.0.1'  # Loopback address
PORT = 12345        # Port to listen on
BUFFER_SIZE = 1024  # Size of the buffer for receiving data
END_MESSAGE = b"END_TRANSFER"  # Message to indicate end of file transfer

def receive_file(filename):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))
        print(f"Server listening on {HOST}:{PORT}")
        
        # Receive data and write to the file
        with open(filename, 'wb') as f:
            while True:
                data, addr = server_socket.recvfrom(BUFFER_SIZE)
                if data == END_MESSAGE:
                    break
                f.write(data)
            print("File received successfully")

if __name__ == "__main__":
    receive_file("received_file.txt")



import socket

# # Server configuration
# HOST = '127.0.0.1'  # Loopback address
# PORT = 12345        # Port to listen on
# BUFFER_SIZE = 1024  # Size of the buffer for receiving data

# def receive_file(filename):
#     # Create a UDP socket
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
#         # Bind the socket to the address and port
#         server_socket.bind((HOST, PORT))
#         print(f"Server listening on {HOST}:{PORT}")
        
#         # Receiving file
#         with open(filename, 'wb') as f:
#             while True:
#                 data, addr = server_socket.recvfrom(BUFFER_SIZE)
#                 if data == b'END':
#                     break
#                 f.write(data)
#         print("File received successfully")

# if __name__ == "__main__":
#     receive_file("received_file.txt")
