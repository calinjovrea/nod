import json
import socket
import requests

from p2pnetwork.node import Node

from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.portofel import Portofel
from Registru.portofel.mină import Mină
from Registru.sistem import Registrul
from Registru.bloc import Bloc

from Registru.utile.peer_discovery import PeerDiscoveryHandler
from Registru.utile.socket_connector import SocketConnector


CANALE = {
    'TEST':'TEST',
    'BLOC':'BLOC',
    'TRANZACȚIE': 'TRANZACȚIE',
    'BULK': 'BULK',
    'REGISTRU': 'REGISTRU',
    'MINA': 'MINA'
}

class Server(Node):
    def __init__(self, ip, port, registru, mină):
        super(Server, self).__init__(ip,port, None)
        self.peers = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)
        self.registru = registru
        self.mină = mină
    
    def connectToFirstNode(self):
        if self.socketConnector.port != 40000:
            self.connect_with_node('localhost', 40000)
        
    def startSocketCommunication(self):
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()
    
    def inbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    def blocMessage(self, connected_node, bloc):
        print('------------ CONECTAT LA NOD')
        return self.peerDiscoveryHandler.Bloc(connected_node, bloc)

    def tranzacțieMessage(self, connected_node, tranzacție):
        return self.peerDiscoveryHandler.Tranzacție(connected_node, tranzacție)

    def node_message(self, connected_node, message):
        import ast

        messages = ast.literal_eval(message)

        if messages['messageType'] == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(messages)
        if messages['messageType'] == 'BLOC':
        
            listă = self.registru.listă
            print(listă)
            print('////////////////@@@@@@@@@')
            #listă.append(Bloc.din_json(messages['data']))
            print(listă)
            print('////////////////')
            try:
                print(self.registru.to_json())
                # self.registru.înlocuiește_listă(listă)
                self.registru.e_validă_lista(listă)
                self.mină.clarifică_registru_tranzacții(self.registru)

                print('\n -- Lista a fost validată cu success !')
            except Exception as e:
                print(e)
                print(f'\n Lista nu a fost înlocuită !')

        if messages['messageType'] == 'TRANZACȚIE':
            tranzacție = Tranzacție.din_json(messages['data'])
            self.mină.pune_tranzacția(tranzacție)

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)
    # def trimite_tranzacție(self,plătitor,beneficiar,sumă):

    #     plătitor.cheie_privată = []

    #     if plătitor.registru:
    #         try:
    #             plătitor.registru = plătitor.registru.to_json()
    #         except Exception as e:
    #             plătitor.registru = plătitor.registru

    #     return requests.post(f'{URL}/portofel/trimite',
    #     json={'plătitor': plătitor.to_json(),'beneficiar': beneficiar, 'sumă': sumă}).json()
    # def ascultare(self):
    #     self.server.listen()
    #     while True:

    #         communication_socket, address = self.server.accept()
    #         print(f'Connected to {address}')
            
    #         # mesaj = communication_socket.recv(4096).decode('utf-8')

    #         if mesaj == CANALE['BLOC']:

    #             try:
    #                 self.registru.e_validă_lista(self.registru.listă)
    #                 self.mină.clarifică_registru_tranzacții(self.registru)
    #                 # communication_socket.send(json.dumps(self.registru.to_json()).encode('utf-8'))
    #                 print('\n -- Lista a fost validată cu success !')
    #             except Exception as e:
    #                 print(e)
    #                 print(f'\n Lista nu a fost înlocuită !')
    #         elif mesaj == CANALE['MINA']:

    #             communication_socket.send(json.dumps(self.mină.to_json()).encode('utf-8'))

    #         elif mesaj == CANALE['TRANSACTION']:
    #             tranzacție = json.loads(communication_socket.recv(4096).decode('utf-8'))
    #             # print(tranzacție)
    #             try:
    #                 tranzacție = Tranzacție.din_json(tranzacție)

    #                 self.mină.pune_tranzacția(tranzacție)

    #                 communication_socket.send(json.dumps(self.mină.to_json()).encode('utf-8'))
                    
    #                 if self.mină.e_necesar_îndeplinitor():
    #                     print('BLOCK AVAILABLE !')
    #             except Exception as e:
    #                 print(e)

    #         # print(f'Message From Client {mesaj}')
    #         # send_blockchain(communication_socket)
    #         communication_socket.close()
    #         print(f'Communication with {address} ended!')
