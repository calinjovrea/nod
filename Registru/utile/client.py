import json
import socket
import tkinter as tk
import time

from tkinter import ttk

from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.portofel import Portofel
from Registru.portofel.mină import Mină
from Registru.sistem import Registrul
from Registru.bloc import Bloc

from Registru.utile.server import Server

class Client():

    def __init__(self, ip, port, registru, mină):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.registru = registru
        self.mină = mină

    def startP2P(self):
        self.p2p = Server(self.ip, self.port, self.registru, self.mină)
        self.p2p.startSocketCommunication()

    def transmite_bloc(self, bloc):
        print('------------ SE TRANSMITE BLOCUL')
        self.p2p.node_message(self.p2p, self.p2p.blocMessage(self.p2p, bloc))

    def transmite_tranzacție(self, tranzacție):
        self.p2p.node_message(self.p2p, self.p2p.tranzacțieMessage(self.p2p, tranzacție))

class Message():
    def __init__(self, senderConnector, messageType, data):
        self.senderConnector = senderConnector
        self.messageType = messageType
        self.data = data


# def ask_blockchain():
#     pass
#     # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # server.connect((HOST,PORT))
#     # server.send("BLOC".encode('utf-8'))
#     # registru = Registrul.din_json(json.loads(server.recv(4096).decode('utf-8')))
#     # # print(registru)
#     # server.close()
#     # return registru

#     # server.close()

# def ask_mină():
#     pass
#     # try:
#     #     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     #     # print('SOCKET OPEN')
#     #     server.connect((HOST,PORT))
#     #     # print('SOCKET PORT OPEN')
#     #     server.send("MINA".encode('utf-8'))
#     #     print(server.recv(4096).decode('utf-8'))
#     # except Exception as e:
#     #     print(e)


# def ask_tranzaction():
#     pass
#     # try:
#     #     portofel = Portofel()
#     #     portofel.registru = ask_blockchain()

#     #     time.sleep(5)
        
#     #     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     #     print('SOCKET OPEN')
#     #     server.connect((HOST,PORT))
#     #     print('SOCKET PORT OPEN')
#     #     server.send("TRANSACTION".encode('utf-8'))
#     #     print('SOCKET TRANSACTION ORDER')
#     #     print(json.dumps(Tranzacție(portofel,'beneficiar', 123).to_json()))
#     #     server.send(json.dumps(Tranzacție(portofel,'beneficiar', 123).to_json()).encode('utf-8'))
#     #     print('SOCKET TRANSACTION SENT')
#     #     print(server.recv(4096).decode('utf-8'))
#     #     server.close()
#     # except Exception as e:
#     #     print(e)

# root = tk.Tk()
# ttk.Label(root, text="NODE", padding=(30,10)).pack()
# #greet_button = ttk.Button(root, text='Receive Blockchain !', command=ask_blockchain).pack()
# #greet_button = ttk.Button(root, text='Mină !', command=ask_mină).pack()
# #greet_button = ttk.Button(root, text='Put Transaction !', command=ask_tranzaction).pack()

# root.mainloop()