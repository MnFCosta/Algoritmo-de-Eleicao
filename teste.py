import argparse
import socket
import threading
import time

enderecos_servers = [
    ('localhost', 8001),
    ('localhost', 8002),
    ('localhost', 8003),   
]

def cliente(id, coordenador,):
    print(coordenador)
    esperando_conexao = True
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while esperando_conexao:
        try:
            client_socket.connect(coordenador)
            break
        except:
            pass
    

    print(f"CONECTADO AO COORDENADOR {coordenador}")

    while True:
        client_socket.sendall(f'{id}'.encode())
        data = client_socket.recv(1024)
        data = data.decode('utf-8')
        print(data)
        time.sleep(5)

def mandar_msg(endereco_prox_servidor, mensagem):
    print("Endereco")
    esperando_conexao = True
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while esperando_conexao:
        try:
            client_socket.connect(endereco_prox_servidor)
            break
        except:
            pass
    client_socket.sendall(f'{mensagem}'.encode())

    client_socket.close()

def eleicao(endereco):
    print("ENTROU")
    esperando_conexao = True
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while esperando_conexao:
        try:
            client_socket.connect(endereco)
            break
        except:
            pass
    client_socket.sendall(f'ELEICAO'.encode())

    client_socket.close()
        
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

    eleicao(endereco_prox_servidor)

    while True:
        conn, client_address = server_socket.accept()
        print(f"Conexão de: {client_address} REQUISITADA")
        print(f"Conexão de: {client_address} INICIADA")
        data = conn.recv(1024)
        data = data.decode('utf-8')

        if data.split("|")[0] == 'ELEITO' and coordenador:
            pass

        if data.split("|")[0] == 'ELEITO' and not coordenador:
            cliente_thread = threading.Thread(target=cliente, args=(data.split("|")[1], id))
            cliente_thread.start()

        if data == 'Ping' and coordenador:
            print(f"Coordenador recebeu: {data}")
            conn.sendall('PONG'.encode())
        if data == 'ELEICAO':
            msg = threading.Thread(target=mandar_msg, args=(endereco_prox_servidor, id))
            msg.start()
        else:
            if coordenador:
                pass
            if int(data) == id:
                print("Você é o novo coordenador!")
                coordenador = True
                msg = threading.Thread(target=mandar_msg, args=(endereco_prox_servidor, f'ELEITO|{id}'))
                msg.start()

            if int(data) < id:
                print("passe pro proximo sua id")
                msg = threading.Thread(target=mandar_msg, args=(endereco_prox_servidor, id))
                msg.start()
            if int(data) > id:
                print("passe a id recebida para o proximo")
                msg = threading.Thread(target=mandar_msg, args=(endereco_prox_servidor, int(data)))
                msg.start()

        if not data:
            break




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, help="Client ID", required=True)
    args = parser.parse_args()
    server(args.id)
    

if __name__ == "__main__":
    main()