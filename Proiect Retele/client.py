import socket
import threading
import pickle
import subprocess

class ClientProcesare:
    def __init__(self, server_gazda='localhost', server_port=12345, client_port=55555):
        self.adresa_server = (server_gazda, server_port)
        self.adresa_client = ('localhost', client_port)
        self.inregistrat = False

    def inregistreaza_la_server(self):
        if not self.inregistrat:
            mesaj = {
                'tip': 'inregistrare',
                'adresa': self.adresa_client[0],
                'port': self.adresa_client[1]
            }
            self.trimite_mesaj_la_server(mesaj)
            self.inregistrat = True
            print("Client înregistrat la server.")
        else:
            print("Clientul este deja înregistrat la server.")

    def deconectare_la_server(self):
        if self.inregistrat:
            mesaj = {
                'tip': 'deconectare',
                'adresa': self.adresa_client[0],
                'port': self.adresa_client[1]
            }
            self.trimite_mesaj_la_server(mesaj)
            self.inregistrat = False
            print("Client deconectat de la server.")
        else:
            print("Clientul nu este înregistrat la server.")

    def trimite_mesaj_la_server(self, mesaj):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect(self.adresa_server)
                server_socket.sendall(pickle.dumps(mesaj))
        except Exception as e:
            print(f"Eroare la comunicarea cu serverul: {e}")

    def trimite_task_la_server(self, task, args):
        if self.inregistrat:
            mesaj = {
                'tip': 'procesare',
                'task': task,
                'args': args
            }
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                    server_socket.connect(self.adresa_server)
                    server_socket.sendall(pickle.dumps(mesaj))
                    response = pickle.loads(server_socket.recv(4096))
                    if response['status'] == 'completat':
                        print(f"Rezultatul task-ului: {response['rezultat']}")
                    else:
                        print("Task-ul este în curs de procesare.")
            except Exception as e:
                print(f"Eroare la trimiterea task-ului către server: {e}")
        else:
            print("Clientul nu este înregistrat la server. Înregistrați-vă mai întâi.")

    def asteapta_cereri_procesare(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.adresa_client)
        server_socket.listen(5)
        print(f"Aștept cereri de procesare pe {self.adresa_client}")

        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=self.gestioneaza_task, args=(client_socket,)).start()

    def gestioneaza_task(self, client_socket):
        try:
            data = client_socket.recv(4096)
            mesaj = pickle.loads(data)
            task = mesaj['task']
            args = mesaj['args']

            exit_code = self.executa_task(task, args)
            client_socket.sendall(pickle.dumps({'exit_code': exit_code}))

        except Exception as e:
            print(f"Eroare la procesarea task-ului: {e}")
        finally:
            client_socket.close()

    def executa_task(self, task, args):
        try:
            process = subprocess.run([task] + args, capture_output=True, text=True)
            print(f"Rezultatul task-ului: {process.stdout}")
            return process.returncode
        except Exception as e:
            print(f"Incheiere task!")
            #print(f"Eroare task: + {e}")
            return -1

    def porneste(self):
        threading.Thread(target=self.asteapta_cereri_procesare).start()
        while True:
            comanda = input("Introduceți comanda (inregistreaza, trimite_task, iesire): ").strip().lower()
            if comanda == 'inregistreaza':
                self.inregistreaza_la_server()
            elif comanda == 'trimite_task':
                task = input("Introduceți comanda pentru task: ").strip()
                args = input("Introduceți argumentele pentru task (separate prin spațiu): ").strip().split()
                self.trimite_task_la_server(task, args)
            elif comanda == 'iesire':
                if self.inregistrat:
                    self.deconectare_la_server()
                print("Client închis.")
                break
            else:
                print("Comandă necunoscută. Încercați din nou.")

if __name__ == "__main__":

    port_client = 55555
    client = ClientProcesare(client_port=port_client)
    client.porneste()