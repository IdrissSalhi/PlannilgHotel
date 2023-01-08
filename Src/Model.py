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

    def __init__(self,id_client,id_chambre,date_arrivee,date_depart,nb_occupants,accompte, origine = "") :
        self._id = -1
        self._id_client = id_client
        self._id_chambre = id_chambre
        self._nb_occupants = nb_occupants
        self._date_arrivee = date_arrivee
        self._date_depart = date_depart
        self._origine = origine
        self._accompte = accompte
        self._couts = []
    
    def getNuitees(self, from_date):
        if from_date == None :
            return 1 + (self._date_depart - self._date_arrivee).days
        else :
            return 1 + (self._date_depart - from_date.replace(hour=0,minute=0,second=0, microsecond=0)).days

    def update_couts (self, nouveaux_cj) :
     
        self._couts = list(filter(lambda x: (x._date_jour >= self._date_arrivee and x._date_jour <= self._date_depart), self._couts))
        if self._couts != [] :
            modele_cout = self._couts[0]
        else :
            modele_cout = nouveaux_cj[0]
        
        for nc in nouveaux_cj :
            tag = False
            for oc in self._couts :
                if nc._date_jour == oc._date_jour :
                    tag = True
            if tag == False :
                nc._total_chambre = modele_cout._total_chambre
                nc._total_petit_dej = modele_cout._total_petit_dej
                nc._total_bar = modele_cout._total_bar
                nc._total_telephone= modele_cout._total_telephone
                nc._total_taxe_sejour= modele_cout._total_taxe_sejour
                self._couts.append(nc)
        
      
       
    
    def afficher_couts (self):
        print(self._id)
        if self._couts == [] :
            print("liste vide")
        for c in self._couts:
            print(c._date_jour)
    


class Couts_jour :
    def __init__ (self, date_jour, total_chambre,total_petit_dej,total_bar,total_telephone,total_taxe_sejour) :
        self._date_jour = date_jour
        self._total_chambre = total_chambre
        self._total_petit_dej = total_petit_dej
        self._total_bar = total_bar
        self._total_telephone = total_telephone
        self._total_taxe_sejour = total_taxe_sejour
    
    


        

        


