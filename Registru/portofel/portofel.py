import json
import uuid

from Registru.configurare import TOTAL
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class Portofel:
    """
    Un portofel individual ce permite unui miner să își observe totalul
    și să autorizeze tranzacții
    """

    def __init__(self, registru=None, adresă =None, cheie_privată = None, cheie_publică= None):
        self.registru = registru
        self.adresă = str(uuid.uuid4())[0:8]
        self.cheie_privată = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.cheie_publică = self.cheie_privată.public_key()
        self.serializează_cheie_publică()

    @property
    def sumă(self):
        return Portofel.calculează_total(self.registru, self.adresă)
    
    def to_json(self):
        return self.__dict__

    @staticmethod
    def din_json(self, portofel):
        return Portofel(**portofel)
    
    def to_string(self):
        return str(self)
    # @staticmethod
    # def generează_chei(self):
    #     pem = ec.generate_private_key(ec.SECP256K1(), default_backend())

    #     private_pem = pem.private_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PrivateFormat.PKCS8,
    #     encryption_algorithm=serialization.NoEncryption()).decode('utf-8')

    #     public_pem = pem.public_key().public_bytes(
    #         encoding=serialization.Encoding.PEM,
    #         format=serialization.PublicFormat.SubjectPublicKeyInfo
    #     ).decode('utf-8')

    #     with open(f'C:\\Users\\jovre\\Documents\\system\\Registru\\utile\\chei\\cheie_privată.pem', 'w+') as f:
    #         f.write(private_pem)
    #         f.close()

    #     with open(f'C:\\Users\\jovre\\Documents\\system\\Registru\\utile\\chei\\cheie_publică.pem', 'w+') as f:
    #         f.write(public_pem)
    #         f.close()

    @staticmethod
    def din_cheie(self, file):
        with open(file, "r+") as f:
            informații = f.read()

        # print(load_pem_private_key(informații.encode('utf-8'), password=None).public_key().public_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PublicFormat.SubjectPublicKeyInfo
        # ).decode('utf-8'))
        return load_pem_private_key(informații.encode("utf-8"), password=None)

    def semnează(self, informații):
        """
        Generează o semnătură bazată pe informații folosind cheia privată
        """
        return decode_dss_signature(self.cheie_privată.sign(
            json.dumps(informații).encode('utf-8'), 
            ec.ECDSA(hashes.SHA256())))

    def serializează_cheie_publică(self):
        """
        Resetează cheia publică în versiunea serializată
        """

        if type(self.cheie_publică) != str:
            self.cheie_publică = self.cheie_publică.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

        else:
            return self.cheie_publică

    @staticmethod
    def verifică(cheie_publică, informații, semnătură):
        """
        Verifică semnătura bazată pe originala cheie publică și informațiile.
        """

        cheie_publică_deserializată = serialization.load_pem_public_key(
            cheie_publică.encode('utf-8'),
            default_backend()
        )

        try:
            cheie_publică_deserializată.verify(encode_dss_signature(semnătură[0],semnătură[1]),
            json.dumps(informații).encode('utf-8'),
            ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def calculează_total(registru, adresă):
        """
        Calculează totalul a unei adrese considerând informațiile din registru.

        Totalul este calculat prin adăugare a ieșirilor care aparțin în adresă de când
        a fost cea mai recentă tranzacție a adresei. 
        """

        total = TOTAL

        if not registru or not registru.listă[-1].informații:
            return total

        for bloc in registru.listă:
            for tranzacție in bloc.informații:
                if type(tranzacție) == list:
                    for tranzacția in tranzacție:
                        if 'id' in tranzacția and tranzacția['intrare']['adresă'] == adresă:
                            """
                            Oricând adresa are o nouă tranzacție resetează totalul
                            """
                            
                            total = tranzacția['ieșire'][adresă]
                        elif 'id' in tranzacția and adresă in tranzacția['ieșire']:
                            total += tranzacția['ieșire'][adresă]
                else:
                    if 'id' in tranzacție and tranzacție['intrare']['adresă'] == adresă:
                        """
                        Oricând adresa are o nouă tranzacție resetează totalul
                        """
                        
                        total = tranzacție['ieșire'][adresă]
                    elif 'id' in tranzacție and adresă in tranzacție['ieșire']:
                        total += tranzacție['ieșire'][adresă]
                        
        return total





def main():
    portofel = Portofel()
    print(f'portofel: {portofel.__dict__}')

    informații = {'foo': 'bar'}
    semnătura = portofel.semnează(informații)
    print(f'semnătură: {semnătura}')

    valid = Portofel.verifică(portofel.cheie_publică, informații, semnătura)
    print(valid)

    invalid = Portofel.verifică(Portofel().cheie_publică, informații, semnătura)
    print(invalid)

if __name__ == '__main__':
    main()