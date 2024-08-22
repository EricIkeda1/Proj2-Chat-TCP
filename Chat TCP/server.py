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

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            cipher_type = message[0]
            key = None
            password = None
            if cipher_type in ['1', '2', '3']:
                key = int(input("Digite a chave (para cifra de César) ou None (para outras cifras): \n"))
                if cipher_type == '2':
                    password = input("Digite a palavra-chave para a cifra de substituição: \n")
                elif cipher_type == '3':
                    password = input("Digite a palavra-chave para a cifra de Playfair: \n")
            decrypted_message = decrypt_message(message[1:], cipher_type, key, password)
            print(f"Recebido: {decrypted_message}")
            encrypted_message = encrypt_message(decrypted_message, cipher_type, key, password)
            client_socket.send(encrypted_message.encode('utf-8'))
        except:
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 55555))
server.listen(5)

print("Servidor iniciado. Aguardando conexões...")

def start():
    while True:
        client_socket, addr = server.accept()
        print(f"Conectado com {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

start()
