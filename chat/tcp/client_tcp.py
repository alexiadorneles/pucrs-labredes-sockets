from socket import*
from threading import Thread
import re

porta = 12001
host = 'localhost'
BUFFER_SIZE=1024


def custom_print(string, sucesso=True):
    if sucesso:
        print('\x1b[%sm%s\x1b[0m' % ("32", string))
    else:
        print('\x1b[%sm%s\x1b[0m' % ("31", string))


def receber_resposta_servidor(cliente_soc, break_loop=False):
    while True:
        msg = cliente_soc.recv(BUFFER_SIZE).decode("utf-8")
        if msg.startswith("FILE_RECEIVED"):
            print('received the file received message!')
            receber_arquivo(msg, cliente_soc)
        else:
            custom_print(msg)
            if break_loop:
                return msg


def converter_e_enviar(cliente_soc, conteudo):
    cliente_soc.send(bytearray(conteudo, 'utf-8'))
    
def receber_arquivo(msg, cliente_soc):
    sender = msg.split(" ")[1]
    file_name = "fileReceived_from_" + sender + ".txt"
    print('waiting forward to finish...')
    data = cliente_soc.recv(BUFFER_SIZE)
    print('data received, saving in txt...')
    with open(file_name, 'wb') as f:
        f.write(data)
    custom_print("Arquivo recebido de %s, salvo em %s" % (sender, file_name))


def enviar_arquivo(cliente_soc, usuario_alvo):
    with open("./fileToSend.txt", 'rb') as f:
        data = f.read(BUFFER_SIZE)
        msg = "FILE_SENT " + usuario_alvo + " "
        converter_e_enviar(cliente_soc, msg)
        print('sending file')
        cliente_soc.sendall(data)
        print('file sent')


def printar_comandos():
    custom_print("--------------------------------------------------------------------\n")
    custom_print(
        "Lista de comandos: \n-QUIT = sair do chat\n-SEND mensagem TO usuario = "
        "Para enviar uma mensagem, substituindo os campos corretamente."
        "\n-SENDFILE usuario = Para enviar arquivo para o usuário"
    )
    custom_print("--------------------------------------------------------------------\n")

def extrair_conteudo(string_input):
    return re.match(r"SEND(.*)TO", string_input).group(1).strip()

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
                elif comando == 'SEND':
                    conteudo_criptografado = extrair_conteudo(string_input)
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