from datetime import *

class Client :
    
    def __init__(self,nom="",prenom="",adresse="",mail="",telephone="") :
        self._id = -1
        self._nom = nom
        self._prenom = prenom
        self._adresse = adresse
        self._mail = mail
        self._telephone = telephone
    

class Chambre :

    def __init__(self,numero,capacite) :
        self._id = -1
        self._numero = numero
        self._capacite = capacite
    

class Reservation :

    def __init__(self,id_client,id_chambre,date_arrivee,date_depart,nb_occupants,est_reglee=False) :
        self._id = -1
        self._id_client = id_client
        self._id_chambre = id_chambre
        self._nb_occupants = nb_occupants
        self._est_reglee = est_reglee
        self._date_arrivee = date_arrivee
        self._date_depart = date_depart
    
    def getNuitees(self, from_date):
        print (self._date_depart, from_date.replace(hour=0,minute=0,second=0, microsecond=0))
        if from_date == None :
            return 1 + (self._date_depart - self._date_arrivee).days
        else :
            return 1 + (self._date_depart - from_date.replace(hour=0,minute=0,second=0, microsecond=0)).days
        
        

        


