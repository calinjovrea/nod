import uuid
import time

from Registru.portofel.portofel import Portofel
from Registru.configurare import RĂSPLĂTIRE, RĂSPLĂTIRE_

class Tranzacție:

    """
    Documentează un schimb de valută 
    de la un plătitor către un beneficiar
    """

    def __init__(self, plătitor=None, beneficiar=None, sumă=None, id=None, ieșire=None, intrare=None):
        self.id = id or str(uuid.uuid4())[0:8]
        self.ieșire = ieșire or self.creează_plată(
            plătitor,
            beneficiar,
            sumă
        )
        self.intrare = intrare or self.creează_intrare(plătitor, self.ieșire)


    def creează_plată(self, plătitor, beneficiar, sumă):

        """
        Structurează afișarea de informații a unei tranzacții
        """

        if sumă > plătitor.sumă:
            raise Exception('Suma este mai mare decât totalul portofelului !')
        afișare = {}
        afișare[beneficiar] = sumă
        afișare[plătitor.adresă] = plătitor.sumă - sumă

        return afișare

    def creează_intrare(self, plătitor, ieșire):

        """
        Structurează informațiile de intrare pentru tranzacție
        Semnează tranzacția incluzând cheia publică a plătitorului
        și adresa
        """

        return {
            'dată': time.time_ns(),
            'sumă': plătitor.sumă,
            'adresă': plătitor.adresă,
            'cheia_publică': plătitor.cheie_publică,
            'semnătura': plătitor.semnează(ieșire)
        }

    def actualizează(self, plătitor, beneficiar, sumă):
        """
        Actualizează tranzacția cu un existent sau nou beneficiar
        """

        if sumă > self.ieșire[plătitor.adresă]:
            raise Exception('Suma este mai mare decât totalul !')

        if beneficiar in self.ieșire:
            self.ieșire[beneficiar] = self.ieșire[beneficiar] + sumă
        else:
            self.ieșire[beneficiar] = sumă 

        self.ieșire[plătitor.adresă] = self.ieșire[plătitor.adresă] - sumă
        self.intrare = self.creează_intrare(plătitor, self.ieșire)

    def to_json(self):
        """
        Serializare a tranzacțiilor
        """

        return self.__dict__

    @staticmethod
    def din_json(tranzacție_json):
        """
        Deserializează o tranzacție json înapoi într-o tranzacție
        """

        return Tranzacție(**tranzacție_json)

    @staticmethod
    def e_validă_tranzacția(tranzacție):
        """
        Validează o tranzacție.
        Ridică o excepție pentru invalidele tranzacții
        """

        if tranzacție.intrare == RĂSPLĂTIRE_:
            if list(tranzacție.ieșire.values()) != [RĂSPLĂTIRE]:
                raise Exception('Răsplătire de miner, invalidă !')
            return

        ieșire_total = sum(tranzacție.ieșire.values())

        if tranzacție.intrare['sumă'] != ieșire_total:
            raise Exception('Tranzacție invalidă valori ieșire')

        if not Portofel.verifică(
            tranzacție.intrare['cheia_publică'],
            tranzacție.ieșire,
            tranzacție.intrare['semnătura']):
            raise Exception('Semnătură Invalidă !')

    
    @staticmethod
    def răsplătește_tranzacție(miner):
        """
        Generează o răsplătire pentru tranzacția minerului.
        """
        ieșire = {}
        ieșire[miner.adresă] = RĂSPLĂTIRE

        return Tranzacție(intrare=RĂSPLĂTIRE_, ieșire=ieșire)

    @staticmethod
    def tranzacție_consensus(miner, sumă):
        """
        Generează o tranzacție consensus.
        """
        ieșire = {}
        ieșire[miner.adresă] -= sumă

        return Tranzacție(intrare=miner.adresă, ieșire=ieșire)

def main():

    #tranzacție = Tranzacție(Portofel(), 'beneficiar', 15)
    #print(f'tranzacție: {tranzacție.__dict__}')

    #tranzacție_json = tranzacție.to_json()
    #restorare_tranzacție = Tranzacție.din_json(tranzacție_json)
    #print(f'json {tranzacție_json} \n restorată {restorare_tranzacție.__dict__}')
    pass
    
if __name__ == '__main__':
    main()



