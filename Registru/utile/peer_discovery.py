import threading
import time

from Registru.portofel.tranzacție import Tranzacție

class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socketCommunication = node
    
    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=())
        discoveryThread.start()
    
    def status(self):
        while True:
            print('Current Connections:')
            for peer in self.socketCommunication.peers:
                peer = Peer('obiect', peer['ip'], peer['port'])
                print(str(peer.ip) + ':' + str(peer.port))
            time.sleep(10)

    def discovery(self):
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    def handshake(self, connect_node):
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connect_node, handshakeMessage)

    def Bloc(self, connect_node, bloc):
        print('--------- SE FABRICA MESAJUL')
        return self.BlocMessage(bloc)
        #self.socketCommunication.send(connect_node, blocMessage)

    def Tranzacție(self, connect_node, tranzacție):
        return self.TranzacțieMessage(tranzacție)

    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data = ownPeers
        messageType = 'DISCOVERY'
        return str({'obiect': 'Message.Message', 'senderConnector': {'obiect': 'SocketConnector.SocketConnector', 'ip':ownConnector.ip, 'port':ownConnector.port}, 'messageType': messageType, 'data':data})

    def handleMessage(self, message):

        peersSocketConnector = message['senderConnector']

        peersPeerList = message['data']
        newPeer = True

        for peer in self.socketCommunication.peers:
            peer = Peer('obiect', peer['ip'], peer['port'])
            if peer.equals(Peer('obiect', peersSocketConnector['ip'], peersSocketConnector['port'])):
                newPeer = False
        if newPeer == True:
            self.socketCommunication.peers.append(peersSocketConnector)

        for peersPeer in peersPeerList:
            peerKnown = False
            peersPeer = Peer('obiect',peersPeer['ip'],peersPeer['port'])
            for peer in self.socketCommunication.peers:
                peer = Peer('obiect',peer['ip'],peer['port'])
                if peer.equals(Peer('obiect', peersPeer.ip, peersPeer.port)):
                    peerKnown = True
            
            comm = self.socketCommunication.socketConnector
            if not peerKnown and not peersPeer.equals(Peer('obiect', comm.ip, comm.port)):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)

    def BlocMessage(self, bloc):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        messageType = 'BLOC'
        return str({'obiect': 'Message.Message', 'senderConnector': {'obiect': 'SocketConnector.SocketConnector', 'ip':ownConnector.ip, 'port':ownConnector.port}, 'messageType': messageType, 'data': bloc})

    def TranzacțieMessage(self, tranzacție):
        
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        messageType = 'TRANZACȚIE'
        return str({'obiect': 'Message.Message', 'senderConnector': {'obiect': 'SocketConnector.SocketConnector', 'ip':ownConnector.ip, 'port':ownConnector.port}, 'messageType': messageType, 'data': tranzacție})


        
class Peer():
    def __init__(self, obiect, ip, port):
        self.obiect = obiect
        self.ip = ip
        self.port = port

    def equals(self,peer):
        if self.obiect == peer.obiect and self.ip == peer.ip and self.port == peer.port:
            return True

        return False

        
