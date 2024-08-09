import time

from Registru.sistem import Registrul
from Registru.bloc import Bloc
from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.mină import Mină

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-f13bc8f3-1207-49be-a62e-2e00084894cc'
pnconfig.publish_key = 'pub-c-d84002ba-b98d-42c0-a056-1e26a982ae49'
pubnub = PubNub(pnconfig)

CANALE = {
    'TEST':'TEST',
    'BLOC':'BLOC',
    'TRANSACTION': 'TRANSACTION',
    'BULK': 'BULK'
}

# pubnub.subscribe().channels([sistem]).execute()


class Listener(SubscribeCallback):
    def __init__(self,registru, mină):
        self.registru = registru
        self.mină = mină

    def message(self, pubnub, mesaj):
        # if mesaj.channel == CANALE['BLOC']:
            # print(f'\n-- Channel: {mesaj.channel} | Message: {mesaj.message}')

        if mesaj.channel == CANALE['BLOC']:
            # bloc = Bloc.din_json(mesaj.message)
            listă = self.registru.listă[:]
            try:
                self.registru.e_validă_lista(listă)
                self.mină.clarifică_registru_tranzacții(self.registru)

                print('\n -- Lista a fost validată cu success !')
            except Exception as e:
                print(e)
                print(f'\n Lista nu a fost înlocuită !')

        elif mesaj.channel == CANALE['TRANSACTION']:
            tranzacție = Tranzacție.din_json(mesaj.message)
            self.mină.pune_tranzacția(tranzacție)
            # print('Tranzacția a fost adăugată !')
        elif mesaj.channel == CANALE['BULK']:
            [self.mină.pune_tranzacția(Tranzacție.din_json(tranzacție)) for tranzacție in mesaj.message['tranzacții']]
            print('Bulk Efectuat !')
        elif mesaj.channel == CANALE['REGISTRU']:
            rezultat = requests.get(f'https://fe60-82-77-240-24.ngrok-free.app/registru')

            rezultat_registru = self.registru.din_json(rezultat.json())

            try:
                self.registru.înlocuiește_listă(rezultat_registru.listă)
                self.registru.e_validă_lista(rezultat_registru.listă)
                print('\nRegistrul s-a sincronizat !')
            except Exception as e:
                print(f'\nRegistrul nu s-a sincronizat, eroare {e}')
            

class PubSub():
    """
    Administrează stratul de publicare sau abonare a aplicației
    Pune la dispoziție comunicare între nodurile unui sistem independent financiar.
    """
    def __init__(self, registru, mină):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CANALE.values()).execute()
        self.pubnub.add_listener(Listener(registru, mină))

    def publish(self, channel, message):
        """
        Publicare a mesajului obiect către canal.
        """
        pubnub.publish().channel(channel).message(message).sync()


    def transmite_bloc(self,bloc):
        """
        Transmite un bloc în toate nodurile
        """
        self.publish(CANALE['BLOC'], bloc.to_json())

    def transmite_bulk(self, bulk):
        self.publish(CANALE['BULK'], bulk)

    def transmitere_tranzacție(self, transacție):
        """
        Transmitere a unui bloc obiect către toate nodurile
        """

        self.publish(CANALE['TRANSACTION'],transacție.to_json())

    def transmitere_registru(self):
        self.publish(CANALE['REGISTRU'],'REGISTRU')

def main():
    pass
    #registru = Registrul()
    #mină = Mină()

    #pubsub = PubSub(registru, mină)
    #time.sleep(1)
    #pubsub.publish(CANALE['TEST'], {'foo':'bar'})



if __name__ == '__main__':
    main()