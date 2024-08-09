from Registru.utile.hex_binar import hex_binar

def test_hex_binar():

    original = 789

    hexx = hex(789)[2:]
    binar = hex_binar(hexx)

    assert int(binar,2) == original