import socket
import subprocess
import threading
HOST = '127.0.0.1'
PORT = 12345

active_clients = []
task_queue = []

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    while True:
        # Receiving commands from the client
        command = client_socket.recv(1024).decode()
        print(command)
        if not command:
            break
        # The command can be of the form "REGISTER", "TASK task_code arg1 arg2 ...", or "UNREGISTER"
        command_parts = command.split()
        if command_parts[0] == "REGISTER":
            active_clients.append(client_socket)
            client_socket.sendall(b"REGISTERED")
        elif command_parts[0] == "TASK":
            # Extract the task code and arguments
            task_code = command_parts[1]
            task_args = command_parts[2:]
            task_queue.append((task_code, task_args, client_socket))
        elif command_parts[0] == "UNREGISTER":
            #active_clients.remove(client_socket)
            client_socket.sendall(b"UNREGISTERED")
            client_socket.close()
            break

def listen_for_clients():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server is listening on {HOST}:{PORT}")
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()

def process_tasks():
    while True:
        if task_queue:
            task_code, task_args, client_socket = task_queue.pop(0)
            try:
                # Execute the task using subprocess.run()
                result = subprocess.run([task_code] + task_args, capture_output=True)
                print("Task executed successfully")
                exit_code = result.returncode
                print(f"Exit code: {exit_code}")
            except Exception as e:
                print(f"Error executing task: {e}")
                exit_code = -1
            client_socket.sendall(str(exit_code).encode())

client_listener_thread = threading.Thread(target=listen_for_clients)
client_listener_thread.start()

task_processor_thread = threading.Thread(target=process_tasks)
task_processor_thread.start()

# Wait for all threads to finish before the main thread exits
client_listener_thread.join()
task_processor_thread.join()