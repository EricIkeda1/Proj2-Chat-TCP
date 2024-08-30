import socket
import threading

# Escolha da cifra de criptografia pelo usuário
print("Escolha a cifra de criptografia: ")
print("1. Cifra de César")
print("2. Substituição Monoalfabética")
print("3. Cifra de Playfair")
print("4. Cifra de Vigenère")
escolha = input("Digite o número da cifra desejada: ")

# Solicitação da chave de criptografia
chave = input("Digite a chave para a cifra escolhida: ")

# Função que implementa a Cifra de César
def cifra_de_cesar(mensagem, chave, criptografar=True):
    resultado = ''
    deslocamento = chave if criptografar else -chave
    for caractere in mensagem:
        if caractere.isalpha():
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
        else:
            resultado += caractere
    return resultado

# Função que implementa a Substituição Monoalfabética
def cifra_monoalfabetica(mensagem, chave, criptografar=True):
    alfabeto_original = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alfabeto_substituido = 'QWERTYUIOPLKJHGFDSAZXCVBNM'
    
    chave = chave.upper()
    
    if criptografar:
        mapa_chave = {alfabeto_original[i]: alfabeto_substituido[i] for i in range(26)}
    else:
        mapa_chave = {alfabeto_substituido[i]: alfabeto_original[i] for i in range(26)}

    resultado = ''
    for caractere in mensagem.upper():
        resultado += mapa_chave.get(caractere, caractere)
    return resultado

# Função que implementa a Cifra de Playfair
def cifra_de_playfair(mensagem, chave, criptografar=True):
    def formatar_mensagem(mensagem):
        mensagem = mensagem.replace(' ', '').upper()
        formatada = ''
        i = 0
        while i < len(mensagem):
            if i == len(mensagem) - 1:
                formatada += mensagem[i] + 'X'
                i += 1
            elif mensagem[i] == mensagem[i + 1]:
                formatada += mensagem[i] + 'X'
                i += 1
            else:
                formatada += mensagem[i] + mensagem[i + 1]
                i += 2
        return formatada

    def criar_matriz(chave):
        alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        chave = chave.upper().replace('J', 'I')  # Substituir J por I
        chave = ''.join(sorted(set(chave), key=chave.index))  # Remover duplicatas mantendo a ordem
        matriz = [chave[i] for i in range(len(chave))]  # Adicionar caracteres da chave
        matriz += [c for c in alfabeto if c not in matriz]  # Adicionar caracteres do alfabeto que não estão na chave
        return [matriz[i:i + 5] for i in range(0, 25, 5)]

    def encontrar_posicao(matriz, caractere):
        for i, linha in enumerate(matriz):
            for j, valor in enumerate(linha):
                if valor == caractere:
                    return i, j
        # Retorna uma posição padrão para caracteres não encontrados
        return None, None

    mensagem = formatar_mensagem(mensagem)
    matriz = criar_matriz(chave)
    resultado = ''
    
    for i in range(0, len(mensagem), 2):
        pos1 = encontrar_posicao(matriz, mensagem[i])
        pos2 = encontrar_posicao(matriz, mensagem[i + 1])

        if pos1 == (None, None) or pos2 == (None, None):
            # Ignorar caracteres não encontrados na matriz
            resultado += mensagem[i] + mensagem[i + 1]
            continue
        
        linha1, coluna1 = pos1
        linha2, coluna2 = pos2

        if linha1 == linha2:
            coluna1 = (coluna1 + 1) % 5 if criptografar else (coluna1 - 1) % 5
            coluna2 = (coluna2 + 1) % 5 if criptografar else (coluna2 - 1) % 5
        elif coluna1 == coluna2:
            linha1 = (linha1 + 1) % 5 if criptografar else (linha1 - 1) % 5
            linha2 = (linha2 + 1) % 5 if criptografar else (linha2 - 1) % 5
        else:
            coluna1, coluna2 = coluna2, coluna1

        resultado += matriz[linha1][coluna1] + matriz[linha2][coluna2]
    
    return resultado

# Função que implementa a Cifra de Vigenère
def cifra_de_vigenere(mensagem, chave, criptografar=True):
    resultado = ''
    chave = chave.lower()
    indice_chave = 0
    
    for caractere in mensagem:
        if caractere.isalpha():
            deslocamento = ord(chave[indice_chave]) - ord('a')
            deslocamento = deslocamento if criptografar else -deslocamento
            base = ord('A') if caractere.isupper() else ord('a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
            indice_chave = (indice_chave + 1) % len(chave)
        else:
            resultado += caractere
    
    return resultado


# Função que aplica a cifra escolhida na mensagem
def criptografar_mensagem(mensagem):
    if escolha == '1':
        return cifra_de_cesar(mensagem, int(chave))
    elif escolha == '2':
        return cifra_monoalfabetica(mensagem, chave)
    elif escolha == '3':
        return cifra_de_playfair(mensagem, chave)
    elif escolha == '4':
        return cifra_de_vigenere(mensagem, chave)
    else:
        return mensagem

# Função que recebe mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            print(mensagem)
        except:
            print("Ocorreu um erro!")
            cliente.close()
            break

# Função que envia mensagens para o servidor
def enviar_mensagens():
    while True:
        mensagem = '{}: {}'.format(apelido, input(''))
        mensagem_criptografada = criptografar_mensagem(mensagem)
        cliente.send(mensagem_criptografada.encode('ascii'))

# Conectando ao servidor
apelido = input("Escolha seu apelido: ")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

# Iniciando threads para envio e recebimento de mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar_mensagens)
thread_enviar.start()
