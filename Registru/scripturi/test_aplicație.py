import requests
import time
import threading
import multiprocessing
import os

import random

from Registru.sistem import Registrul
from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.portofel import Portofel
from cryptography.hazmat.primitives import hashes, serialization

from multiprocessing import Pool
from multiprocessing import Process


URL = 'http://localhost:5000'
def cere_registrul():
    return requests.get(f'{URL}/registru').json()

def cere_registru_minează():
    return requests.get(f'{URL}/registru/minează').json()

def tranzacție(plătitor,beneficiar,sumă):

    plătitor.cheie_privată = []

    if plătitor.registru:
        try:
            plătitor.registru = plătitor.registru.to_json()
        except Exception as e:
            plătitor.registru = plătitor.registru 
             
    return requests.post(f'{URL}/portofel/trimite',
    json={'plătitor': plătitor.to_json(),'beneficiar': beneficiar, 'sumă': sumă}).json()


def tranzacții_în_masă(tranzacții):

    plătitori = [w['plătitor'] for w in tranzacții]
    beneficiari = [w['beneficiar'] for w in tranzacții]
    sume = [w['sumă'] for w in tranzacții]

    if len(plătitori) == len(beneficiari) == len(sumă):
        return requests.post(f'{URL}/portofel/trimite',json={'plătitori': plătitori, 'beneficiari':'beneficiari', 'sume': sume}).json()
    else:
        raise Exception('Date Incorecte pentru Tranzacții !')


def cere_info_portofel():
    return requests.get(f'{URL}/portofel/info').json() 

# start_registru = cere_registrul()
# print(f'Registrul: {start_registru}')

# beneficiar = Portofel().adresă

# for i in range(5):
#     tranzacție_1 = tranzacție(beneficiar,random.randint(1,5))
#     print(f'\n tranzacție {tranzacție_1}')

# time.sleep(5)
# acțiune = cere_registru_minează()

# print(f'\nAcțiune:{acțiune}')

# portofel_info = cere_info_portofel()
# print(f'Info Portofel: {portofel_info}')


from Registru.consensus.consensus import Consensus
from Registru.consensus.loc import Loc

import random
import string

def aleatoriu(lungime):
    """
    """
    litere = string.ascii_lowercase
    rezultat = ''.join(random.choice(litere) for i in range(lungime))
    return rezultat

def test_1():
    """

    """
    consensus = Consensus()
    consensus.actualizează('Ioan', 19)
    consensus.actualizează('Maria', 25)
    print(consensus.cere('Ioan'))
    print(consensus.cere('Maria'))
    print(consensus.cere('Ioans'))

def test_2():
    """
    """

    loc = Loc('Ioan', 1, 'ultimul_hash')

    print(loc.hashLoc())

def text_3():
    consensus = Consensus()
    consensus.actualizează('Ioan', 100)
    consensus.actualizează('Maria', 100)

    ioan_ = 0
    maria_ = 0

    for i in range(100):
        îndeplinitor = consensus.îndeplinitor(aleatoriu(i))
        if îndeplinitor == 'Ioan':
            ioan_ += 1
        elif îndeplinitor == 'Maria':
            maria_ += 1

    print(f'Ioan --> {ioan_}')
    print(f'Maria --> {maria_}')

def test_4():
    import time

    registru = Registrul()

    portofel = Portofel(registru)
    portofel_2 = Portofel(registru)
    portofel_3 = Portofel(registru)

    start = time.time()
    [tranzacție(portofel,f'Ioan-{random.randint(10,1000)}', random.randint(10,15)) for i in range(2)]
    print(time.time()-start)
     #  tranzacție(portofel_2,f'Maria-{random.randint(10,1000)}', random.randint(10,15))
    
    
    # for i in range(3):
    #    tranzacție(portofel,f'Ioan-{random.randint(10,1000)}', random.randint(10,15))
    #    tranzacție(portofel_3,f'Maria-{random.randint(10,1000)}', random.randint(10,15))
    
    # for i in range(4):
    #    tranzacție(portofel,f'Ioan-{random.randint(10,1000)}', random.randint(10,15))
    #    tranzacție(portofel_3,f'Maria-{random.randint(10,1000)}', random.randint(10,15))

def test_5():
    Portofel.din_cheie(Portofel,f'C:\\Users\\jovre\\Documents\\GitHub\\sistem\\sistem\\Registru\\utile\\chei\\cheie_privată.pem')

def test_6():

    start = time.time()
    portofele = [Portofel() for w in range(5000)]

    tranzacții = [Tranzacție(portofele[i], f'beneficiar-{random.randint(1,25000)}', random.randint(1,250)).to_json() for i in range(len(portofele))]


    bloc = requests.post(f'{URL}/portofel/trimite/tranzacții', json={'tranzacții': tranzacții}).json()
    print(print(time.time() - start))

    return bloc


def test_6_threaded():
    threads = []
    for k in range(8):
        t = threading.Thread(target=test_6)
        threads.append(t)
        t.start()


def main():
    import multiprocessing

    start = time.time()
    
    for i in range(8):
        Process(target=test_6_threaded).start()

    end = time.time()
    print(end - start)
if __name__== '__main__':
    main()




