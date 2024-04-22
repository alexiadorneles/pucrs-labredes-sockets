# -*- coding: UTF-8 -*-
from socket import *
from threading import Thread
import re
import hashlib

port = 12001
ip = 'localhost'  # localhost.

nick_con = {}

def receive_message_cleint(con):
    return con.recv(1024).decode("utf-8")


def get_conected_users(prefix):
    if len(nick_con) > 1:
        return prefix.format("\n - " + "\n - ".join(list(nick_con.keys())) + "\n")
    else:
        return prefix.format("".join(list(nick_con.keys())) + "\n")


def send_to_client(con, content):
    con.send(bytearray(content, "utf-8"))


def start_server(server_soc):
    server_soc.bind((ip, port))
    server_soc.listen(60)

    print("Server active!\Waiting conections.")

    while True:
        conection, end_remote = server_soc.accept()
        send_to_client(conection, get_conected_users("Users conented: {}"))
        t = Thread(target=treat_new_conection, args=(conection, end_remote), daemon=True)
        t.start()


def analyse_hash(msg):
    return True

def send_to_user(target_user, msg_remote, nick, con):
    try:
        con_target_user = nick_con[target_user]
        message_content = re.match(r"SEND(.*)TO", msg_remote).group(1).strip()
        message_content_decrypted = message_content
        msg = "Message from %s: %s" % (nick, message_content_decrypted)
        send_to_client(con_target_user, msg)
    except error:
        send_to_client(con, "User %s is not online at the moment" % target_user)

def send_file_to_user(target_user, message_coontent, nick, con):
    print("Sending content: " + message_coontent)
    try:
        con_target_user = nick_con[target_user]
        msg = "FILE_RECEIVED %s " % (nick)
        con_target_user.sendall(bytearray(msg + message_coontent, "utf-8"))
    except error:
        send_to_client(con, "User %s is not online at the moment" % target_user)


def treat_new_conection(con, end_remote):
    msg = receive_message_cleint(con)
    nick = msg.strip().split(" ")[0]

    if nick in list(nick_con.keys()):
        response = nick + " already in use." + get_conected_users("Nicks in use: {}")
        send_to_client(con, response)
        treat_new_conection(con, end_remote)
    else:
        nick_con[nick] = con
        send_to_client(con, nick + " connected with sucess.\n")

        while True:
            msg_remote = receive_message_cleint(con)

            if analyse_hash(msg_remote):
                if msg_remote == '' or msg_remote == 'SAIR':
                    print("Conection with ", nick, " was closed.\n")
                    con.close()
                    del nick_con[nick]
                    break
                
                elif msg_remote.startswith("FILE_SENT"):
                    target_user = msg_remote.split(" ")[1]
                    file_content = msg_remote.split(target_user + " ")[1]
                    if target_user not in list(nick_con.keys()):
                        send_to_client(con, "User %s is not connected" % target_user)
                    else:
                        send_file_to_user(target_user, file_content, nick, con)

                elif msg_remote.split()[0] == 'SEND':
                    if "TO" not in msg_remote or len(msg_remote.split("TO")) < 2:
                        send_to_client(con,
                                            "Receiver not specified\nComando para mensagens: @user  "
                                            "message")
                    elif "TO" in msg_remote and len(msg_remote.split("TO")) >= 1:
                        target_user = msg_remote.split("TO")[1].strip()
                        if target_user not in list(nick_con.keys()):
                            send_to_client(con, "User %s not connected" % target_user)
                        else:
                            send_to_user(target_user, msg_remote, nick, con)
            else:
                send_to_client(con, "Integrity violated")


# MAIN.
if __name__ == '__main__':
    try:
        serverSoc = socket(AF_INET, SOCK_STREAM)  # Socket TCP
        t2 = Thread(target=start_server, args=(serverSoc,), daemon=True)
        t2.start()

        while True:
            aux = input('')
            if aux == 'FIM':
                print("Bye!\n")
                serverSoc.close()  # nunca!
                exit(1)

    except timeout:
        print("Timeout!")
    except error:
        print("Error on server:", error)
        exit(1)