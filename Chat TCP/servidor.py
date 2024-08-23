import socket
import threading

# Funções de criptografia

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

# Função que gerencia as mensagens recebidas dos clientes
def gerenciar_cliente(cliente):
    while True:
        try:
            # Recebendo a mensagem do cliente
            mensagem_criptografada = cliente.recv(1024).decode('ascii')
            print(f"[Mensagem recebida antes da criptografia]: {mensagem_criptografada}")
            
            # Exemplo de criptografia usando a Cifra de César com chave 3
            mensagem_desencriptada = cifra_de_cesar(mensagem_criptografada, 3, criptografar=False)
            print(f"[Mensagem descriptografada]: {mensagem_desencriptada}")
            
            mensagem_criptografada_devolvida = cifra_de_cesar(mensagem_desencriptada, 3)
            print(f"[Mensagem criptografada antes do envio]: {mensagem_criptografada_devolvida}")
            
            # Enviando a mensagem criptografada para todos os clientes
            transmitir_para_todos(mensagem_criptografada_devolvida.encode('ascii'))
        except:
            # Em caso de erro, remove o cliente da lista e fecha a conexão
            indice = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            apelido = apelidos[indice]
            transmitir_para_todos(f'{apelido} saiu!'.encode('ascii'))
            apelidos.remove(apelido)
            break

# Função que envia uma mensagem para todos os clientes conectados
def transmitir_para_todos(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)

# Função que recebe novas conexões de clientes
def aceitar_conexoes():
    while True:
        cliente, endereco = servidor.accept()
        print(f"Conectado com {str(endereco)}")

        # Pedindo o apelido do cliente
        cliente.send('APELIDO'.encode('ascii'))
        apelido = cliente.recv(1024).decode('ascii')
        apelidos.append(apelido)
        clientes.append(cliente)

        print(f"Apelido é {apelido}")
        transmitir_para_todos(f"{apelido} entrou!".encode('ascii'))
        cliente.send('Conectado ao servidor!'.encode('ascii'))

        # Criando uma nova thread para gerenciar as mensagens desse cliente
        thread = threading.Thread(target=gerenciar_cliente, args=(cliente,))
        thread.start()

# Configurações do servidor
ip_servidor = '0.0.0.0'
porta_servidor = 55555

# Inicializando o servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((ip_servidor, porta_servidor))
servidor.listen()

clientes = []
apelidos = []

print("Servidor iniciado e aguardando conexões...")

aceitar_conexoes()
