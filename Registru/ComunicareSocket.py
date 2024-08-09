from p2pnetwork.node import Node

class ComunicareSocket(Node):

    def __init__(self, ip, port):
        super(ComunicareSocket, self).__init__(ip, port, None)
    
    def startSocket(self):
        self.start()

    def inbound_node_connected(self, connected_node):
        print('inbound connection')
        self.send_to_node(connected_node, 'Hi, I am Straight !')

    def outbound_node_connected(self, connected_node):
        print('outbound connection')
        self.send_to_node(connected_node, 'Hi, I am the node that initialized the connection !')
    
    def node_message(self, connected_node, message):
        print(message)