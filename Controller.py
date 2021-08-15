from Model import *
from View import *
from Database import *

#ensemble client , chambre (d'un étage, resa a cette etage)
#ajouter les autres fonctions
class Controller :

    def __init__(self,database):
        self._database = database
      

    def all_clients(self) :
        return self._database.getAllClients()
    
    def ajouter_client(self,client) :

        self._database.ajouter_client(client)
    
    def ajouter_chambre(self,chambre) :
        self._database.ajouter_chambre(chambre)
    

    def ajouter_reservation(self, reservation) :
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

    def get_reservation_byDateandRoomNumber(self, date, id_chambre):
        return self._database.get_reservation_byDateandRoomNumber(date, id_chambre)

    def get_id_byNumChambre (self, id_chambre) : 
        return self._database.get_id_byNumChambre(id_chambre)

    

    def modifier_client_byId(self,client):
        
        if client._id == -1 :
            if self._database.getClientByMail(client._mail) == None :
                self._database.ajouter_client(client)
                return "OK"
            else :
                return "MAIL EXISTANT"

        else : 
            self._database.modifier_client_byId(client)
            return "OK"
            
    def supprimer_client_byId(self,client):
        self._database.supprimer_client_byId(client)
    


    def creer_reservation(self):
        clients = self.getAllClients()
        for c in range(0,len(clients)) :
            print(str(c+1) +" : "+ clients[c]._nom +" "+clients[c]._prenom)
        client = int(input("Qui est le client : "))
        print(str(clients[client-1]._id)+" "+clients[client-1]._nom)
        chambres = self.getAllChambres()
        for i in range (0,len(chambres)):
            print(str(i+1)+" : "+str(chambres[i]._numero)+" : "+str(chambres[i]._capacite))
        chambre = int(input("Quel chambre :"))
        print(str(chambres[chambre-1]._id)+":"+str(chambres[chambre-1]._numero))
        date_arrivee = input ("A partir de : ")
        date_depart = input("Jusqu'au : ")
        reservation = Reservation(clients[client-1]._id, chambres[chambre-1]._id, date_arrivee, date_depart)
        #print ("je renvois la réservation de "+clients[client-1]._nom+" qui sejournera a la chambre "+str(chambres[chambre-1]._numero)+" a partir du " +str(date_arrivee)+" jusqu'au "+str(date_depart) )
        return reservation


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

    

    


       

        
