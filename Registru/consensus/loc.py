

from Registru.utile.algoritm_hash import creează_hash

class Loc():

    def __init__(self,cheie_publică, iterații, ultimul_bloc_hash):
        self.cheie_publică = cheie_publică
        self.iterații = iterații
        self.ultimul_bloc_hash = ultimul_bloc_hash

    def hashLoc(self):
        informații = self.cheie_publică + self.ultimul_bloc_hash
        for _ in range(self.iterații):
            informații = creează_hash(informații)
        return informații
