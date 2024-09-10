import json
import socket
import requests

from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.portofel import Portofel
from Registru.portofel.mină import Mină
from Registru.sistem import Registrul
from Registru.bloc import Bloc

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

CANALE = {
    'TEST':'TEST',
    'BLOC':'BLOC',
    'TRANSACTION': 'TRANSACTION',
    'BULK': 'BULK',
    'REGISTRU': 'REGISTRU'
}

class Canal():
    def __init__(self, registru, mină):
        self.registru = registru
        self.mină = mină

while True:

    communication_socket, address = server.accept()
    print(f'Connected to {address}')

    registru = Registrul()
    mină = Mină()
    
    mesaj = communication_socket.recv(4096).decode('utf-8')

    if mesaj == CANALE['BLOC']:
            rezultat = requests.get(f'http://localhost:5000/registru')

            rezultat_json = rezultat.json()
            print(rezultat_json)
            rezultat_registru = registru.din_json(rezultat_json)

            try:    
                registru.e_validă_lista(listă)
                mină.clarifică_registru_tranzacții(registru)
                socket.send(json.dumps(registru.to_json()).encode('utf-8'))
                print('\n -- Lista a fost validată cu success !')
            except Exception as e:
                print(e)
                print(f'\n Lista nu a fost înlocuită !')

    elif mesaj == CANALE['TRANSACTION']:
        tranzacție = Tranzacție.din_json(communication_socket.recv(4096).decode('utf-8'))
        mină.pune_tranzacția(tranzacție)
        socket.send(json.dumps(mină.to_json()).encode('utf-8'))
            
    # print(f'Message From Client {mesaj}')
    # send_blockchain(communication_socket)
    communication_socket.close()
    print(f'Communication with {address} ended!')
    server.close()
