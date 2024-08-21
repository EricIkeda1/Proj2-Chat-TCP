import socket
import threading

class SimpleSubstitution:
    def __init__(self):
        self.p_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.decrypting = False

    def cipher_alphabet(self, password):
        ''' (str) -> str
        Retorna um alfabeto cifrado iniciado com
        o texto da palavra chave password
        '''
        c_alphabet = []
        password = password.upper()
        for ch in password:
            if ch not in c_alphabet:
                c_alphabet.append(ch)
                idx = self.p_alphabet.find(ch)
        p_alphabet = self.p_alphabet[idx:] + self.p_alphabet[:idx]
        for ch in p_alphabet:
            if ch not in c_alphabet:
                c_alphabet.append(ch)
        return ''.join(c_alphabet)

    def encrypt(self, plaintext, password):
        '''(str, str) -> str
        Retorna o texto plano cifrado com a cifra de
        substituicao com a palavra chave password
        '''
        txt = ''
        p_alphabet = self.p_alphabet
        text = plaintext.replace(' ', '').upper()
        cipher = self.cipher_alphabet(password)
        if self.decrypting:
            p_alphabet, cipher = cipher, p_alphabet
            self.decrypting = False
        for ch in text:
            txt += cipher[p_alphabet.find(ch)]
        return txt

    def decrypt(self, ciphertext, password):
        '''(str, str) -> str
        Retorna o texto cifrado decifrado com a cifra de
        substituicao com a palavra chave password
        '''
        self.decrypting = True
        return self.encrypt(ciphertext, password)

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

def encrypt_message(message, cipher_type, key, password=None):
    if cipher_type == '1':  # Caesar Cipher
        return caesar(message, key, 'encrypt')
    elif cipher_type == '2':  # Substitution Cipher
        substitution = SimpleSubstitution()
        return substitution.encrypt(message, password)
    # Add other cipher implementations here
    return message

def decrypt_message(message, cipher_type, key, password=None):
    if cipher_type == '1':  # Caesar Cipher
        return caesar(message, key, 'decrypt')
    elif cipher_type == '2':  # Substitution Cipher
        substitution = SimpleSubstitution()
        return substitution.decrypt(message, password)
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

# Função para determinar o tipo de cifra e chave
if cifra == '1':
    chave = int(input("Digite o valor da chave entre 1 a 25 para cifrar e decifrar a mensagem: \n"))
    password = None
elif cifra == '2':
    password = input("Digite a palavra-chave para a cifra de substituição: \n")
    chave = None
else:
    print("Opção de cifra inválida")
    exit()

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
                decoded_message = decrypt_message(message, cifra, chave, password)
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
        encoded_message = encrypt_message(message, cifra, chave, password)
        client.send(encoded_message.encode('utf-8'))

# Iniciando threads para ouvir e escrever
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
