from Registru.consensus.loc import Loc
from Registru.portofel.portofel import Portofel

from Registru.utile.algoritm_hash import creează_hash

class Consensus():

    def __init__(self):
        self.colaboratori = {}
        self.puneNodGeneză()

    def puneNodGeneză(self):
        cheie_geneză_privată = Portofel.din_cheie(Portofel,f"C:\\Users\\jovre\\Documents\\GitHub\\sistem\\sistem\\Registru\\utile\\chei\\cheie_privată.pem")
        cheie_geneză_publică = cheie_geneză_privată.public_key()
        
        portofel = Portofel()
        portofel.cheie_privată = cheie_geneză_privată
        portofel.cheie_publică = cheie_geneză_publică
        portofel.serializează_cheie_publică()

        self.colaboratori[portofel.cheie_publică] = 1

    def actualizează(self, cheie_publică, sumă):
        if cheie_publică in self.colaboratori.keys():
            self.colaboratori[cheie_publică] += sumă
        else:
            self.colaboratori[cheie_publică] = sumă
    
    def cere(self, cheie_publică):
        if cheie_publică in self.colaboratori.keys():
            return self.colaboratori[cheie_publică]
        else:
            return None

    def validatori_de_loc(self, sămânță):
        locuri = []

        for validator in self.colaboratori.keys():
            for sumă in range(self.cere(validator)):
                locuri.append(Loc(validator, sumă+1, sămânță))
        return locuri

    def locCâștigător(self, locuri, sămânță):
        câștigător=None
        cel_mai_apropiat = None
        referință_hash_int_valoare = int(creează_hash(sămânță),16)
        for loc in locuri:
            lotIntV = int(loc.hashLoc(),16)
            apropiat = abs(lotIntV - referință_hash_int_valoare)
            if cel_mai_apropiat is None or apropiat < cel_mai_apropiat:
                cel_mai_apropiat = apropiat
                câștigător = loc
        
        return câștigător

    def îndeplinitor(self, ultimul_bloc_hash):

        locuri = self.validatori_de_loc(ultimul_bloc_hash)
        câștigător = self.locCâștigător(locuri, ultimul_bloc_hash)
        return câștigător.cheie_publică