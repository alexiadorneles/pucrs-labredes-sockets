import socket
import threading
import queue


messages = queue.Queue()

clients = []


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))

def receive_messages():
    """Thread function to receive messages from clients."""
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except Exception as e:
            print(f"Error receiving messages: {e}")
            break

def broadcast_messages():
    """Thread function to broadcast messages to all connected clients."""
    while True:
        while not messages.empty():
            message, addr = messages.get()
            decoded_message = message.decode()
            print(decoded_message)
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if decoded_message.startswith("SIGNUP_TAG:"):
                        name = decoded_message.split(':')[1].strip()
                        server.sendto(f"{name} joined!".encode(), client)
                    else:
                        server.sendto(message, client)
                except Exception as e:
                    print(f"Error sending message to {client}: {e}")
                    clients.remove(client)

t1 = threading.Thread(target=receive_messages)
t2 = threading.Thread(target=broadcast_messages)

t1.start()
t2.start()
