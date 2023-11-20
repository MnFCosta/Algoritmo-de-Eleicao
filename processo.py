import argparse
import socket
import threading
import time

enderecos_servers = [
    ('localhost', 8001),
    ('localhost', 8002),
    ('localhost', 8003),
    ('localhost', 8004),
    ('localhost', 8005),
    ('localhost', 8006),
    ('localhost', 8007),
       
]

def cliente(id, coordenador,):
    coordenador = enderecos_servers[int(coordenador) - 1]

    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(coordenador)
            client_socket.sendall(f'PING'.encode())
        except Exception as e:
            servidor_do_cliente = enderecos_servers[int(id) - 1]
            enderecos_servers.pop()
            client_socket.close()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(servidor_do_cliente)
            client_socket.sendall(f'ELEICAO'.encode())
            client_socket.close()
            break
        
        try:
            data = client_socket.recv(1024)
            data = data.decode('utf-8')
            print(data)
        except Exception as e:
            client_socket.close()

        client_socket.close()
        time.sleep(5)

def mandar_msg(endereco_prox_servidor, mensagem):
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

def eleicao_inicial(endereco):
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
    participante = False

    endereco = enderecos_servers[id-1]

    # Cria socket de servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(endereco)
    
    server_socket.listen()

    print(f'Processo {id} com o endereco {endereco} escutando')

    eleicao_inicial(enderecos_servers[id % len(enderecos_servers)])

    while True:
        conn, client_address = server_socket.accept()
        data = conn.recv(1024)
        data = data.decode('utf-8')

        if data.split("|")[0] == 'ELEITO' and participante and not coordenador:
            participante = False
            cliente_thread = threading.Thread(target=cliente, args=(id, data.split("|")[1]))
            cliente_thread.start()
            msg = threading.Thread(target=mandar_msg, args=(enderecos_servers[id % len(enderecos_servers)], data))
            msg.start()

        if data == 'PING' and coordenador:
            print(f"Coordenador recebeu: {data}")
            conn.sendall('PONG'.encode())

        if participante:
            if int(data) == id:
                print("Você é o novo coordenador!")
                if len(enderecos_servers) == 1:
                        print("Novo anel de conexões não pode ser criado, apenas 1 servidor restante.")
                        break
                coordenador = True
                participante = False
                msg = threading.Thread(target=mandar_msg, args=(enderecos_servers[id % len(enderecos_servers)], f'ELEITO|{id}'))
                msg.start()

            if int(data) < id:
                print("passe pro proximo sua id")
                msg = threading.Thread(target=mandar_msg, args=(enderecos_servers[id % len(enderecos_servers)], id))
                msg.start()
            if int(data) > id:
                print("passe a id recebida para o proximo")
                msg = threading.Thread(target=mandar_msg, args=(enderecos_servers[id % len(enderecos_servers)], int(data)))
                msg.start()

        if data == 'ELEICAO':
            participante = True
            msg = threading.Thread(target=mandar_msg, args=(enderecos_servers[id % len(enderecos_servers)], id))
            msg.start()





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, help="Client ID", required=True)
    args = parser.parse_args()
    server(args.id)
    

if __name__ == "__main__":
    main()