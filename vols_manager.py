class Vol:
    def __init__(self, ref_vol, destination, nb_places_dispo, prix_place):
        self.ref_vol = ref_vol
        self.destination = destination
        self.nb_places_dispo = nb_places_dispo
        self.prix_place = prix_place
class GestionnaireVols:
    def __init__(self):
        self.vols = {}
        self.factures = {}
        self.transactions = []
        with open("vols.txt", 'r') as f:
            for line in f:
                ref_vol, destination, nb_places_dispo, prix_place = line.strip().split()
                self.vols[ref_vol] = Vol(ref_vol, destination, int(nb_places_dispo), float(prix_place))
        f.close()
        with open("factures.txt", 'r') as f:
            for line in f:
                agence,  prix = line.strip().split()
                self.factures[agence] = float(prix)
        f.close()
        with open("histo.txt", 'r') as f:
            for line in f:
                ref_vol, agence, transaction, valeur, resultat = line.strip().split()
                self.transactions.append((ref_vol, agence, transaction, int(valeur), resultat))
        f.close()
    def reserver(self, ref_vol, agence, transaction, valeur):
        vol = self.vols.get(ref_vol)
        if vol is None:
            return False, "Vol inexistant"
        if transaction == "Demande":
            if vol.nb_places_dispo >= valeur:
                vol.nb_places_dispo -= valeur
                montant = valeur * vol.prix_place
                self.factures[agence] = self.factures.get(agence, 0) + montant
                # Update vols.txt with information
                with open("vols.txt", "r") as f:
                    lines = f.readlines()
                with open("vols.txt", "w") as f:
                    for line in lines:
                        ref, dest, nb_places, prix = line.strip().split()
                        if ref == ref_vol:
                            nb_places = str(vol.nb_places_dispo)
                        f.write(f"{ref} {dest} {nb_places} {prix}\n")
                with open("factures.txt", "r") as f:
                    lines = f.readlines()
                    cond = False
                    for line in lines:
                        agenceF , prix = line.strip().split()
                        if agenceF == agence:
                            cond=True
                    if cond == True:
                        with open("factures.txt", "w") as fw:
                            for line in lines:
                                agenceF, prix = line.strip().split()
                                if agenceF == agence:
                                    prix = str(montant+float(prix))
                                fw.write(f"{agenceF} {prix}\n")
                    else:
                        lines.append(agence+' '+str(montant))
                        with open("factures.txt", "w") as fw:
                                for newline in lines:
                                    newagenceF , newprix = newline.strip().split()
                                    fw.write(f"{newagenceF} {newprix}\n")
                resultat="Succés"
                self.transactions.append((ref_vol, agence, transaction, valeur, resultat))
                with open("histo.txt", 'w') as f:
                    for transaction in self.transactions:
                        ref_vol, agence, transaction_type, valeur, resultat = transaction
                        f.write(f"{ref_vol} {agence} {transaction_type} {valeur} {resultat}\n")
                f.close()
                return True, "Demande accepté"
            else:
                resultat="Impossible"
                self.transactions.append((ref_vol, agence, transaction, valeur, resultat))
                with open("histo.txt", 'w') as f:
                    for transaction in self.transactions:
                        ref_vol, agence, transaction_type, valeur, resultat = transaction
                        f.write(f"{ref_vol} {agence} {transaction_type} {valeur} {resultat}\n")
                f.close()
                return False, "Demande refusée"
        elif transaction == "Annulation":
            with open("factures.txt", "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        agenceF , prix = line.strip().split()
                        if agenceF == agence:
                            x = float(prix)
            f.close()
            penalite = 0.1 * valeur * vol.prix_place
            vol.nb_places_dispo += valeur
            montant = x - valeur * vol.prix_place + penalite
            self.factures[agence] = self.factures.get(agence, 0) - montant
            # Update vols.txt with new information
            with open("vols.txt", "r") as f:
                lines = f.readlines()
            with open("vols.txt", "w") as f:
                for line in lines:
                    ref, dest, nb_places, prix = line.strip().split()
                    if ref == ref_vol:
                        nb_places = str(vol.nb_places_dispo)
                        prix = str(vol.prix_place)
                    f.write(f"{ref} {dest} {nb_places} {prix}\n")
            with open("factures.txt", "r") as f:
                    lines = f.readlines()
            with open("factures.txt", "w") as f:
                    for line in lines:
                        agenceF , prix = line.strip().split()
                        if agenceF == agence:
                            agence = str(agenceF)
                            prix = str(montant)
                        f.write(f"{agenceF} {prix}\n")
            resultat="Succés"
            self.transactions.append((ref_vol, agence, transaction, valeur, resultat))
            with open("histo.txt", 'w') as f:
                    for transaction in self.transactions:
                        ref_vol, agence, transaction_type, valeur, resultat = transaction
                        f.write(f"{ref_vol} {agence} {transaction_type} {valeur} {resultat}\n")
            f.close()
            return True, "Annulation acceptée"
        else:
            return False, "Transaction invalide"
    def getFacture(self, ag):
        with open("factures.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                agenceF , prix = line.strip().split()
                if agenceF == ag:
                    return("Votre facture est :"+prix)
    def getHisto(self, ag):
        with open("histo.txt", "r") as f:
            lines = f.readlines()
            x=""
            for line in lines:
                ref_vol, agence, transaction_type, valeur, resultat = line.strip().split()
                if ag == agence:
                    x=x+line+"\n"
            return x