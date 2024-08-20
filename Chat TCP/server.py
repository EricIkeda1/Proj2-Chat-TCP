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

# Dados da conexão
host = '127.0.0.1'
port = 55555

# Iniciando o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Listas para clientes e seus apelidos
clients = []
nicknames = []

# Função para enviar mensagens para todos os clientes conectados
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            # Remove client from list if there's an error
            clients.remove(client)
            client.close()

# Função para lidar com mensagens dos clientes
def handle(client):
    cipher_type = '1'  # Default to Caesar Cipher
    key = 1            # Default key
    
    while True:
        try:
            # Recebendo mensagens e transmitindo para todos os clientes
            message = client.recv(1024).decode('utf-8')
            decrypted_message = decrypt_message(message, cipher_type, key)
            broadcast(decrypted_message.encode('utf-8'))
        except:
            # Removendo e fechando clientes desconectados
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} saiu!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Função para receber conexões
def receive():
    while True:
        # Aceitando conexão
        client, address = server.accept()
        print(f"Conectado com {str(address)}")

        # Solicitando e armazenando apelido
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Imprimindo e transmitindo apelido
        print(f"Apelido é {nickname}")
        broadcast(f"{nickname} entrou!".encode('utf-8'))
        client.send('Conectado ao servidor, Opções!'.encode('utf-8'))

        # Iniciando thread para lidar com o cliente
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
receive()
