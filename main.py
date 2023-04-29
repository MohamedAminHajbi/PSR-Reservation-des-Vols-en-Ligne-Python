from vols_manager import GestionnaireVols


# Create a new instance of GestionnaireVols with the name of the input file
gestionnaire_vols = GestionnaireVols()


# Reserve some seats on a flight
reservation_successful, message = gestionnaire_vols.reserver("001", "Agence2", "Annulation", 5)
print(message)

