import socket
import threading
import pickle

class ServerProcesare:
    def __init__(self, gazda='localhost', port=12345):
        self.adresa_server = (gazda, port)
        self.clienti = []
        self.index_curent = 0
        self.lock = threading.Lock()

    def porneste_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.adresa_server)
        server_socket.listen(5)
        print(f"Serverul a pornit pe {self.adresa_server}")

        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=self.gestioneaza_client, args=(client_socket,)).start()

    def gestioneaza_client(self, client_socket):
        try:
            data = client_socket.recv(4096)
            mesaj = pickle.loads(data)
            print(f"Mesaj primit de la client: {mesaj}")

            if mesaj['tip'] == 'inregistrare':
                with self.lock:
                    self.clienti.append((mesaj['adresa'], mesaj['port']))
                    print(f"Client înregistrat: {mesaj['adresa']}:{mesaj['port']}")

            elif mesaj['tip'] == 'procesare':
                task = mesaj['task']
                args = mesaj['args']
                with self.lock:
                    if not self.clienti:
                        print("Nu sunt clienți disponibili pentru a procesa task-ul")
                        return

                    client = self.clienti[self.index_curent]
                    self.index_curent = (self.index_curent + 1) % len(self.clienti)

                print(f"Trimit task-ul la client: {client}")
                threading.Thread(target=self.trimite_task_la_client, args=(client, task, args, client_socket)).start()

            elif mesaj['tip'] == 'deconectare':
                with self.lock:
                    self.clienti.remove((mesaj['adresa'], mesaj['port']))
                    print(f"Client deconectat: {mesaj['adresa']}:{mesaj['port']}")

        except Exception as e:
            print(f"Eroare la gestionarea clientului: {e}")
        finally:
            client_socket.close()

    def trimite_task_la_client(self, client, task, args, response_socket):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(client)

            print(f"Trimit task: {task} cu argumente: {args} la client: {client}")
            client_socket.sendall(pickle.dumps({'task': task, 'args': args}))
            data = b""
            data += client_socket.recv(4096)
            rezultat = pickle.loads(data)

            client_socket.sendall(pickle.dumps({'status': 'completat', 'rezultat': rezultat}))
        except Exception as e:
            print(f"Eroare la trimiterea task-ului către client: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = ServerProcesare()
    server.porneste_server()
