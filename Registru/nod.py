
from Registru.portofel.portofel import Portofel
from Registru.portofel.mină import Mină
from Registru.sistem import Registrul
from Registru.ComunicareSocket import ComunicareSocket

class Nod():

    def __init__(self, ip, port):

        self.p2p = None
        self.ip = ip
        self.port = port

        self.mină = Mină()
        self.portofel = Portofel()
        self.registru = Registrul()

    def startP2P(self):
        self.p2p = ComunicareSocket(self.ip, self.port)
        self.p2p.startSocket()   