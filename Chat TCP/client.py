import socket
import threading

class SimpleSubstitution:
    def __init__(self):
        self.p_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.decrypting = False

    def cipher_alphabet(self, password):
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
    elif cipher_type == '3':  # Playfair Cipher
        return playfair_cipher(message, password, 'encrypt')
    # Add other cipher implementations here
    return message

def decrypt_message(message, cipher_type, key, password=None):
    if cipher_type == '1':  # Caesar Cipher
        return caesar(message, key, 'decrypt')
    elif cipher_type == '2':  # Substitution Cipher
        substitution = SimpleSubstitution()
        return substitution.decrypt(message, password)
    elif cipher_type == '3':  # Playfair Cipher
        return playfair_cipher(message, password, 'decrypt')
    # Add other cipher implementations here
    return message

def playfair_cipher(plaintext, key, mode):
    alphabet = 'abcdefghiklmnopqrstuvwxyz'
    key = key.lower().replace(' ', '').replace('j', 'i')
    key_square = ''
    for letter in key + alphabet:
        if letter not in key_square:
            key_square += letter
    plaintext = plaintext.lower().replace(' ', '').replace('j', 'i')
    if len(plaintext) % 2 == 1:
        plaintext += 'x'
    digraphs = [plaintext[i:i+2] for i in range(0, len(plaintext), 2)]

    def encrypt(digraph):
        a, b = digraph
        row_a, col_a = divmod(key_square.index(a), 5)
        row_b, col_b = divmod(key_square.index(b), 5)
        if row_a == row_b:
            col_a = (col_a + 1) % 5
            col_b = (col_b + 1) % 5
        elif col_a == col_b:
            row_a = (row_a + 1) % 5
            row_b = (row_b + 1) % 5
        else:
            col_a, col_b = col_b, col_a
        return key_square[row_a*5+col_a] + key_square[row_b*5+col_b]

    def decrypt(digraph):
        a, b = digraph
        row_a, col_a = divmod(key_square.index(a), 5)
        row_b, col_b = divmod(key_square.index(b), 5)
        if row_a == row_b:
            col_a = (col_a - 1) % 5
            col_b = (col_b - 1) % 5
        elif col_a == col_b:
            row_a = (row_a - 1) % 5
            row_b = (row_b - 1) % 5
        else:
            col_a, col_b = col_b, col_a
        return key_square[row_a*5+col_a] + key_square[row_b*5+col_b]

    result = ''
    for digraph in digraphs:
        if mode == 'encrypt':
            result += encrypt(digraph)
        elif mode == 'decrypt':
            result += decrypt(digraph)

    return result

print("Tarefa 2")
print("Atividade em Dupla: Implementação de Cifras Clássicas em um Chat TCP")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = input("Digite o endereço IP do servidor, exemplo '127.0.0.1': ")
server_port = input("Digite a porta do servidor, exemplo '55555': ")

try:
    client.connect((server_ip, int(server_port)))
except socket.error as e:
    print(f"Erro ao conectar ao servidor: {e}")
    exit()

nickname = input("Escolha seu apelido:\n ")

print("1. Cifra de César")
print("2. Substituição Monoalfabética")
print("3. Cifra de Playfair")
print("4. Cifra de Vigenère")

cifra = input("Digite uma das opções, cifra de criptografia a ser utilizada: \n")

if cifra == '1':
    chave = int(input("Digite o valor da chave entre 1 a 25 para cifrar e decifrar a mensagem: \n"))
    password = None
elif cifra == '2':
    password = input("Digite a palavra-chave para a cifra de substituição: \n")
    chave = None
elif cifra == '3':
    password = input("Digite a palavra-chave para a cifra de Playfair: \n")
    chave = None
else:
    print("Opção de cifra inválida")
    exit()

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                decoded_message = decrypt_message(message, cifra, chave, password)
                print(decoded_message)
        except:
            print("Ocorreu um erro!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        encoded_message = encrypt_message(message, cifra, chave, password)
        client.send(encoded_message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
