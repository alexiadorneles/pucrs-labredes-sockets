# -*- coding: UTF-8 -*-
from socket import*
from threading import Thread
import hashlib
import codecs
import sys
import re

# Para codificação no terminal do windows
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

porta = 12001
host = 'localhost'


def custom_print(string, sucesso=True):
    if sucesso:
        print('\x1b[%sm%s\x1b[0m' % ("32", string))
    else:
        print('\x1b[%sm%s\x1b[0m' % ("31", string))


def receber_resposta_servidor(cliente_soc, break_loop=False):
    while True:
        msg = cliente_soc.recv(1024).decode("utf-8")
        if msg.startswith("FILE_RECEIVED"):
            receber_arquivo(msg)
        else:
            custom_print(msg)
            if break_loop:
                return msg


def converter_e_enviar(cliente_soc, conteudo):
    cliente_soc.send(bytearray(gerar_hash(conteudo), 'utf-8'))
    
def receber_arquivo(msg):
    sender = msg.split(" ")[1]
    file_name = "fileReceived_from_" + sender + ".txt"
    data = msg.split(sender + " ")[1]
    with open(file_name, 'wb') as f:
        f.write(bytearray(data.strip(), "utf-8"))
    custom_print("Arquivo recebido de %s, salvo em %s" % (sender, file_name))


def enviar_arquivo(cliente_soc, usuario_alvo):
    with open("./fileToSend.txt", 'rb') as f:
        data = f.read(1024)
        msg = bytearray(gerar_hash("FILE_SENT " + usuario_alvo + " "),'utf-8')
        cliente_soc.sendall(msg + data)


def printar_comandos():
    custom_print("--------------------------------------------------------------------\n")
    custom_print(
        "Lista de comandos: \n-QUIT = sair do chat\n-SEND mensagem TO usuario = "
        "Para enviar uma mensagem, substituindo os campos corretamente."
        "\n-SENDFILE usuario = Para enviar arquivo para o usuário"
    )
    custom_print("--------------------------------------------------------------------\n")


def gerar_hash(msg_param):
    return msg_param


def criptografar_conteudo(string_input, is_default=False):
    conteudo_mensagem = re.match(r"SEND(.*)", string_input).group(1).strip() \
        if is_default \
        else re.match(r"SEND(.*)TO", string_input).group(1).strip()
    return conteudo_mensagem


if __name__ == '__main__':
    try:
        clienteSoc = socket(AF_INET, SOCK_STREAM)
        clienteSoc.connect((host, porta))

        custom_print("---------------------------\n")
        custom_print("Bem vindo ao Terminal Chat!\n")
        custom_print("---------------------------\n")

        receber_resposta_servidor(clienteSoc, True)

        while True:
            nick = input('Informe o seu nome de usuario: \n')
            converter_e_enviar(clienteSoc, nick)
            msg = receber_resposta_servidor(clienteSoc, True)
            if "com sucesso" in msg: break

        t = Thread(target=receber_resposta_servidor, args=(clienteSoc,), daemon=True)
        t.start()

        printar_comandos()
        while True:
            string_input = input('')
            if string_input is not '':
                comando = string_input.split()[0]
                if comando == 'QUIT':
                    custom_print("Obrigado por utilizar o Terminal Chat!\nVolte Sempre ;)")
                    converter_e_enviar(clienteSoc, "SAIR")
                    clienteSoc.close()
                    exit(1)
                    break
                elif comando == 'SEND':
                    if "TO" not in string_input:
                        conteudo_criptografado = criptografar_conteudo(string_input, True)
                        converter_e_enviar(clienteSoc, "SEND %s" % conteudo_criptografado)
                    else:
                        conteudo_criptografado = criptografar_conteudo(string_input)
                        usuarioAlvo = string_input.split("TO")[1].strip()
                        converter_e_enviar(clienteSoc, "SEND %s TO %s" % (conteudo_criptografado, usuarioAlvo))
                elif comando == 'SENDFILE':
                    usuarioAlvo = string_input.split(" ")[1].strip()
                    enviar_arquivo(clienteSoc, usuarioAlvo)
                else:
                    custom_print('Comando inválido.\nDigite HELP para ver a lista de comandos novamente\n ')

    except timeout:
        custom_print("Tempo exedido!", False)
    except error:
        custom_print("Erro no Cliente: %s" % host, False)