import socket
import threading

def handle_client(client_socket, addr, clients):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            print(f"Message from {addr}: {message}")
            
            # Broadcast to all other clients
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(f"{addr}: {message}".encode('utf-8'))
                    except:
                        clients.remove(client)
        except:
            clients.remove(client_socket)
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen()
    print("Server started, waiting for connections...")
    
    clients = []
    
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Connection from {addr} established")
        
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, addr, clients)
        )
        thread.start()

if __name__ == "__main__":
    start_server()