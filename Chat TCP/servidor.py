import socket  # Importa o módulo socket para comunicação de rede
import threading  # Importa o módulo threading para criar e gerenciar threads

# Função que implementa a Cifra de César
def cifra_de_cesar(mensagem, chave, criptografar=True):
    resultado = ''  # Inicializa a string para armazenar o resultado
    deslocamento = chave if criptografar else -chave  # Define o deslocamento com base na criptografia (positiva) ou descriptografia (negativa)
    for caractere in mensagem:  # Itera sobre cada caractere da mensagem
        if caractere.isalpha():  # Verifica se o caractere é uma letra
            base = ord('A') if caractere.isupper() else ord('a')  # Define a base ASCII para maiúsculas ou minúsculas
            # Aplica a cifra de César e adiciona o caractere criptografado ao resultado
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
        else:
            resultado += caractere  # Adiciona caracteres não alfabéticos sem modificação
    return resultado  # Retorna a mensagem criptografada ou descriptografada

# Função que gerencia as mensagens recebidas dos clientes
def gerenciar_cliente(cliente):
    while True:  # Loop contínuo para gerenciar as mensagens do cliente
        try:
            # Recebendo a mensagem do cliente (máximo de 1024 bytes) e decodificando de bytes para string ASCII
            mensagem = cliente.recv(1024).decode('ascii')
            print(f"[Mensagem recebida antes da criptografia]: {mensagem}")
            
            # Exemplo de criptografia usando a Cifra de César com chave 3
            mensagem_criptografada = cifra_de_cesar(mensagem, 3)
            print(f"[Mensagem criptografada]: {mensagem_criptografada}")
            
            # Enviando a mensagem criptografada para todos os clientes conectados
            transmitir_para_todos(mensagem_criptografada.encode('ascii'))
        except:
            # Em caso de erro (por exemplo, desconexão), remove o cliente da lista e fecha a conexão
            indice = clientes.index(cliente)  # Obtém o índice do cliente na lista de clientes
            clientes.remove(cliente)  # Remove o cliente da lista de clientes
            cliente.close()  # Fecha a conexão com o cliente
            apelido = apelidos[indice]  # Obtém o apelido do cliente
            transmitir_para_todos(f'{apelido} saiu!'.encode('ascii'))  # Informa aos outros clientes que o cliente saiu
            apelidos.remove(apelido)  # Remove o apelido da lista de apelidos
            break  # Sai do loop

# Função que envia uma mensagem para todos os clientes conectados
def transmitir_para_todos(mensagem):
    for cliente in clientes:  # Itera sobre cada cliente na lista de clientes
        cliente.send(mensagem)  # Envia a mensagem para o cliente

# Função que recebe novas conexões de clientes
def aceitar_conexoes():
    while True:  # Loop contínuo para aceitar novas conexões
        cliente, endereco = servidor.accept()  # Aceita uma nova conexão e obtém o socket do cliente e o endereço
        print(f"Conectado com {str(endereco)}")

        # Pedindo o apelido do cliente
        cliente.send('APELIDO'.encode('ascii'))  # Solicita ao cliente que envie seu apelido
        apelido = cliente.recv(1024).decode('ascii')  # Recebe o apelido do cliente
        apelidos.append(apelido)  # Adiciona o apelido à lista de apelidos
        clientes.append(cliente)  # Adiciona o socket do cliente à lista de clientes

        print(f"Apelido é {apelido}")
        transmitir_para_todos(f"{apelido} entrou!".encode('ascii'))  # Informa aos outros clientes que um novo cliente entrou
        cliente.send('Conectado ao servidor!'.encode('ascii'))  # Envia uma mensagem ao novo cliente confirmando a conexão

        # Criando uma nova thread para gerenciar as mensagens desse cliente
        thread = threading.Thread(target=gerenciar_cliente, args=(cliente,))
        thread.start()  # Inicia a thread

# Configuração do servidor
host = '127.0.0.1'  # Define o endereço IP do servidor (localhost)
porta = 55555  # Define a porta de escuta do servidor

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP/IP
servidor.bind((host, porta))  # Associa o socket ao endereço IP e porta
servidor.listen()  # Configura o socket para aceitar conexões

clientes = []  # Lista para armazenar os sockets dos clientes conectados
apelidos = []  # Lista para armazenar os apelidos dos clientes conectados

print("Servidor está rodando...")  # Exibe mensagem indicando que o servidor está em execução
aceitar_conexoes()  # Inicia a função para aceitar conexões de clientes
