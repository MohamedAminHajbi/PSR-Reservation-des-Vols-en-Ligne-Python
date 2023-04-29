from vols_manager import GestionnaireVols
from vols_manager import Histo

# Create a new instance of GestionnaireVols with the name of the input file
gestionnaire_vols = GestionnaireVols("vols.txt")


# Cancel a reservation on a flight
cancellation_successful, message = gestionnaire_vols.reserver("001", "Agence1", "Annulation", 2)
print(message)

# Generate the list of invoices for the agencies
gestionnaire_vols.generer_factures("factures.txt")