from Src.Model import *
from Src.View import *
from Src.Database import *
import time

class Controller :

    def __init__(self,database):
        self._database = database
        self.log("Program Started")
    
    def log(self,message):
       file_name = "Bellevue_log_" + time.strftime("%Y%m%d")
       f = open("Logs/" + file_name + ".txt", "a")
       f.write(time.strftime("%H:%M:%S ") + message  + "\n")
       f.close()

      

    def all_clients(self) :
        return self._database.getAllClients()
    
    def ajouter_client(self,client) :
        self.log("Client added : " + client._nom + ", " + client._prenom + ", " + client._mail + ", " + client._adresse + ", " + client._telephone)
        self._database.ajouter_client(client)
    
    def ajouter_chambre(self,chambre) :
        self.log("Room added : " + str(chambre._numero) + ", " + str(chambre._capacite))
        self._database.ajouter_chambre(chambre)
    

    def ajouter_reservation(self, reservation) :
        self.log("Reservation added : "+ str(reservation._id_client) + ", " + str(reservation._id_chambre) + ", " + str(reservation._nb_occupants) + ", " + str(reservation._est_reglee) + ", " + reservation._date_arrivee.strftime("%Y%m%d") + ", " + reservation._date_depart.strftime("%Y%m%d") + ", " + reservation._origine )
        self._database.ajouter_reservation(reservation)

    
    def getClientById(self, _id) :
        return self._database.getClientById(_id)
    
    
    def getChambreById(self, _id) :
        return self._database.getChambreById(_id)

    def getReservationById(self, _id) :
        return self._database.getReservationById(_id)
    
    def getClientByMail(self, _mail) :
        return self._database.getClientByMail(_mail)

    def getAllClients(self) :
        return self._database.getAllClients()
    
    def getAllChambres(self) :
        return self._database.getAllChambres()

    def get_reservation_byDateandRoomId(self, date, id_chambre):
        return self._database.get_reservation_byDateandRoomId(date, id_chambre)

    def get_id_byNumChambre (self, id_chambre) : 
        return self._database.get_id_byNumChambre(id_chambre)

    

    def modifier_client_byId(self,client):
        if self._database.getClientByMail(client._mail) == None :
            if client._id == -1 :
                self.log("Client added : " + client._nom + ", " + client._prenom + ", " + client._mail + ", " + client._adresse + ", " + client._telephone)
                self._database.ajouter_client(client)
            else : 
                self.log("Client modified : " + client._nom + ", " + client._prenom + ", " + client._mail + ", " + client._adresse + ", " + client._telephone)
                self._database.modifier_client_byId(client)
            return "OK"
        else :
            return "MAIL EXISTANT"

        
            
    def supprimer_client_byId(self,client):
        self.log("Client "+ client._nom + " " + client._prenom + "supprime :"+ client._mail + ", " + client._adresse + ", " + client._telephone)
        self._database.supprimer_client_byId(client)
    


    def modifier_reservation_byId(self, reservation) :
        if reservation._id == -1 :
            self.log("Reservation added : "+ str(reservation._id_client) + ", " + str(reservation._id_chambre) + ", " + str(reservation._nb_occupants) + ", " + str(reservation._est_reglee) + ", " + reservation._date_arrivee.strftime("%Y%m%d") + ", " + reservation._date_depart.strftime("%Y%m%d") + ", " + reservation._origine )
            return self._database.ajouter_reservation(reservation)
            
             
        else :  
            self.log("Reservation modified : "+ str(reservation._id_client) + ", " + str(reservation._id_chambre) + ", " + str(reservation._nb_occupants) + ", " + str(reservation._est_reglee) + ", " + reservation._date_arrivee.strftime("%Y%m%d") + ", " + reservation._date_depart.strftime("%Y%m%d") + ", " + reservation._origine )
            self._database.modifier_reservation_byId(reservation)
            return reservation._id
        
    def getRoomsAsArray(self) :
        rooms_1d = []
        chambres = self.getAllChambres()
        if len(chambres) == 0 :
            return []
        else :
            for i in range (0,len(chambres)):
                rooms_1d.append(chambres[i]._numero)
            rooms = []
            etages = int(rooms_1d[-1] / 100)
            for i in range(0,etages) :
                rooms.append([])
            for nc in rooms_1d :
                rooms[int(nc/100)-1].append(nc)

        return rooms
    
    def get_capacite_max_chambre (self) :
        return self._database.get_capacite_max_chambre()

    def  supprimer_resa_byId(self,reservation) :
        self.log("Reservation supprimee  : id client : "+ str(reservation._id_client) + ", id chambre : " + str(reservation._id_chambre) + ", nombre d'occupants : " + str(reservation._nb_occupants) + ", reservation reglee : " + str(reservation._est_reglee) + ", date-arrivee :  " + reservation._date_arrivee.strftime("%Y%m%d") + ", date depart :  " + reservation._date_depart.strftime("%Y%m%d") + ", origine : " + reservation._origine )
       
        self._database.supprimer_resa_byId(reservation)

    def get_chambre_dispo (self,reservation) :
        return self._database.get_chambre_dispo(reservation)
    
    def supprimer_resa_byClient(self,client) :
        self.log("Les reservations de "+ client._nom + " " + client._prenom + " ont ete supprimees")
        self._database.supprimer_resa_byClient(client)

        
    


       

        
