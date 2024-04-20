import socket
import threading
import queue


messages = queue.Queue()

nick_addr = {}


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

def find_nickname(address):
    for nickname, addr in nick_addr.items():
        if addr == address:
            return nickname
    return None  # Address not found

def broadcast_messages():
    """Thread function to broadcast messages to all connected clients."""
    while True:
        while not messages.empty():
            message, addr = messages.get()
            decoded_message = message.decode()
            print(decoded_message)
            if decoded_message.startswith("SIGNUP_TAG:"):
                name = decoded_message.split(':')[1].strip()
                nick_addr[name] = addr  # Add client's nickname and address
                server.sendto(f"{name} joined!".encode(), addr)  # Send join message to new client
            else:
                sender_name = find_nickname(addr)
                print('decoded message', decoded_message)
                if decoded_message.startswith("@"):
                    print('@')
                    recipient, message_text = decoded_message.split(" ", 1)
                    recipient = recipient[1:]  # Remove '@' from recipient's nickname
                    for c_name, c_addr in nick_addr.items():
                        if c_name == recipient:  # Send message to recipient and sender
                            server.sendto(f"{sender_name}: {message_text}".encode(), c_addr)


t1 = threading.Thread(target=receive_messages)
t2 = threading.Thread(target=broadcast_messages)

t1.start()
t2.start()
