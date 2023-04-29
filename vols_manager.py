#class vols

class Vol:
    def __init__(self, ref_vol, destination, nb_places_dispo, prix_place):
        self.ref_vol = ref_vol
        self.destination = destination
        self.nb_places_dispo = nb_places_dispo
        self.prix_place = prix_place
        
        
#calss gestion des vols   
        
class GestionnaireVols:
    
    
    
    def __init__(self, nom_fichier):
        self.vols = {}
        self.factures = {}
        self.transactions = []
        with open(nom_fichier, 'r') as f:
            for line in f:
                ref_vol, destination, nb_places_dispo, prix_place = line.strip().split()
                self.vols[ref_vol] = Vol(ref_vol, destination, int(nb_places_dispo), float(prix_place))
        f.close()



    def sauvegarder_vols(self, nom_fichier):
        with open(nom_fichier, 'w') as f:
            for ref_vol, vol in self.vols.items():
                f.write(f"{vol.ref_vol} {vol.destination} {vol.nb_places_dispo} {vol.prix_place}\n")
        f.close()



   
        
    def sauvegarder_histo(self, nom_fichier):
       
        with open(nom_fichier, 'w') as f:
            f.write("Référence Vol Agence Transaction Valeur Résultat\n")
            for transaction in self.transactions:
                ref_vol, agence, transaction_type, valeur, resultat = transaction
                f.write(f"{ref_vol} {agence} {transaction_type} {valeur} {resultat}\n")
        f.close()
        
    def ajouter_transaction(self, ref_vol, agence, transaction, valeur, resultat):
        with open(nom_fichier, 'r') as f:
            for line in f:
                ref_vol, agence, transaction, valeur, resultat = line.strip().split()
                self.transactions.append((ref_vol, agence, transaction, int(valeur), resultat))
        f.close()
        self.transactions.append((ref_vol, agence, transaction, valeur, resultat))
        if resultat == "Demande acceptée" or resultat == "Annulation acceptée":
            GestionnaireVols.factures[agence] = GestionnaireVols.factures.get(agence, 0)
            
            
            
            
            
    def reserver(self, ref_vol, agence, transaction, valeur ,resultat):
        vol = self.vols.get(ref_vol)
        if vol is None:
            return False, "Vol inexistant"
        if transaction == "Demande":
            if vol.nb_places_dispo >= valeur:
                vol.nb_places_dispo -= valeur
                resultat = "Demande acceptée"
                ajouter_transaction(self, ref_vol, agence, transaction, valeur, resultat)
                montant = valeur * vol.prix_place
                self.factures[agence] = self.factures.get(agence, 0) + montant
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
                return True, resultat
            else:
                return False, "Demande refusée"
        elif transaction == "Annulation":
            penalite = 0.1 * valeur * vol.prix_place
            vol.nb_places_dispo += valeur
            montant = valeur * vol.prix_place - penalite
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
            return True, "Annulation acceptée"
        else:
            return False, "Transaction invalide"
        
        
    def generer_factures(self, nom_fichier):
        with open(nom_fichier, 'w') as f:
            for agence, montant in self.factures.items():
                f.write(f"{agence} {montant}\n")
        f.close()

        # Update factures.txt with new information
        with open("factures.txt", "w") as f:
            for agence, montant in self.factures.items():
                f.write(f"{agence} {montant}\n")
        f.close()
        
        
        
        
        
        
        
        
  #class histo      

class Histo:
    
    def __init__(self, nom_fichier):
        self.transactions = []
        with open(nom_fichier, 'r') as f:
            for line in f:
                ref_vol, agence, transaction, valeur, resultat = line.strip().split()
                self.transactions.append((ref_vol, agence, transaction, int(valeur), resultat))
        f.close()

    def ajouter_transaction(self, ref_vol, agence, transaction, valeur, resultat):
        self.transactions.append((ref_vol, agence, transaction, valeur, resultat))
        if resultat == "Demande acceptée" or resultat == "Annulation acceptée":
            GestionnaireVols.factures[agence] = GestionnaireVols.factures.get(agence, 0)
            

    def sauvegarder_histo(self, nom_fichier):
        with open(nom_fichier, 'w') as f:
            f.write("Référence Vol Agence Transaction Valeur Résultat\n")
            for transaction in self.transactions:
                ref_vol, agence, transaction_type, valeur, resultat = transaction
                f.write(f"{ref_vol} {agence} {transaction_type} {valeur} {resultat}\n")
        f.close()