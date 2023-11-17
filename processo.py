import socket
import threading
import time


# Endereço dos servidores no anel
enderecos_servers = [
    ('localhost', 8001),
    ('localhost', 8002),
    ('localhost', 8003),   
]

threads = []

coordenador_recebendo = True


def terminar_coordenador(coordenador):
    global coordenador_recebendo
    time.sleep(20)
    try:
        coordenador.close()
    except:
        print("Não deu")

def cliente(id, coordenador, servidor):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(coordenador)

    time.sleep(5)

    while True:
        try:
            client_socket.sendall('Ping'.encode())
        except:
            print("COORDENADOR MORREU")
            client_socket.close()  # Close the existing connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket
            client_socket.connect(servidor)
            client_socket.sendall('ELEICAO'.encode())
        data = client_socket.recv(1024)
        data = data.decode('utf-8')
        print(f"PROCESSO {id} recebeu: {data}")
        time.sleep(5)


def thread_conexao(conn, client_address):
        print(f"Conexão de: {client_address} INICIADA")
        while True:
            data = conn.recv(1024)
            data = data.decode('utf-8')

            if data == 'Ping':
                print(f"Coordenador recebeu: {data}")
                conn.sendall('PONG'.encode())
            if data == 'ELEICAO':
                print("ELEICAO GARAI")

            if not data:
                break

def server(id, endereco, endereco_prox_servidor):
    global enderecos_servers
    global coordenador_recebendo
    coordenador = False 

    # Cria socket de servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(endereco)
    
    server_socket.listen()

    if id == len(enderecos_servers):
        coordenador = True
        terminar_thread = threading.Thread(target=terminar_coordenador, args=(server_socket,))
        terminar_thread.start()

    if not coordenador:
            coordenador = enderecos_servers[len(enderecos_servers) - 1]
            cliente_thread = threading.Thread(target=cliente, args=(id, coordenador, endereco))
            cliente_thread.start()
    
    while True:
        conn, client_address = server_socket.accept()
        print(f"Conexão de: {client_address} REQUISITADA")
        resposta_thread = threading.Thread(target=thread_conexao, args=(conn, client_address))
        resposta_thread.start()

        



def main():
    global enderecos_servers
    global threads

    # Inicia uma thread pra cada server
    for i in range(len(enderecos_servers)):
        endereco_prox_servidor = enderecos_servers[(i + 1) % len(enderecos_servers)]
        thread = threading.Thread(target=server, args=(i + 1, enderecos_servers[i], endereco_prox_servidor,))
        threads.append(thread)
        thread.start()

    # espera todas as threads terminarem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()