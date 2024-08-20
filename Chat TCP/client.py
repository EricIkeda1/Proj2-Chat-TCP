import socket
import threading

def caesar(data, key, mode):
    alphabet = 'abcdefghijklmnopqrstuvwyzàáãâéêóôõíúçABCDEFGHIJKLMNOPQRSTUVWYZÀÁÃÂÉÊÓÕÍÚÇ'
    new_data = ''
    for c in data:
        index = alphabet.find(c)
        if index == -1:
            new_data += c
        else:
            new_index = index + key if mode == 'encrypt' else index - key
            new_index = new_index % len(alphabet)
            new_data += alphabet[new_index:new_index+1]
    return new_data

def encrypt_message(message, cipher_type, key):
    if cipher_type == '1':  # Caesar Cipher
        return caesar(message, key, 'encrypt')
    # Add other cipher implementations here
    return message

def decrypt_message(message, cipher_type, key):
    if cipher_type == '1':  # Caesar Cipher
        return caesar(message, key, 'decrypt')
    # Add other cipher implementations here
    return message

print("Tarefa 2")
print("Atividade em Dupla: Implementação de Cifras Clássicas em um Chat TCP")

# Conectando ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Solicitar ao usuário que digite o número do servidor e a porta
server_ip = input("Digite o endereço IP do servidor, exemplo '127.0.0.1': ")
server_port = input("Digite a porta do servidor, exemplo '55555': ")

try:
    # Conectar ao servidor usando os valores fornecidos pelo usuário
    client.connect((server_ip, int(server_port)))
except socket.error as e:
    print(f"Erro ao conectar ao servidor: {e}")
    exit()

# Escolhendo um apelido
nickname = input("Escolha seu apelido:\n ")

print("1. Cifra de César")
print("2. Substituição Monoalfabética")
print("3. Cifra de Playfair")
print("4. Cifra de Vigenère")

# Usuário vai digitar e ser lido uma das opções
cifra = input("Digite uma das opções, cifra de criptografia a ser utilizada: \n")

# Em seguida, o usuário deverá fornecer a chave previamente combinada com seu parceiro.
chave = int(input("Digite o valor da chave entre 1 a 4, para codificar e decodificar a mensagem: \n"))

# Função para ouvir o servidor e enviar o apelido
def receive():
    while True:
        try:
            # Receber mensagem do servidor
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                # Decodificar a mensagem recebida
                decoded_message = decrypt_message(message, cifra, chave)
                print(decoded_message)
        except:
            # Fechar conexão em caso de erro
            print("Ocorreu um erro!")
            client.close()
            break
        
# Função para enviar mensagens ao servidor
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        # Codificar a mensagem antes de enviar
        encoded_message = encrypt_message(message, cifra, chave)
        client.send(encoded_message.encode('utf-8'))
        
# Iniciando threads para ouvir e escrever
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
