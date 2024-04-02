# coding: utf-8
import operator

alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
            'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

caracteres_especiais = ['?', ',', ':', ' ', '.']

# chave = "WONDERWOMAN"
chave = "PRINCE"

LIMITE_SUPERIOR = 126
LIMITE_INFERIOR = 32


def is_posicao_de_uma_letra(pos):
    return (65 <= pos <= 90) or (97 <= pos <= 122)


def definir_lista_circular(lista):
    while True:
        for nodo in lista:
            yield nodo


def resolve_posicao_decrypt(pos, ascii, letra_chave):
    if pos < LIMITE_INFERIOR:
        return ascii + LIMITE_SUPERIOR - alfabeto.index(letra_chave) - LIMITE_INFERIOR
    return pos


def resolve_posicao_encrypt(pos):
    if pos > LIMITE_SUPERIOR:
        pos -= LIMITE_SUPERIOR
    if pos < LIMITE_INFERIOR:
        pos += LIMITE_INFERIOR
    return pos


def resolve_criptografia(conteudo, decrypt=False):
    chave_circular = definir_lista_circular(chave)
    operador = operator.sub if decrypt else operator.add
    texto = ""
    for caractere in conteudo:
        letra_chave = next(chave_circular)
        ascii = ord(caractere)

        if not decrypt and (caractere not in caracteres_especiais and is_posicao_de_uma_letra(ascii)) \
                or decrypt and caractere not in caracteres_especiais:
            pos = operador(ascii, alfabeto.index(letra_chave))
            pos = resolve_posicao_decrypt(pos, ascii, letra_chave) if decrypt else resolve_posicao_encrypt(pos)
            nova_letra = chr(pos)
        else:
            nova_letra = caractere
        texto += nova_letra
    return texto


class Cifra:

    @staticmethod
    def criptografar_conteudo(conteudo):
        return resolve_criptografia(conteudo.strip())

    @staticmethod
    def descriptografar_conteudo(conteudo):
        return resolve_criptografia(conteudo.strip(), True)