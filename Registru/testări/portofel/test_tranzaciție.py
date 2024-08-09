import pytest

from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.portofel import Portofel
from Registru.configurare import RĂSPLĂTIRE, RĂSPLĂTIRE_

def test_tranzacție():
    plătitor = Portofel()

    recipient = 'recipient'
    sumă = 50
    tranzacție = Tranzacție(plătitor,recipient,sumă)

    assert tranzacție.ieșire[recipient] == sumă
    assert tranzacție.ieșire[plătitor.adresă] == plătitor.sumă - sumă
    assert 'dată' in tranzacție.intrare
    assert tranzacție.intrare['sumă'] == plătitor.sumă
    assert tranzacție.intrare['adresă'] == plătitor.adresă
    assert tranzacție.intrare['cheia_publică'] == plătitor.cheie_publică

    assert Portofel.verifică
    (
        tranzacție.intrare['cheia_publică'],
        tranzacție.ieșire,
        tranzacție.intrare['semnătura']
    )

def test_tranzacție_sumă_prea_mică():

    with pytest.raises(Exception, match='Suma este mai mare decât totalul portofelului !'):
        Tranzacție(Portofel(), 'recipient', 9001)


def test_tranzacție_actualizare_mai_mare():

    plătitor = Portofel()
    tranzacție = Tranzacție(plătitor, 'beneficiar', 50)

    with pytest.raises(Exception, match='Suma este mai mare decât totalul !'):
        tranzacție.actualizează(plătitor, 'nou_beneficiar', 9001)


def test_tranzacție_actualizare():

    plătitor = Portofel()
    primul_beneficiar = 'primul_beneficiar'
    prima_sumă = 50

    tranzacție = Tranzacție(plătitor, primul_beneficiar, prima_sumă)

    urmatorul_beneficiar = 'următorul_beneficiar'
    următoare_sumă = 75

    # with pytest.raises(Exception, match='Suma este mai mare decât totalul !'):
    tranzacție.actualizează(plătitor, urmatorul_beneficiar, următoare_sumă)

    assert tranzacție.ieșire[urmatorul_beneficiar] == următoare_sumă
    assert tranzacție.ieșire[plătitor.adresă] == \
              plătitor.sumă - prima_sumă - următoare_sumă

    assert Portofel.verifică
    (
        tranzacție.intrare['cheia_publică'],
        tranzacție.ieșire,
        tranzacție.intrare['semnătura']
    )

    către_primul_beneficiar = 25
    tranzacție.actualizează(plătitor, primul_beneficiar, către_primul_beneficiar)

    assert tranzacție.ieșire[primul_beneficiar] ==\
        prima_sumă + către_primul_beneficiar
    assert tranzacție.ieșire[plătitor.adresă] ==\
        plătitor.sumă - prima_sumă - următoare_sumă - către_primul_beneficiar
    assert Portofel.verifică
    (
        tranzacție.intrare['cheia_publică'],
        tranzacție.ieșire,
        tranzacție.intrare['semnătura']
    )

def test_validă_tranzacție():

    Tranzacție.e_validă_tranzacția(Tranzacție(Portofel(),'beneficiar',50))

def test_validă_tranzacție_cu_ieșire_invalidă():

    plătitor = Portofel()
    tranzacție = Tranzacție(plătitor, 'beneficiar', 50)
    tranzacție.ieșire[plătitor.adresă] = 9001

    with pytest.raises(Exception, match='Tranzacție invalidă valori ieșire'):
        Tranzacție.e_validă_tranzacția(tranzacție)

def test_validă_tranzacție_cu_invalidă_semnătură():
    tranzacție = Tranzacție(Portofel(), 'recipient', 50)
    tranzacție.intrare['semnătură'] = Portofel().semnează(tranzacție.ieșire)
    
    # with pytest.raises(Exception, match='Semnătură Invalidă !'):

def test_răsplătire_tranzacție():
    miner = Portofel()
    tranzacție = Tranzacție.răsplătește_tranzacție(miner)

    assert tranzacție.intrare == RĂSPLĂTIRE_
    assert tranzacție.ieșire[miner.adresă] == RĂSPLĂTIRE

def test_validă_răsplătire():
    răsplătire_tranzacție = Tranzacție.răsplătește_tranzacție(Portofel())
    Tranzacție.e_validă_tranzacția(răsplătire_tranzacție)

def test_invalidă_răsplătire():
    răsplătire_tranzacție = Tranzacție.răsplătește_tranzacție(Portofel())
    răsplătire_tranzacție.ieșire['extra'] = 60

    with pytest.raises(Exception, match='Răsplătire de miner, invalidă !'):
        Tranzacție.e_validă_tranzacția(răsplătire_tranzacție)

def test_invalidă_răsplătire_prea_mare_sumă():

    portofel = Portofel()

    răsplătire_tranzacție = Tranzacție.răsplătește_tranzacție(portofel)
    răsplătire_tranzacție.ieșire[portofel.adresă] = 9001

    with pytest.raises(Exception, match='Răsplătire de miner, invalidă !'):
        Tranzacție.e_validă_tranzacția(răsplătire_tranzacție)