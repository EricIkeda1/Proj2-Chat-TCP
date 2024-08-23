import socket  # Importa o módulo socket para comunicação de rede
import threading  # Importa o módulo threading para execução de threads

# Funções de criptografia

def cifra_de_cesar(mensagem, chave, criptografar=True):
    """
    Função para criptografar ou descriptografar uma mensagem usando a Cifra de César.
    """
    resultado = ''  # Inicializa a variável para armazenar o resultado
    deslocamento = chave if criptografar else -chave  # Define o deslocamento baseado na criptografia ou descriptografia
    for caractere in mensagem:
        if caractere.isalpha():  # Verifica se o caractere é uma letra
            base = ord('A') if caractere.isupper() else ord('a')  # Define a base ASCII ('A' ou 'a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)  # Aplica a cifra e adiciona ao resultado
        else:
            resultado += caractere  # Adiciona caracteres não alfabéticos sem alteração
    return resultado

def cifra_monoalfabetica(mensagem, chave, criptografar=True):
    """
    Função para criptografar ou descriptografar uma mensagem usando a Cifra Monoalfabética.
    """
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'  # Define o alfabeto
    resultado = ''  # Inicializa a variável para armazenar o resultado
    # Cria o mapa de substituição baseado na chave
    mapa_chave = {alfabeto[i]: chave[i] for i in range(26)} if criptografar else {chave[i]: alfabeto[i] for i in range(26)}
    
    for caractere in mensagem.lower():  # Converte a mensagem para minúsculas e processa caractere por caractere
        resultado += mapa_chave.get(caractere, caractere)  # Substitui o caractere conforme o mapa de chave
    return resultado

def cifra_de_playfair(mensagem, chave, criptografar=True):
    """
    Função para criptografar ou descriptografar uma mensagem usando a Cifra de Playfair.
    """
    def formatar_mensagem(mensagem):
        """
        Formata a mensagem para a cifra de Playfair (remove espaços e adiciona 'X' onde necessário).
        """
        mensagem = mensagem.replace(' ', '').upper()  # Remove espaços e converte para maiúsculas
        formatada = ''  # Inicializa a mensagem formatada
        i = 0
        while i < len(mensagem):
            if i == len(mensagem) - 1:  # Se for o último caractere, adiciona 'X'
                formatada += mensagem[i] + 'X'
                i += 1
            elif mensagem[i] == mensagem[i + 1]:  # Se dois caracteres iguais, adiciona 'X'
                formatada += mensagem[i] + 'X'
                i += 1
            else:
                formatada += mensagem[i] + mensagem[i + 1]  # Adiciona dois caracteres
                i += 2
        return formatada

    def criar_matriz(chave):
        """
        Cria a matriz para a cifra de Playfair com base na chave.
        """
        alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # Define o alfabeto sem 'J'
        matriz = []  # Inicializa a matriz
        for caractere in chave.upper():  # Adiciona caracteres da chave na matriz
            if caractere not in matriz and caractere != 'J':
                matriz.append(caractere)
        for caractere in alfabeto:  # Adiciona caracteres restantes do alfabeto na matriz
            if caractere not in matriz:
                matriz.append(caractere)
        return [matriz[i:i + 5] for i in range(0, 25, 5)]  # Cria uma matriz 5x5

    def encontrar_posicao(matriz, caractere):
        """
        Encontra a posição de um caractere na matriz.
        """
        for i, linha in enumerate(matriz):
            for j, valor in enumerate(linha):
                if valor == caractere:
                    return i, j  # Retorna a linha e coluna do caractere

    mensagem = formatar_mensagem(mensagem)  # Formata a mensagem
    matriz = criar_matriz(chave)  # Cria a matriz de Playfair
    resultado = ''  # Inicializa o resultado
    
    for i in range(0, len(mensagem), 2):  # Processa a mensagem em pares de caracteres
        linha1, coluna1 = encontrar_posicao(matriz, mensagem[i])
        linha2, coluna2 = encontrar_posicao(matriz, mensagem[i + 1])

        if linha1 == linha2:  # Caso na mesma linha
            coluna1 = (coluna1 + 1) % 5 if criptografar else (coluna1 - 1) % 5
            coluna2 = (coluna2 + 1) % 5 if criptografar else (coluna2 - 1) % 5
        elif coluna1 == coluna2:  # Caso na mesma coluna
            linha1 = (linha1 + 1) % 5 if criptografar else (linha1 - 1) % 5
            linha2 = (linha2 + 1) % 5 if criptografar else (linha2 - 1) % 5
        else:  # Caso diferente linha e coluna
            coluna1, coluna2 = coluna2, coluna1

        resultado += matriz[linha1][coluna1] + matriz[linha2][coluna2]  # Adiciona os caracteres criptografados/descriptografados
    
    return resultado

