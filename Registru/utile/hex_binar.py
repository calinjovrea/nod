from Registru.utile.algoritm_hash import creează_hash

HEX_BINAR_TABEL_CONVERSIE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}

def hex_binar(hexx):
    binar = ''

    for caracter in hexx:
        binar += HEX_BINAR_TABEL_CONVERSIE[caracter]

    return binar


def main():
    număr = 451
    hexx = hex(număr)[2:]
    binar = hex_binar(hexx)
    print(f'hex: {hexx}')
    print(f'binar: {binar}')

    original = int(binar ,2)
    print(f'original: {original}')

    hash_original = hex_binar(creează_hash('hash-original'))
    print(f'hash_original_binar: {hash_original}')


if __name__ == '__main__':
    main()