import socket  # Importa o módulo socket para comunicação de rede
import threading  # Importa o módulo threading para criar threads

# Exibe opções de cifras de criptografia para o usuário
print("Escolha a cifra de criptografia: ")
print("1. Cifra de César")
print("2. Substituição Monoalfabética")
print("3. Cifra de Playfair")
print("4. Cifra de Vigenère")

# Captura a escolha da cifra de criptografia do usuário
escolha = input("Digite o número da cifra desejada: ")

# Solicita ao usuário a chave de criptografia
chave = input("Digite a chave para a cifra escolhida: ")

ip_servidor = input("Digite o IP do servidor: ")  # Solicita o IP do servidor
porta_servidor = int(input("Digite a porta do servidor: "))  # Solicita a porta do servidor

# Função que implementa a Cifra de César
def cifra_de_cesar(mensagem, chave, criptografar=True):
    resultado = ''  # Inicializa a string para armazenar o resultado
    deslocamento = chave if criptografar else -chave  # Define o deslocamento com base na criptografia ou descriptografia
    for caractere in mensagem:  # Itera sobre cada caractere da mensagem
        if caractere.isalpha():  # Verifica se o caractere é uma letra
            base = ord('A') if caractere.isupper() else ord('a')  # Define a base ASCII para maiúsculas ou minúsculas
            # Aplica a cifra e adiciona o caractere ao resultado
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
        else:
            resultado += caractere  # Adiciona caracteres não alfabéticos sem modificação
    return resultado  # Retorna a mensagem criptografada ou descriptografada

# Função que implementa a Substituição Monoalfabética
def cifra_monoalfabetica(mensagem, chave, criptografar=True):
    alfabeto_original = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Alfabeto original
    alfabeto_substituido = 'QWERTYUIOPLKJHGFDSAZXCVBNM'  # Alfabeto substituído
    
    chave = chave.upper()  # Converte a chave para maiúsculas
    
    if criptografar:
        # Cria um mapa de substituição usando o alfabeto original e substituído
        mapa_chave = {alfabeto_original[i]: alfabeto_substituido[i] for i in range(26)}
    else:
        # Cria um mapa de substituição invertido para descriptografar
        mapa_chave = {alfabeto_substituido[i]: alfabeto_original[i] for i in range(26)}

    resultado = ''  # Inicializa a string para armazenar o resultado
    for caractere in mensagem.upper():  # Converte a mensagem para maiúsculas e itera sobre cada caractere
        resultado += mapa_chave.get(caractere, caractere)  # Substitui o caractere ou mantém o original
    return resultado  # Retorna a mensagem criptografada ou descriptografada

# Função que implementa a Cifra de Playfair
def cifra_de_playfair(mensagem, chave, criptografar=True):
    # Função auxiliar para formatar a mensagem
    def formatar_mensagem(mensagem):
        mensagem = mensagem.replace(' ', '').upper()  # Remove espaços e converte para maiúsculas
        formatada = ''  # Inicializa a string formatada
        i = 0
        while i < len(mensagem):
            if i == len(mensagem) - 1:
                formatada += mensagem[i] + 'X'  # Adiciona 'X' se a mensagem tiver um número ímpar de caracteres
                i += 1
            elif mensagem[i] == mensagem[i + 1]:
                formatada += mensagem[i] + 'X'  # Adiciona 'X' se houver caracteres repetidos consecutivos
                i += 1
            else:
                formatada += mensagem[i] + mensagem[i + 1]  # Adiciona pares de caracteres
                i += 2
        return formatada  # Retorna a mensagem formatada

    # Função auxiliar para criar a matriz da cifra de Playfair
    def criar_matriz(chave):
        alfabeto = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # Alfabeto sem a letra 'J'
        chave = chave.upper().replace('J', 'I')  # Substitui 'J' por 'I'
        chave = ''.join(sorted(set(chave), key=chave.index))  # Remove duplicatas mantendo a ordem
        matriz = [chave[i] for i in range(len(chave))]  # Adiciona caracteres da chave
        matriz += [c for c in alfabeto if c not in matriz]  # Adiciona caracteres do alfabeto não presentes na chave
        return [matriz[i:i + 5] for i in range(0, 25, 5)]  # Cria uma matriz 5x5

    # Função auxiliar para encontrar a posição de um caractere na matriz
    def encontrar_posicao(matriz, caractere):
        for i, linha in enumerate(matriz):
            for j, valor in enumerate(linha):
                if valor == caractere:
                    return i, j  # Retorna a posição do caractere
        return None, None  # Retorna None se o caractere não for encontrado

    mensagem = formatar_mensagem(mensagem)  # Formata a mensagem
    matriz = criar_matriz(chave)  # Cria a matriz da cifra
    resultado = ''  # Inicializa a string para armazenar o resultado
    
    for i in range(0, len(mensagem), 2):  # Itera sobre a mensagem em pares de caracteres
        pos1 = encontrar_posicao(matriz, mensagem[i])  # Encontra a posição do primeiro caractere
        pos2 = encontrar_posicao(matriz, mensagem[i + 1])  # Encontra a posição do segundo caractere

        if pos1 == (None, None) or pos2 == (None, None):
            resultado += mensagem[i] + mensagem[i + 1]  # Ignora caracteres não encontrados na matriz
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

        resultado += matriz[linha1][coluna1] + matriz[linha2][coluna2]  # Adiciona os caracteres criptografados ou descriptografados
    
    return resultado  # Retorna a mensagem criptografada ou descriptografada

