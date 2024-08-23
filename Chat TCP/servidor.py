import socket  # Importa o módulo socket para comunicação de rede
import threading  # Importa o módulo threading para executar código em paralelo

# Função para criptografar e descriptografar mensagens usando a cifra de César
def cifra_de_cesar(mensagem, chave, criptografar=True):
    resultado = ''  # Inicializa a variável para armazenar o resultado
    deslocamento = chave if criptografar else -chave  # Define o deslocamento para criptografar ou descriptografar
    for caractere in mensagem:  # Itera sobre cada caractere da mensagem
        if caractere.isalpha():  # Verifica se o caractere é uma letra
            base = ord('A') if caractere.isupper() else ord('a')  # Define a base ASCII dependendo se a letra é maiúscula ou minúscula
            # Calcula o novo caractere aplicando a cifra de César e adiciona ao resultado
            resultado += chr((ord(caractere) - base + deslocamento) % 26 + base)
        else:
            resultado += caractere  # Adiciona caracteres não alfabéticos sem modificação
    return resultado  # Retorna a mensagem criptografada ou descriptografada

# Função que gerencia as mensagens recebidas de um cliente
def gerenciar_cliente(cliente):
    while True:  # Loop para continuar gerenciando o cliente enquanto estiver conectado
        try:
            # Recebe a mensagem criptografada do cliente e decodifica para texto
            mensagem_criptografada = cliente.recv(1024).decode('ascii')
            print(f"[Mensagem recebida antes da criptografia]: {mensagem_criptografada}")

            # Descriptografa a mensagem usando a cifra de César com chave 3
            mensagem_desencriptada = cifra_de_cesar(mensagem_criptografada, 3, criptografar=False)
            print(f"[Mensagem descriptografada]: {mensagem_desencriptada}")

            # Recriptografa a mensagem para enviar de volta para todos os clientes
            mensagem_criptografada_devolvida = cifra_de_cesar(mensagem_desencriptada, 3)
            print(f"[Mensagem criptografada antes do envio]: {mensagem_criptografada_devolvida}")

            # Envia a mensagem criptografada para todos os clientes conectados
            transmitir_para_todos(mensagem_criptografada_devolvida.encode('ascii'))
        except:  # Em caso de erro
            # Obtém o índice do cliente na lista
            indice = clientes.index(cliente)
            clientes.remove(cliente)  # Remove o cliente da lista
            cliente.close()  # Fecha a conexão com o cliente
            apelido = apelidos[indice]  # Obtém o apelido do cliente
            # Notifica todos os clientes de que o cliente saiu
            transmitir_para_todos(f'{apelido} saiu!'.encode('ascii'))
            apelidos.remove(apelido)  # Remove o apelido da lista
            break  # Sai do loop

# Função que envia uma mensagem para todos os clientes conectados
def transmitir_para_todos(mensagem):
    for cliente in clientes:  # Itera sobre todos os clientes
        cliente.send(mensagem)  # Envia a mensagem para o cliente

# Função que aceita novas conexões de clientes
def aceitar_conexoes():
    while True:  # Loop para continuar aceitando novas conexões
        # Aceita uma nova conexão do cliente e obtém o endereço do cliente
        cliente, endereco = servidor.accept()
        print(f"Conectado com {str(endereco)}")

        # Pede o apelido do cliente
        cliente.send('APELIDO'.encode('ascii'))
        apelido = cliente.recv(1024).decode('ascii')
        apelidos.append(apelido)  # Adiciona o apelido à lista de apelidos
        clientes.append(cliente)  # Adiciona o cliente à lista de clientes

        print(f"Apelido é {apelido}")
        # Notifica todos os clientes de que um novo cliente entrou
        transmitir_para_todos(f"{apelido} entrou!".encode('ascii'))
        cliente.send('Conectado ao servidor!'.encode('ascii'))

        # Cria uma nova thread para gerenciar as mensagens desse cliente
        thread = threading.Thread(target=gerenciar_cliente, args=(cliente,))
        thread.start()

# Configurações do servidor
ip_servidor = '127.0.0.1'  # Define o IP em que o servidor vai escutar
porta_servidor = 55555  # Define a porta em que o servidor vai escutar

# Inicializa o servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
servidor.bind((ip_servidor, porta_servidor))  # Associa o socket ao IP e porta
servidor.listen()  # Coloca o servidor em modo de escuta

clientes = []  # Lista para armazenar clientes conectados
apelidos = []  # Lista para armazenar apelidos dos clientes

print("Servidor iniciado e aguardando conexões...")  # Mensagem indicando que o servidor está pronto para aceitar conexões

aceitar_conexoes()  # Inicia a aceitação de novas conexões
