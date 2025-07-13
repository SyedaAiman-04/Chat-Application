import socket
import threading
import sys

def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
    except:
        print("\nDisconnected from server")
    finally:
        client_socket.close()
        sys.exit(0)

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 5555))
    except ConnectionRefusedError:
        print("Could not connect to server. Is it running?")
        return

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client,),
        daemon=True
    )
    receive_thread.start()

    print("Connected to chat server. Type your messages (Ctrl+C to quit):")
    
    try:
        while True:
            message = input()
            try:
                client.send(message.encode('utf-8'))
            except:
                print("Failed to send message")
                break
    except KeyboardInterrupt:
        print("\nClosing connection...")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()