# Função que implementa a Cifra de Vigenère
def cifra_de_vigenere(mensagem, chave, criptografar=True):
    resultado = ''  # Inicializa a string para armazenar o resultado
    chave = chave.lower()  # Converte a chave para minúsculas
    indice_chave = 0  # Inicializa o índice da chave
    
    for caractere in mensagem:  # Itera sobre cada caractere da mensagem
        if caractere.isalpha():  # Verifica se o caractere é uma letra
            deslocamento = ord(chave[indice_chave]) - ord('a')  # Calcula o deslocamento com base na chave
            deslocamento = deslocamento if criptografar else -deslocamento  # Define o deslocamento com base na criptografia ou descriptografia
            base = ord('A') if caractere.isupper() else ord('a')  # Define a base ASCII para maiúsculas ou minúsculas
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)  # Aplica a cifra e adiciona o caractere ao resultado
            indice_chave = (indice_chave + 1) % len(chave)  # Atualiza o índice da chave
        else:
            resultado += caractere  # Adiciona caracteres não alfabéticos sem modificação
    
    return resultado  # Retorna a mensagem criptografada ou descriptografada

# Função que aplica a cifra escolhida na mensagem
def criptografar_mensagem(mensagem):
    if escolha == '1':
        return cifra_de_cesar(mensagem, int(chave))  # Aplica a Cifra de César
    elif escolha == '2':
        return cifra_monoalfabetica(mensagem, chave)  # Aplica a Substituição Monoalfabética
    elif escolha == '3':
        return cifra_de_playfair(mensagem, chave)  # Aplica a Cifra de Playfair
    elif escolha == '4':
        return cifra_de_vigenere(mensagem, chave)  # Aplica a Cifra de Vigenère
    else:
        return mensagem  # Retorna a mensagem original se a escolha não for válida

# Função que recebe mensagens do servidor
def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')  # Recebe e decodifica a mensagem do servidor
            print(mensagem)  # Exibe a mensagem recebida
        except:
            print("Ocorreu um erro!")  # Exibe mensagem de erro
            cliente.close()  # Fecha a conexão com o servidor
            break  # Sai do loop

# Função que envia mensagens para o servidor
def enviar_mensagens():
    while True:
        mensagem = '{}: {}'.format(apelido, input(''))  # Formata a mensagem com o apelido do usuário
        mensagem_criptografada = criptografar_mensagem(mensagem)  # Criptografa a mensagem
        cliente.send(mensagem_criptografada.encode('ascii'))  # Envia a mensagem criptografada para o servidor

# Conectando ao servidor
apelido = input("Escolha seu apelido: ")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

# Inicia uma thread para receber mensagens do servidor
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

# Inicia uma thread para enviar mensagens para o servidor
thread_enviar = threading.Thread(target=enviar_mensagens)
thread_enviar.start()
