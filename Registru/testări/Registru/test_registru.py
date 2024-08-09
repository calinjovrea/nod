import pytest
import random

from Registru.sistem import Registrul
from Registru.portofel.portofel import Portofel
from Registru.portofel.tranzacție import Tranzacție

from Registru.configurare import RĂSPLĂTIRE,RĂSPLĂTIRE_

from Registru.bloc import Bloc
from Registru.bloc import INFORMAȚII_GENESIS

from Registru.utile.hex_binar import hex_binar


def test_registru():
    registru = Registrul()
    assert registru.listă[0].hash == INFORMAȚII_GENESIS['hash']

def test_adaugă_bloc():
    registru = Registrul()
    informații = 'test-data'
    
    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    registru.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue),informații])


    assert registru.listă[-1].informații == ['#%02x%02x%02x' % (red, green, blue),informații]
    
def test_minează_bloc():
    ultimul_bloc = Bloc.geneză()
    informații = 'test-data'
    dificultate = 3
    nonce = 0
    bloc = Bloc.minează_bloc(ultimul_bloc,informații)

    assert isinstance(bloc,Bloc)
    assert bloc.informații == informații
    assert bloc.ultimul_hash == ultimul_bloc.hash
    assert hex_binar(bloc.hash)[0:bloc.dificultate] == '0' * bloc.dificultate

def test_geneză():

    geneză = Bloc.geneză()

    assert isinstance(geneză,Bloc)
    # assert geneză.dată == INFORMAȚII_GENESIS['dată']
    # assert geneză.ultimul_hash == INFORMAȚII_GENESIS['ultimul_hash']
    # assert geneză.hash == INFORMAȚII_GENESIS['hash']
    # assert geneză.informații == INFORMAȚII_GENESIS['informații']

    for cheie, valoare in INFORMAȚII_GENESIS.items():
        getattr(geneză, cheie) == valoare

def test_e_valid_blocul():
    ultimul_bloc = Bloc.geneză()
    bloc = Bloc.minează_bloc(ultimul_bloc, 'informații-test')
    Bloc.e_valid_blocul(ultimul_bloc,bloc)


@pytest.fixture
def ultimul_bloc():
    return Bloc.geneză()

@pytest.fixture
def bloc(ultimul_bloc):
    return Bloc.minează_bloc(ultimul_bloc, 'informații-test')
    

def test_e_valid_blocul_rău():
    ultimul_bloc = Bloc.geneză()
    bloc = Bloc.minează_bloc(ultimul_bloc, 'informații-test')
    bloc.ultimul_hash = 'rău_ultimul_hash'
    
    with pytest.raises(Exception, match='Ultimul hash a blocului trebuie să fie corect !'):
        Bloc.e_valid_blocul(ultimul_bloc,bloc)

def test_e_valid_blocul_algoritm_de_muncă(ultimul_bloc,bloc):
    bloc.hash = 'fff'

    with pytest.raises(Exception, match='Algoritmul de muncă nu a dat rezultatul corect !'):
        Bloc.e_valid_blocul(ultimul_bloc,bloc)

def test_e_valid_blocul_dificultate_sărită(ultimul_bloc,bloc):

    bloc.dificultate = 10
    bloc.hash = f'{"0" * 10}222bcd'

    with pytest.raises(Exception, match='Dificultatea trebuie să se adjusteze doar cu 1 !'):
        Bloc.e_valid_blocul(ultimul_bloc,bloc)

def test_e_valid_blocul_bloc_rău(ultimul_bloc,bloc):
    bloc.hash = '000000000000bcddef'

    with pytest.raises(Exception, match='Hash-ul blocului trebuie să fie corect !'):
        Bloc.e_valid_blocul(ultimul_bloc,bloc)

@pytest.fixture
def sistem_3_blocuri():

    registru = Registrul()
    for i in range(3):
        blue =  random.randint(0,10000000000) & 255
        green = (random.randint(0,10000000000) >> 8) & 255
        red =   (random.randint(0,10000000000) >> 16) & 255

        registru.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue),[Tranzacție(Portofel(),f'beneficiar-{random.randint(1,15)}',i).to_json()]])

    return registru

