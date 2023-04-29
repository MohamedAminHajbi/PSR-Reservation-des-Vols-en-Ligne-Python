from vols_manager import GestionnaireVols
from vols_manager import Histo



resultat = ""
# Create a new instance of GestionnaireVols with the name of the input file
gestionnaire_vols = GestionnaireVols("vols.txt")


# Cancel a reservation on a flight
cancellation_successful, message = gestionnaire_vols.reserver("001", "Agence1", "Annulation", 2 , resultat)
print(message)

# Generate the list of invoices for the agencies
gestionnaire_vols.generer_factures("factures.txt")


#Reserve a flight

#reservation_successful , message1 = gestionnaire_vols.reserver("001" , "Agence1" , "Demande" , 3)
#print(message1)