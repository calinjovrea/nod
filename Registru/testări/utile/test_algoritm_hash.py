from Registru.utile.algoritm_hash import creează_hash

def test_algoritm_hash():

    assert creează_hash(1,[2], 'three') == creează_hash('three',1,[2])
    assert creează_hash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'