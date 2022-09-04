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

    def __init__(self,id_client,id_chambre,date_arrivee,date_depart,nb_occupants, origine = "") :
        self._id = -1
        self._id_client = id_client
        self._id_chambre = id_chambre
        self._nb_occupants = nb_occupants
        self._date_arrivee = date_arrivee
        self._date_depart = date_depart
        self._origine = origine
        self._couts = []
    
    def getNuitees(self, from_date):
        if from_date == None :
            return 1 + (self._date_depart - self._date_arrivee).days
        else :
            return 1 + (self._date_depart - from_date.replace(hour=0,minute=0,second=0, microsecond=0)).days

class Couts_jour :
    def __init__ (self, date_jour, total_chambre,total_petit_dej,total_bar,total_telephone,total_taxe_sejour) :
        self._id = -1
        self._date_jour = date_jour
        self._total_chambre = total_chambre
        self._regle_chambre = 0
        self._total_petit_dej = total_petit_dej
        self._regle_petit_dej = 0
        self._total_bar = total_bar
        self._regle_bar = 0
        self._total_telephone = total_telephone
        self._regle_telephone = 0
        self._total_taxe_sejour = total_taxe_sejour
        self._regle_taxe_sejour = 0


        

        