def cifra_de_vigenere(mensagem, chave, criptografar=True):
    """
    Função para criptografar ou descriptografar uma mensagem usando a Cifra de Vigenère.
    """
    resultado = ''  # Inicializa a variável para armazenar o resultado
    chave = chave.lower()  # Converte a chave para minúsculas
    indice_chave = 0  # Inicializa o índice da chave
    
    for caractere in mensagem:  # Processa a mensagem caractere por caractere
        if caractere.isalpha():  # Verifica se o caractere é uma letra
            deslocamento = ord(chave[indice_chave]) - ord('a')  # Calcula o deslocamento baseado na chave
            deslocamento = deslocamento if criptografar else -deslocamento
            base = ord('A') if caractere.isupper() else ord('a')  # Define a base ASCII ('A' ou 'a')
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)  # Aplica a cifra e adiciona ao resultado
            indice_chave = (indice_chave + 1) % len(chave)  # Atualiza o índice da chave
        else:
            resultado += caractere  # Adiciona caracteres não alfabéticos sem alteração
    return resultado

def criptografar_mensagem(mensagem):
    """
    Função para criptografar uma mensagem com base na cifra escolhida.
    """
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

def receber_mensagens():
    """
    Função que recebe e imprime mensagens do servidor.
    """
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')  # Recebe a mensagem do servidor e decodifica
            print(mensagem)  # Exibe a mensagem recebida
        except:
            print("Ocorreu um erro!")  # Mensagem de erro caso ocorra algum problema
            cliente.close()  # Fecha a conexão do cliente
            break  # Encerra o loop

def enviar_mensagens():
    """
    Função que envia mensagens para o servidor.
    """
    while True:
        mensagem = '{}: {}'.format(apelido, input(''))  # Formata a mensagem com o apelido do usuário
        mensagem_criptografada = criptografar_mensagem(mensagem)  # Criptografa a mensagem
        cliente.send(mensagem_criptografada.encode('ascii'))  # Envia a mensagem criptografada

print("Escolha a cifra de criptografia: ")
print("1. Cifra de César")
print("2. Substituição Monoalfabética")
print("3. Cifra de Playfair")
print("4. Cifra de Vigenère")
escolha = input("Digite o número da cifra desejada: ")  # Solicita a escolha da cifra

chave = input("Digite a chave para a cifra escolhida: ")  # Solicita a chave para a cifra

ip_servidor = input("Digite o IP do servidor: ")  # Solicita o IP do servidor
porta_servidor = int(input("Digite a porta do servidor: "))  # Solicita a porta do servidor

apelido = input("Escolha seu apelido: ")  # Solicita o apelido do usuário

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
cliente.connect((ip_servidor, porta_servidor))  # Conecta ao servidor

# Criação das threads para enviar e receber mensagens
thread_receber = threading.Thread(target=receber_mensagens)
thread_enviar = threading.Thread(target=enviar_mensagens)

thread_receber.start()  # Inicia a thread para receber mensagens
thread_enviar.start()  # Inicia a thread para enviar mensagens
