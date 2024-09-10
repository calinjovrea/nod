class Mină:
    def __init__(self):
        self.harta_tranzacțiilor = {}
    
    def to_json(self):
        def tranzacții_to_json():

            for item in self.harta_tranzacțiilor.keys():
                if type(self.harta_tranzacțiilor[item]) != dict:
                    self.harta_tranzacțiilor[item] = self.harta_tranzacțiilor[item].to_json()
        
        tranzacții_to_json()

        return self.__dict__
        
    def pune_tranzacția(self, tranzacție):
        """
        Pune o tranzacție în mină
        """
        self.harta_tranzacțiilor[tranzacție.id] = tranzacție

    def tranzacție_existentă(self, adresă):

        """
        Caută o tranzacție generată de o adresă în mină
        """
        # tranzacție = [tranzacția if tranzacția.intrare['adresă'] == adresă else None for self.harta_tranzacțiilor.values()]

        for transacție in self.harta_tranzacțiilor.values():
            if transacție.intrare['adresă'] == adresă:
                return transacție
        # return transacție[0] if len(transacție) >= 1 else None

    def informații_tranzacții(self):
        """
        Transmite tranzacțiile minei în format json serializat.
        """
        return list(map(lambda transacție: transacție.to_json(),self.harta_tranzacțiilor.values()))

    def clarifică_registru_tranzacții(self, registru):

        """
        Șterge tranzacțiile ce sunt în registru din mină. 
        """

        for bloc in registru.listă:

            if bloc.informații:
                for tranzacție in bloc.informații:
                    if '#' not in tranzacție:
                        for informații in tranzacție:
                            try:
                                del self.harta_tranzacțiilor[informații['id']]
                            except KeyError:
                                pass
    
    def e_necesar_îndeplinitor(self):
        if len(self.harta_tranzacțiilor) >= 1:
            return True
        else:
            return False