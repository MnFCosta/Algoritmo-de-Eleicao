import argparse
import socket
import threading
import time

enderecos_servers = [
    ('localhost', 8001),
    ('localhost', 8002),
    ('localhost', 8003),   
]

def cliente(id, endereco_prox_servidor,):
    esperando_conexao = True
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while esperando_conexao:
        try:
            client_socket.connect(endereco_prox_servidor)
            break
        except:
            pass
    

    print(f"CONECTADO AO PROCESSO {endereco_prox_servidor}")

    while True:
        client_socket.sendall(f'{id}'.encode())
        data = client_socket.recv(1024)
        data = data.decode('utf-8')
        print(data)
        time.sleep(5)



            
def server(id):
    global enderecos_servers
    coordenador = False
    endereco_prox_servidor = enderecos_servers[id % len(enderecos_servers)]

    endereco = enderecos_servers[id-1]

    # Cria socket de servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(endereco)
    
    server_socket.listen()

    print(f'Processo {id} com o endereco {endereco} escutando')

    cliente_thread = threading.Thread(target=cliente, args=(id, endereco_prox_servidor,))
    cliente_thread.start()

    while True:
        conn, client_address = server_socket.accept()
        print(f"Conexão de: {client_address} REQUISITADA")
        print(f"Conexão de: {client_address} INICIADA")
        data = conn.recv(1024)
        data = data.decode('utf-8')

        if data == 'Ping' and coordenador:
            print(f"Coordenador recebeu: {data}")
            conn.sendall('PONG'.encode())
        if data == 'ELEICAO':
            print("ELEICAO")
        else:
            print(data)

        if not data:
            break
        




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, help="Client ID", required=True)
    args = parser.parse_args()
    server(args.id)
    

if __name__ == "__main__":
    main()