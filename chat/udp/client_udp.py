import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))
name = input("Nickname: ")

def printar_comandos():
    print("--------------------------------------------------------------------\n")
    print(
        "Lista de comandos: \n-QUIT = sair do chat\n-SEND mensagem TO usuario = "
        "Para enviar uma mensagem, substituindo os campos corretamente."
        "\n-SENDFILE usuario = Para enviar arquivo para o usuário"
    )
    print("--------------------------------------------------------------------\n")

def receber_mensagens():
    while True:
        try:
            mensagem, _ = client.recvfrom(2048)
            if (mensagem.decode().startswith("FILE_RECEIVED")):
                receber_arquivo(mensagem.decode())
            else:
                print(mensagem.decode())
        except Exception as e:
            print(f"Erro: {e}")
            break


t = threading.Thread(target=receber_mensagens)
t.start()

client.sendto(f"REGISTER: {name}".encode(), ("localhost", 9999))

def receber_arquivo(msg):
    usuario = msg.split(" ")[1]
    nome_arquivo = "fileReceived_from_" + usuario + ".txt"
    conteudo = msg.split(usuario + " ")[1]
    with open(nome_arquivo, 'wb') as f:
        f.write(bytearray(conteudo.strip(), "utf-8"))
    print("Arquivo recebido de %s, salvo em %s" % (usuario, nome_arquivo))


def enviar_arquivo(para):
    with open("./fileToSend.txt", 'rb') as f:
        data = f.read(2048)
        msg = bytearray("FILE_SENT " + para + " ",'utf-8')
        client.sendto(msg + data, ("localhost", 9999))

printar_comandos();

while True:
    texto = input()
    if texto == "!q":
        print("Exiting chat...")
        client.close()
        break
    elif texto.startswith("SENDFILE"):
        usuario = texto.split(" ")[1].strip()
        enviar_arquivo(usuario)
    else:
        client.sendto(f"{texto}".encode(), ("localhost", 9999))
