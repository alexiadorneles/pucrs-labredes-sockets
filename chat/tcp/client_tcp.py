# -*- coding: UTF-8 -*-
from socket import*
from threading import Thread
import hashlib
import codecs
import sys
import re

# Para codificação no terminal do windows
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

port = 12001
host = 'localhost'


def custom_print(string, sucess=True):
    if sucess:
        print('\x1b[%sm%s\x1b[0m' % ("32", string))
    else:
        print('\x1b[%sm%s\x1b[0m' % ("31", string))


def receive_server_response(client_soc, break_loop=False):
    while True:
        msg = client_soc.recv(1024).decode("utf-8")
        if msg.startswith("FILE_RECEIVED"):
            receive_file(msg)
        else:
            custom_print(msg)
            if break_loop:
                return msg


def convert_and_send(client_soc, content):
    client_soc.send(bytearray(make_hash(content), 'utf-8'))
    
def receive_file(msg):
    sender = msg.split(" ")[1]
    file_name = "fileReceived_from_" + sender + ".txt"
    data = msg.split(sender + " ")[1]
    with open(file_name, 'wb') as f:
        f.write(bytearray(data.strip(), "utf-8"))
    custom_print("File received from %s, saved in %s" % (sender, file_name))


def send_file(client_soc, target_user):
    with open("./fileToSend.txt", 'rb') as f:
        data = f.read(1024)
        msg = bytearray(make_hash("FILE_SENT " + target_user + " "),'utf-8')
        client_soc.sendall(msg + data)


def print_comands():
    custom_print("--------------------------------------------------------------------\n")
    custom_print(
        "List of comands: \n-!q = leave chat\n-@user message = "
        "To send message, replacing with the user and the message to be sent."
        "\n-SENDFILE @user = To send file to the user"
    )
    custom_print("--------------------------------------------------------------------\n")


def make_hash(msg_param):
    return msg_param


def encrypt_content(string_input, is_default=False):
    message_content = re.match(r"SEND(.*)", string_input).group(1).strip() \
        if is_default \
        else re.match(r"SEND(.*)TO", string_input).group(1).strip()
    return message_content


if __name__ == '__main__':
    try:
        clientSoc = socket(AF_INET, SOCK_STREAM)
        clientSoc.connect((host, port))

        custom_print("---------------------------\n")
        custom_print("Welcome to Terminal Chat!\n")
        custom_print("---------------------------\n")

        receive_server_response(clientSoc, True)

        while True:
            nick = input('Nickname: \n')
            convert_and_send(clientSoc, nick)
            msg = receive_server_response(clientSoc, True)
            if "with sucess" in msg: break

        t = Thread(target=receive_server_response, args=(clientSoc,), daemon=True)
        t.start()

        print_comands()
        while True:
            string_input = input('')
            if string_input is not '':
                comand = string_input.split()[0]
                if comand == 'QUIT':
                    custom_print("Thanks for using Terminal Chat!\nCome Back soon ;)")
                    convert_and_send(clientSoc, "SAIR")
                    clientSoc.close()
                    exit(1)
                    break
                elif comand == 'SEND':
                    if "TO" not in string_input:
                        encrypted_content = encrypt_content(string_input, True)
                        convert_and_send(clientSoc, "SEND %s" % encrypted_content)
                    else:
                        encrypted_content = encrypt_content(string_input)
                        targetUser = string_input.split("TO")[1].strip()
                        convert_and_send(clientSoc, "SEND %s TO %s" % (encrypted_content, targetUser))
                elif comand == 'SENDFILE':
                    targetUser = string_input.split(" ")[1].strip()
                    send_file(clientSoc, targetUser)
                else:
                    custom_print('Invalid comand.\n ')

    except timeout:
        custom_print("Timeout!", False)
    except error:
        custom_print("Error in Client: %s" % host, False)