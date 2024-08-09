import random

from Registru.portofel.portofel import Portofel
from Registru.sistem import Registrul
from Registru.configurare import TOTAL
from Registru.portofel.tranzacție import Tranzacție

def test_verifică_valida_semnătură():
    informații = { 'foo': 'test_data' }
    portofel = Portofel()
    semnătură = portofel.semnează(informații)

    assert Portofel.verifică(portofel.cheie_publică, informații, semnătură)

def test_verifică_invalida_semnătură():
    informații = { 'foo': 'test_data' }
    portofel = Portofel()
    semnătură = portofel.semnează(informații)

    assert not Portofel.verifică(Portofel().cheie_publică, informații, semnătură)


def test_calculează_totalul():
    registru = Registrul()
    portofel = Portofel()
    portofel_2 = Portofel()

    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    assert Portofel.calculează_total(registru, portofel.adresă) == TOTAL

    
    sumă = 50
    transacție = Tranzacție(portofel, 'beneficiar', sumă)
    registru.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue),transacție.to_json()])
    
    print('=========================')
    print(Portofel.calculează_total(registru, portofel.adresă))
    print('=========================')
    assert Portofel.calculează_total(registru, portofel.adresă) == TOTAL - sumă

    sumă_primită_1 = 25

    tranzacție_primită_1 = Tranzacție(
        Portofel(),
        portofel.adresă,
        sumă_primită_1
    )

    sumă_primită_2 = 45
    tranzacție_primită_2 = Tranzacție(
        Portofel(),
        portofel.adresă,
        sumă_primită_2
    )

    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    registru.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue),[tranzacție_primită_1.to_json(),tranzacție_primită_2.to_json()]])

    assert Portofel.calculează_total(registru, portofel.adresă) == TOTAL - sumă + sumă_primită_1 + sumă_primită_2