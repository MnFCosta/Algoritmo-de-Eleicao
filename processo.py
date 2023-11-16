import socket
import threading
import time

def server(id, endereco, endereco_prox_servidor):
    # Cria socket de servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(endereco)
    server_socket.listen(1)
    participante = False
    lider = False

    while True:
        print(f"Server {id} em {endereco} esperando conexão...")
        conn, endereco_cliente = server_socket.accept()
        print(f"Conexão de {endereco_cliente}")

        # Recebe a mensagem enviada
        data = conn.recv(1024)

        data = data.decode('utf-8')
        print(f"Server {id} recebeu: {data}")


        if data == "ELEICAO":
            participante = True
            print(data)
            data = f'{id}'
            print(data)
            # Forward the message to the next server in the ring
            mandar_mensagem(endereco_prox_servidor, data.encode())
        else:
            if int(data) == id:
                lider = True
                print(f"Processo {id} é o líder {lider}!")

            if int(data) > id:
                participante = True
                # Forward the message to the next server in the ring
                mandar_mensagem(endereco_prox_servidor, data.encode())
            
            if int(data) < id and participante == False:
                data = f'{id}'
                mandar_mensagem(endereco_prox_servidor, data.encode())
            
        
        time.sleep(5)

        

        # Fecha a conexão atual
        conn.close()

def mandar_mensagem(endereco_destino, mensagem):
    # Cria um socket com uma conexão ao próximo server no anel
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(endereco_destino)

        # Manda mensagem para o próximo server
        client_socket.sendall(mensagem)

def main():
    # Endereço dos servidores no anel
    enderecos_servers = [('localhost', 5000), ('localhost', 5001), ('localhost', 5002), ('localhost', 5003), ('localhost', 5004), ('localhost', 5005), ('localhost', 5006)]

    # Inicia uma thread pra cada server
    threads = []
    for i in range(len(enderecos_servers)):
        endereco_prox_servidor = enderecos_servers[(i + 1) % len(enderecos_servers)]
        thread = threading.Thread(target=server, args=(i + 1, enderecos_servers[i], endereco_prox_servidor))
        threads.append(thread)
        thread.start()

    # Manda mensagem de eleicao pra iniciar o processo
    mensagem_eleicao = "ELEICAO"
    mandar_mensagem(enderecos_servers[0], mensagem_eleicao.encode())

    # espera todas as threads terminarem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()