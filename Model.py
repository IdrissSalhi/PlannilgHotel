

class Client :
    
    def __init__(self,nom="",prenom="",adresse="",mail="",telephone="") :
        self._id = -1
        self._nom = nom
        self._prenom = prenom
        self._adresse = adresse
        self._mail = mail
        self._telephone = telephone
    
    def display(self):

        print("("+self._nom +") "+"("+self._prenom+") "+"("+self._adresse+")  "+"("+self._mail+")  "+"("+self._telephone+")  ")
    

class Chambre :

    def __init__(self,numero,capacite) :
        self._id = -1
        self._numero = numero
        self._capacite = capacite
    
    def display(self):

        print("("+str(self._numero) +")  "+"("+str(self._capacite) +")") 

class Reservation :

    def __init__(self,id_client,id_chambre,date_arrivee,date_depart,nb_occupants) :
        self._id = -1
        self._id_client = id_client
        self._id_chambre = id_chambre
        self._nb_occupants = nb_occupants
        self._date_arrivee = date_arrivee
        self._date_depart = date_depart
    
    def display(self):
        print("("+str(self._id_client)+")  " +"("+str(self._id_chambre) +")  "+"("+str(self._date_arrivee) + ")  " +"("+str(self._date_depart) +")")



