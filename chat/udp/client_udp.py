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
            if (message.decode().startswith("FILE_RECEIVED")):
                receive_file(message.decode())
            else:
                print(message.decode())
        except Exception as e:
            print(f"An error occurred: {e}")
            break


t = threading.Thread(target=receive_messages)
t.start()

client.sendto(f"SIGNUP_TAG: {name}".encode(), ("localhost", 9999))

def receive_file(msg):
    sender = msg.split(" ")[1]
    file_name = "fileReceived_from_" + sender + ".txt"
    data = msg.split(sender + " ")[1]
    with open(file_name, 'wb') as f:
        f.write(bytearray(data.strip(), "utf-8"))
    print("File received from %s, saved in %s" % (sender, file_name))


def send_file(to):
    with open("./fileToSend.txt", 'rb') as f:
        data = f.read(1024)
        msg = bytearray("FILE_SENT " + to + " ",'utf-8')
        client.sendto(msg + data, ("localhost", 9999))


while True:
    message = input()
    if message == "!q":
        print("Exiting chat...")
        client.close()
        break
    elif message.startswith("SENDFILE"):
        user = message.split("@")[1].strip()
        send_file(user)
    else:
        client.sendto(f"{message}".encode(), ("localhost", 9999))
