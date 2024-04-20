import socket
import threading
import random


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


client.bind(("localhost", random.randint(8000, 9000)))


name = input("Nickname: ")

def receive_messages():
    """Function to receive messages from the server."""
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except Exception as e:
            print(f"An error occurred: {e}")
            break


t = threading.Thread(target=receive_messages)
t.start()


client.sendto(f"SIGNUP_TAG: {name}".encode(), ("localhost", 9999))

while True:
    message = input()
    if message == "!q":
        print("Exiting chat...")
        client.close()
        break
    else:
        client.sendto(f"{message}".encode(), ("localhost", 9999))
