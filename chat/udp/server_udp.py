import socket
import threading
import queue
import re

messages = queue.Queue()

nick_end = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))

def receber_mensagem():
    while True:
        try:
            message, addr = server.recvfrom(2048)
            messages.put((message, addr))
        except Exception as e:
            print(f"Erro recebendo mensagem: {e}")
            break

def enviar_arquivo(para, conteudo, nick):
    print("Sending content: " + conteudo.decode())
    endereco = nick_end[para]
    msg = "FILE_RECEIVED %s " % (nick)
    server.sendto(msg.encode() + conteudo, endereco)

def procurar_nickname(endereco):
    for nickname, end in nick_end.items():
        if end == endereco:
            return nickname
    return None 

def enviar_mensagem():
    while True:
        while not messages.empty():
            message, end = messages.get()
            mensagem = message.decode()
            if mensagem.startswith("REGISTER:"):
                nome = mensagem.split(':')[1].strip()
                nick_end[nome] = end 
                server.sendto(f"{nome} registrado!".encode(), end) 
            elif mensagem.startswith("FILE_SENT"):
                    usuario = procurar_nickname(end)
                    usuario_alvo = mensagem.split(" ")[1]
                    conteudo_arquivo = mensagem.split(usuario_alvo + " ")[1]
                    enviar_arquivo(usuario_alvo, conteudo_arquivo.encode(), usuario)
            else:
                usuario = procurar_nickname(end)
                if mensagem.startswith("SEND"):
                    usuario_alvo = mensagem.split("TO")[1].strip()
                    conteudo_mensagem = re.match(r"SEND(.*)TO", mensagem).group(1).strip()
                    mensagem = "Mensagem de %s: %s" % (usuario, conteudo_mensagem)
                    for esse_nome, esse_endereco in nick_end.items():
                        if esse_nome == usuario_alvo: 
                            server.sendto(f"{mensagem}".encode(), esse_endereco)


t1 = threading.Thread(target=receber_mensagem)
t2 = threading.Thread(target=enviar_mensagem)

t1.start()
t2.start()