def test_e_validă_lista(sistem_3_blocuri):

    sistem_3_blocuri.e_validă_lista(sistem_3_blocuri.listă)

def test_e_validă_lista_rea_geneză(sistem_3_blocuri):

    sistem_3_blocuri.listă[0].hash = 'hash_rău'

    with pytest.raises(Exception, match='Blocul geneză trebuie să fie valid !'):
        sistem_3_blocuri.e_validă_lista(sistem_3_blocuri.listă)

def test_înlocuiește_listă(sistem_3_blocuri):

    registru_nou = Registrul()
    registru_nou.înlocuiește_listă(sistem_3_blocuri.listă)

    assert registru_nou.listă == sistem_3_blocuri.listă

def test_înlocuiește_lista_nu_mai(sistem_3_blocuri):

    registru_nou = Registrul()
    registru_nou.înlocuiește_listă(sistem_3_blocuri.listă)

    with pytest.raises(Exception, match='Nu se poate înlocui'):
        sistem_3_blocuri.înlocuiește_listă(registru_nou.listă)

def test_înlocuiește_lista_rea_listă(sistem_3_blocuri):

    registru_nou = Registrul()
    sistem_3_blocuri.listă[1].hash = 'hash_rău'

    with pytest.raises(Exception, match='Nu se poate înlocui. lista ce vine este invalidă'):
        registru_nou.înlocuiește_listă(sistem_3_blocuri.listă)

def test_validă_tranzacție_listă(sistem_3_blocuri):
    Registrul.e_validă_lista_tranzacțiilor(sistem_3_blocuri.listă)

def test_validă_tranzacție_listă_duplicate(sistem_3_blocuri):

    tranzacție = Tranzacție(Portofel(),'beneficiar', 1).to_json()
    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    sistem_3_blocuri.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue),[tranzacție,tranzacție]])

    with pytest.raises(Exception, match='Tranzacția nu este unică !'):
        Registrul.e_validă_lista_tranzacțiilor(sistem_3_blocuri.listă)


def test_e_validă_tranzacția_multiple_răsplătiri(sistem_3_blocuri):
    răsplătire_1 = Tranzacție.răsplătește_tranzacție(Portofel()).to_json()
    răsplătire_2 = Tranzacție.răsplătește_tranzacție(Portofel()).to_json()
    
    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    sistem_3_blocuri.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue),[răsplătire_1,răsplătire_2]])

    with pytest.raises(Exception, match='Trebuie să existe doar o singură răsplătire !'):
        Registrul.e_validă_lista_tranzacțiilor(sistem_3_blocuri.listă)


def test_e_validă_tranzacția_rea(sistem_3_blocuri):

    tranzacție = Tranzacție(Portofel(),'beneficiar', 1)
    tranzacție.intrare['semnătura'] = Portofel().semnează(tranzacție.ieșire)

    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    sistem_3_blocuri.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue),tranzacție.to_json()])

    with pytest.raises(Exception):
        Registrul.e_validă_lista_tranzacțiilor(sistem_3_blocuri.listă)

def test_e_validă_tranzacția_listă_greșit_historică_sumă(sistem_3_blocuri):
    portofel = Portofel()
    tranzacție_rea = Tranzacție(portofel, 'beneficiar', 1)
    tranzacție_rea.ieșire[portofel.adresă] = 9000
    tranzacție_rea.intrare['sumă'] = 9001

    tranzacție_rea.intrare['semnătura'] = portofel.semnează(tranzacție_rea.ieșire)
    
    blue =  random.randint(0,10000000000) & 255
    green = (random.randint(0,10000000000) >> 8) & 255
    red =   (random.randint(0,10000000000) >> 16) & 255

    sistem_3_blocuri.adaugă_bloc(['#%02x%02x%02x' % (red, green, blue),tranzacție_rea.to_json()])

    with pytest.raises(Exception, match='are o sumă în intrare invalidă !'):
        Registrul.e_validă_lista_tranzacțiilor(sistem_3_blocuri.listă)


