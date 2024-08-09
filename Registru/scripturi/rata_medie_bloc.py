import time

from Registru.sistem import Registrul
from Registru.configurare import SECUNDE

registru = Registrul()

dăți = []

for bloc in range(1000):
    start = time.time_ns()
    print(registru.listă)
    registru.adaugă_bloc(registru.listă[-1],bloc)
    sfârșit = time.time_ns()
    timp =  ( sfârșit - start ) / SECUNDE
    dăți.append(timp)

    medie = sum(dăți) / len(dăți)

    print(f'Dificultatea Noului Bloc: {registru.listă[-1].dificultate}')
    print(f'Timp pentru a mina un nou bloc: {timp}s')
    print(f'Timpul mediu pentru a adăuga un bloc: {medie}s\n')


