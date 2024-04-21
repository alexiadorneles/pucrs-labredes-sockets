# -*- coding: UTF-8 -*-
from socket import *
from threading import Thread
import re
import hashlib

porta = 12001
ip = 'localhost'  # localhost.

nick_con = {}

def receber_mensagem_cliente(con):
    return con.recv(1024).decode("utf-8")


def get_usuarios_conectados(prefixo):
    if len(nick_con) > 1:
        return prefixo.format("\n - " + "\n - ".join(list(nick_con.keys())) + "\n")
    else:
        return prefixo.format("".join(list(nick_con.keys())) + "\n")


def enviar_para_cliente(con, conteudo):
    con.send(bytearray(conteudo, "utf-8"))


def inicia_servidor(servidor_soc):
    servidor_soc.bind((ip, porta))
    servidor_soc.listen(60)

    print("Servidor ativo!\nAguardando conexões.")

    while True:
        conexao, end_remoto = servidor_soc.accept()
        enviar_para_cliente(conexao, get_usuarios_conectados("Usuários conectados: {}"))
        t = Thread(target=trata_nova_conexao, args=(conexao, end_remoto), daemon=True)
        t.start()

def enviar_para_usuario(usuario_alvo, msg_remota, nick, con):
    try:
        con_usuario_alvo = nick_con[usuario_alvo]
        conteudo_mensagem = re.match(r"SEND(.*)TO", msg_remota).group(1).strip()
        conteudo_mensagem_descriptografado = conteudo_mensagem
        mensagem = "Mensagem de %s: %s" % (nick, conteudo_mensagem_descriptografado)
        enviar_para_cliente(con_usuario_alvo, mensagem)
    except error:
        enviar_para_cliente(con, "O usuário %s não está online no momento" % usuario_alvo)

def enviar_arquivo_para_usuario(usuario_alvo, conteudo_mensagem, nick, con):
    print("Sending content: " + conteudo_mensagem)
    try:
        con_usuario_alvo = nick_con[usuario_alvo]
        mensagem = "FILE_RECEIVED %s " % (nick)
        con_usuario_alvo.sendall(bytearray(mensagem + conteudo_mensagem, "utf-8"))
    except error:
        enviar_para_cliente(con, "O usuário %s não está online no momento" % usuario_alvo)


def trata_nova_conexao(con, end_remoto):
    msg = receber_mensagem_cliente(con)
    nick = msg.strip().split(" ")[0]

    if nick in list(nick_con.keys()):
        resposta = nick + " ja esta em uso." + get_usuarios_conectados("Nicks em uso: {}")
        enviar_para_cliente(con, resposta)
        trata_nova_conexao(con, end_remoto)
    else:
        nick_con[nick] = con
        enviar_para_cliente(con, nick + " conectado com sucesso.\n")

        while True:
            msg_remota = receber_mensagem_cliente(con)

            if msg_remota == '' or msg_remota == 'SAIR':
                print("A conexao com ", nick, " foi fechada.\n")
                con.close()
                del nick_con[nick]
                break
            
            elif msg_remota.startswith("FILE_SENT"):
                usuario_alvo = msg_remota.split(" ")[1]
                file_content = msg_remota.split(usuario_alvo + " ")[1]
                if usuario_alvo not in list(nick_con.keys()):
                    enviar_para_cliente(con, "O usuário %s não está conectado" % usuario_alvo)
                else:
                    enviar_arquivo_para_usuario(usuario_alvo, file_content, nick, con)

            elif msg_remota.split()[0] == 'SEND':
                if "TO" not in msg_remota or len(msg_remota.split("TO")) < 2:
                    enviar_para_cliente(con,
                                        "Destinatário não especificado\nComando para mensagens: SEND mensagem TO "
                                        "usuario")
                elif "TO" in msg_remota and len(msg_remota.split("TO")) >= 1:
                    usuario_alvo = msg_remota.split("TO")[1].strip()
                    if usuario_alvo not in list(nick_con.keys()):
                        enviar_para_cliente(con, "O usuário %s não está conectado" % usuario_alvo)
                    else:
                        enviar_para_usuario(usuario_alvo, msg_remota, nick, con)


# Função principal.
if __name__ == '__main__':
    try:
        servidorSoc = socket(AF_INET, SOCK_STREAM)  # Socket TCP
        t2 = Thread(target=inicia_servidor, args=(servidorSoc,), daemon=True)
        t2.start()

        while True:
            aux = input('')
            if aux == 'FIM':
                print("Tchau!\n")
                servidorSoc.close()  # nunca!
                exit(1)

    except timeout:
        print("Tempo exedido!")
    except error:
        print("Erro no Servidor:", error)
        exit(1)