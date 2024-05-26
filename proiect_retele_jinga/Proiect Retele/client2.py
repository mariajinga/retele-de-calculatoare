import socket
import subprocess

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

CLIENT_PORT = 55555  # Portul pe care clientul ascultă pentru cereri de procesare

def register_with_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.sendall(b"REGISTER")
        response = client_socket.recv(1024)
        print(response.decode())

def send_task_command_to_server(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        task_message = f"TASK {command}"
        client_socket.sendall(task_message.encode())
        exit_code = client_socket.recv(1024).decode()
        print(f"Task executed with exit code: {exit_code}")

def unregister_from_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.sendall(b"UNREGISTER")


# Înregistrare cu server-ul
register_with_server()

# Trimitere comandă TASK către server
task_command = "python3 -c 'print(\"A mers\")'"
send_task_command_to_server(task_command)

# Dezregistrare de la server
unregister_from_server()
