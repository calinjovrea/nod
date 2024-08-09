import Registru.bloc as bloc

from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.portofel import Portofel
from Registru.consensus.consensus import Consensus
from Registru.configurare import RĂSPLĂTIRE, RĂSPLĂTIRE_ 

from Registru.utile.algoritm_hash import creează_hash
class Registrul:

    """
    Registrul: un public registru de tranzacții.
    Implementat ca o listă de blocuri - seturi de date a tranzacțiilor
    """

    def __init__(self, ):
        self.listă = [bloc.Bloc.geneză()]
        self.consensus = Consensus()

    def adaugă_bloc(self,informații):
        self.listă.append(bloc.Bloc.minează_bloc(self.listă[len(self.listă)-1],informații))

    def __repr__(self):
        return f'Registru: {self.listă}'

    def to_json(self):
        return [w.to_json() for w in self.listă]

    def înlocuiește_listă(self,lista):
        """
        Înlocuiește lista locală cu cea care vine dacă următoarele se aplică:
        - Lista care vine este mai lungă decât cea curentă.
        - Lista este formatată corect.
        """

        if len(lista) <= len(self.listă):
            raise Exception('Nu se poate înlocui')

        try:
            self.e_validă_lista(lista)
        except Exception:
            raise Exception(f'Nu se poate înlocui. lista ce vine este invalidă')

        self.listă = lista

    @staticmethod
    def din_json(listă_json):
        """
        Deserializează o listă de blocuri serializate într-un registru.
        Rezultatul va conține o listă  de blocuri.
        """

        registru = Registrul()
        
        registru.listă = list(map(lambda bloc_json: bloc.Bloc.din_json(bloc_json), listă_json))

        return registru

    @staticmethod
    def e_validă_lista(listă):

        """
        Validează lista
        """

        if listă[0] != bloc.Bloc.geneză():
            raise Exception('Blocul geneză trebuie să fie valid !')

        for curent_bloc in range(1, len(listă)):
            iterare_bloc = listă[curent_bloc]
            iterare_ultimul_bloc = listă[curent_bloc-1]

            try:
                bloc.Bloc.e_valid_blocul(iterare_ultimul_bloc,iterare_bloc)
            except Exception as e:
                print(e)

        try:
            Registrul.e_validă_lista_tranzacțiilor(listă)
        except Exception as e:
            print(e)
            print('----------????????????????/')
    @staticmethod
    def e_validă_lista_tranzacțiilor(listă):

        """
        Verifică regulile unei liste compusă din blocuri de tranzacții
            - Fiecare tranzacție trebuie să apară doar odată în listă
            - Trebuie să existe doar o singură răsplătire pentru fiecare bloc
            - Fiecare tranzacție trebuie să fie validă
        """
        identificatori_tranzacții = set()

        for i in range(len(listă)):
            bloc = listă[i]
            are_răsplătire = False

            for tranzacție_json_info in bloc.informații:

                if type(tranzacție_json_info) == list:
                    for tranzacție_json in tranzacție_json_info:

                        if 'id' in tranzacție_json: 
                            tranzacție = Tranzacție.din_json(tranzacție_json)
                            
                            if tranzacție.id in identificatori_tranzacții:
                                raise Exception(f'Tranzacția nu este unică !')

                            identificatori_tranzacții.add(tranzacție.id)

                            if tranzacție.intrare == RĂSPLĂTIRE_:
                                if are_răsplătire:
                                    raise Exception('Trebuie să existe doar o singură răsplătire !'\
                                    f'Verifică blocul cu hash-ul: {bloc.hash}')
                                are_răsplătire = True
                            else:
                                registru_historic = Registrul()
                                registru_historic.listă = listă[0:i]
                                sumă_historică = Portofel.calculează_total(
                                    registru_historic,
                                    tranzacție.intrare['adresă']
                                )

                                if sumă_historică != tranzacție.intrare['sumă']:
                                    raise Exception(f'Tranzacție {tranzacție.id} are o sumă în intrare invalidă !')


                            Tranzacție.e_validă_tranzacția(tranzacție)
                elif 'id' in tranzacție_json_info:
                    tranzacție_json = tranzacție_json_info

                    tranzacție = Tranzacție.din_json(tranzacție_json)

                   
                    if tranzacție.id in identificatori_tranzacții:
                        raise Exception(f'Tranzacția nu este unică !')

                    identificatori_tranzacții.add(tranzacție.id)


                    if tranzacție.intrare == RĂSPLĂTIRE_:
                        if are_răsplătire:
                            raise Exception('Trebuie să existe doar o singură răsplătire !'\
                            f'Verifică blocul cu hash-ul: {bloc.hash}')
                        are_răsplătire = True
                    else:
                        registru_historic = Registrul()
                        registru_historic.listă = listă[0:i]
                        sumă_historică = Portofel.calculează_total(
                            registru_historic,
                            tranzacție.intrare['adresă']
                        )

                        if sumă_historică != tranzacție.intrare['sumă']:
                            raise Exception(f'Tranzacție {tranzacție.id} are o sumă în intrare invalidă !')

                    Tranzacție.e_validă_tranzacția(tranzacție)


    def următor_îndeplinitor(self):
        ultimul_bloc_hash = creează_hash(self.listă[-1].hash)
        îndeplinitor = self.consensus.îndeplinitor(ultimul_bloc_hash)        
        return îndeplinitor

def main():
    pass
    # registru = Registrul()
    # registru.adaugă_bloc('1')
    # registru.adaugă_bloc('2')

    # print(registru)

if __name__ == '__main__':
    main()

