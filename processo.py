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

def server(id, endereco, endereco_prox_servidor):
    global enderecos_servers

    # Cria socket de servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(endereco)
    lider = False
    participante = False
    conectado = False
    
    server_socket.listen()
    
    # def eleicao():
    #     print(f"Server {id} em {endereco} esperando conexão...")
    #     conn, endereco_cliente = server_socket.accept()
    #     print(f"Conexão de {endereco_cliente}")

    #     # Recebe a mensagem enviada
    #     data = conn.recv(1024)

    #     data = data.decode('utf-8')
    #     print(f"Server {id} recebeu: {data}")


    #     if data == "ELEICAO":
    #         participante = True
    #         print(data)
    #         data = f'{id}'
    #         print(data)
    #         # Manda mensagem para o próximo server no anel
    #         mandar_mensagem(endereco_prox_servidor, data.encode())
    #     else:
    #         if int(data) == id:
    #             print(f"Processo {id} eleito o novo líder!")
    #             lider = True

    #         if int(data) > id:
    #             participante = True
    #             # Manda mensagem para o próximo server no anel
    #             mandar_mensagem(endereco_prox_servidor, data.encode())
            
    #         if int(data) < id and participante == False:
    #             data = f'{id}'
    #             # Manda mensagem para o próximo server no anel
    #             mandar_mensagem(endereco_prox_servidor, data.encode())
            
        
    #     time.sleep(5)

    #     # Fecha a conexão atual
    #     conn.close() 

    def thread_conexao(conn, client_address):
        contador = 0
        print(f"Conexão de: {client_address} INICIADA")
        while contador != 2:
            contador += 1
            data = conn.recv(1024)
            data = data.decode('utf-8')
            print(f"Lider {id} recebeu: {data}")
            conn.sendall('Olá!'.encode())

            if not data:
                break
        
        

    if id == len(enderecos_servers):
        while True:
            conn, client_address = server_socket.accept()
            print(f"Conexão de: {client_address} REQUISITADA")

            connection_thread = threading.Thread(target=thread_conexao, args=(conn, client_address))
            connection_thread.start()
            
    else:
        while True:
            if conectado == False:
                lider = enderecos_servers[len(enderecos_servers) - 1]
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(lider)
                conectado = True
                
            time.sleep(5)

            client_socket.sendall(f'Processo {id}: Olá lider!'.encode())

            # Recebe a mensagem enviada
            try:
                data = client_socket.recv(1024)
            except:
                print("Lider caiu")
                data = 'ELEICAO'
                print(f"Processo {id} recebeu: {data}")
                break
                

            data = data.decode('utf-8')
            print(f"Processo {id} recebeu: {data}")
        



def mandar_mensagem(endereco_destino, mensagem):
    # Cria um socket com uma conexão ao próximo server no anel
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(endereco_destino)

        # Manda mensagem para o próximo server
        client_socket.sendall(mensagem)


def main():
    global enderecos_servers
    global threads

    # Inicia uma thread pra cada server
    for i in range(len(enderecos_servers)):
        endereco_prox_servidor = enderecos_servers[(i + 1) % len(enderecos_servers)]
        thread = threading.Thread(target=server, args=(i + 1, enderecos_servers[i], endereco_prox_servidor))
        threads.append(thread)
        thread.start()

    # espera todas as threads terminarem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()