import random
import time


from Registru.sistem import Registrul
from Registru.portofel.mină import Mină
from Registru.portofel.tranzacție import Tranzacție
from Registru.portofel.portofel import Portofel


def test_pune_tranzacție():
    mină = Mină()
    tranzacție = Tranzacție(Portofel(),'recipient',1)
    mină.pune_tranzacția(tranzacție)

    assert mină.harta_tranzacțiilor[tranzacție.id] == tranzacție

def test_clafică_registru_tranzacții():
    mină = Mină()

    tranzacții = [Tranzacție(Portofel(), f'recipient-{random.randint(1,5)}', random.randint(1,5)) for i in range(2)] 
    [mină.pune_tranzacția(transacție) for transacție in tranzacții]

    registru = Registrul()
    registru.adaugă_bloc(['#123432', [w.to_json() for w in tranzacții]])

    assert len(tranzacții) == 2
    time.sleep(10)
    mină.clarifică_registru_tranzacții(registru)

    assert not tranzacții[0].id in mină.harta_tranzacțiilor

    assert not tranzacții[1].id in mină.harta_tranzacțiilor

