import json
import time


from Registru.utile.algoritm_hash import creează_hash
from Registru.utile.hex_binar import hex_binar
from Registru.configurare import RATA

INFORMAȚII_GENESIS = {
    'dată': 1,
    'ultimul_hash': 'ultimul_hash_geneză',
    'hash': 'hash_geneză',
    'informații':[],
    'dificultate': 3,
    'nonce': 'nonce-geneză'
}
class Bloc:
    """
    Bloc: o unitate de stocare.
    Stochează tranzacții într-un registru care suportă o cryptomonedă.
    """
    def __init__(self,dată, ultimul_hash, hash, informații, dificultate, nonce):
        self.dată = dată
        self.ultimul_hash = ultimul_hash
        self.hash = hash
        self.informații = informații
        self.dificultate = dificultate
        self.nonce = nonce

    def __repr__(self):
        return ( 
            'Bloc('
            f'dată: {self.dată}, '
            f'ultimul_hash: {self.ultimul_hash}, '
            f'hash: {self.hash}, '
            f'informații: {self.informații}, '
            f'dificultate: {self.dificultate}, '
            f'nonce: {self.nonce})'
        )

    def __eq__(self,other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        return self.__dict__

    def din_json(bloc_json):
        return Bloc(**bloc_json)

    @staticmethod
    def minează_bloc(ultimul_bloc, informații):

        """
        Minează un Bloc bazat pe ultimul bloc și data, pâmă când un hash este găsit conform cerințelor de 0-uri .
        """
        dată = time.time_ns()
        
        ultimul_hash = ultimul_bloc.hash
        dificultate = Bloc.adjustă_dificultatea(ultimul_bloc, dată)
        nonce = 0
        hash = creează_hash(dată,ultimul_hash,informații, dificultate, nonce)

        while hex_binar(hash)[0:dificultate] != '0' * dificultate:
            nonce += 1
            dată = time.time_ns()
            hash = creează_hash(dată,ultimul_hash,informații, dificultate, nonce)

        #return  Bloc(dată,ultimul_hash,hash,informații, dificultate, nonce)
        return  Bloc(dată,ultimul_hash,hash,informații, dificultate, nonce)

    @staticmethod
    def geneză():
        """
        Creaază Blocul Geneză.
        """

        # return  Bloc(INFORMAȚII_GENESIS['dată'],INFORMAȚII_GENESIS['ultimul_hash'], INFORMAȚII_GENESIS['hash'], INFORMAȚII_GENESIS['informații'])
        return Bloc(**INFORMAȚII_GENESIS)

    @staticmethod
    def adjustă_dificultatea(ultimul_bloc, nouă_dată):
        """
        Calculează noua dificultate in funcție de RATĂ
        """
        if (nouă_dată - ultimul_bloc.dată) < RATA:
            return ultimul_bloc.dificultate + 1

        if (ultimul_bloc.dificultate -1) > 0:
            return ultimul_bloc.dificultate - 1 

        return 1

    @staticmethod
    def e_valid_blocul(ultimul_bloc,bloc):
        """
        Validează blocurile după următoarele reguli:
        - Blocul trebuie să respecte ultimul hash cum trebuie
        - Blocul trebuie să respecte validitatea algoritmului de muncă
        - Blocul trebuie să se adjusteze doar cu câte o unitate
        - Blocul trebuie să aibe informațiile utile corecte
        """

        if ( bloc.ultimul_hash != ultimul_bloc.hash ):
            print(bloc.ultimul_hash, ultimul_bloc.hash)
            raise Exception('Ultimul hash a blocului trebuie să fie corect !')

        if hex_binar(bloc.hash)[0:bloc.dificultate] != '0' * bloc.dificultate:
            raise Exception('Algoritmul de muncă nu a dat rezultatul corect !')

        if abs(ultimul_bloc.dificultate - bloc.dificultate) > 1:
            raise Exception('Dificultatea trebuie să se adjusteze doar cu 1 !')

        hash_reconstruit = creează_hash(
            bloc.dată,
            bloc.ultimul_hash,
            bloc.informații,
            bloc.dificultate,
            bloc.nonce
        )

        if bloc.hash != hash_reconstruit:
            raise Exception('Hash-ul blocului trebuie să fie corect !')
def main():

    #geneză = Bloc.geneză()
    #bloc_greșit = Bloc.minează_bloc(Bloc.geneză(), 'foo')
    #bloc_greșit.ultimul_hash = 'greșit'
    #bloc_greșit.dificultate = -2

    ##try:
    #    Bloc.e_valid_blocul(geneză,bloc_greșit)
    #except Exception as e:
    #    print(f'e_valid_blocul: {e}')
    pass
if __name__ == '__main__':
    main()