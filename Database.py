import sqlite3
from Model import *


class Database : 

    def __init__(self) :
        self._connexion = sqlite3.connect('MaBDD.db')
        self._cursor = self._connexion.cursor()
        self.create_tables()
    
    
    def create_tables(self) :
    
        self._cursor.execute("""
        CREATE TABLE IF NOT EXISTS CLIENTS(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Nom TEXT,
            Prenom TEXT,
            Adresse TEXT,
            mail Text UNIQUE,
            telephone Text
        )
        """)

        self._cursor.execute("""CREATE TABLE IF NOT EXISTS CHAMBRES (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            num_ch INTEGER UNIQUE,
            capacite Integer
        )
        """)

        self._cursor.execute("""CREATE TABLE IF NOT EXISTS RESERVATIONS(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            id_client INTEGER NOT NULL,
            id_chambre INTEGER NOT NULL,
            date_arrivee DATE,
            date_depart DATE,
            nb_occupants INTEGER NOT NULL,
            FOREIGN KEY (id_client) references CLIENTS (id),
            FOREIGN KEY (id_chambre) references CHAMBRES(id)
            
        )
        """)


    def ajouter_client(self,client) : 
        db_client = (client._nom,client._prenom,client._adresse,client._mail,client._telephone)
        self._cursor.execute("""
    INSERT INTO CLIENTS(nom,prenom,adresse,mail,telephone) VALUES(?,?,?,?,?)""", db_client)

    def ajouter_chambre(self,chambre):
        db_chambre = (chambre._numero,chambre._capacite)
        self._cursor.execute("""
    INSERT INTO CHAMBRES(num_ch,capacite) VALUES(?,?)""", db_chambre)

    def ajouter_reservation(self, reservation) :
        db_reservation = (reservation._id_client, reservation._id_chambre, reservation._date_arrivee, reservation._date_depart, reservation._nb_occupants)
        self._cursor.execute("""INSERT INTO RESERVATIONS (id_client, id_chambre, date_arrivee, date_depart, nb_occupants) VALUES (?,?,?,?,?)""",db_reservation)



    def getClientById(self,_id) :

        self._cursor.execute(""" Select * from CLIENTS where Id = """+str(_id))
        db_client = self._cursor.fetchall()
        if len(db_client)== 0 :
            return None
        else :
            client = Client(db_client[0][1],db_client[0][2],db_client[0][3],db_client[0][4],db_client[0][5])
            client._id = db_client[0][0]
            return client


    def getChambreById(self,_id) :
        self._cursor.execute("""Select * from CHAMBRES where Id = """+str(_id))
        db_chambre = self._cursor.fetchall()
        if len(db_chambre)==0 :
            return None
        else:
            chambre = Chambre(db_chambre[0][1],db_chambre[0][2])
            chambre._id = db_chambre[0][0]
            return chambre 
    
    def getReservationById(self,_id) :

        self._cursor.execute("""Select * from RESERVATIONS where Id = """+str(_id))
        db_reservation = self._cursor.fetchall()
        if len(db_reservation)== 0 :
            return None
        else :
            reservation = Reservation(db_reservation[0][1],db_reservation[0][2],db_reservation[0][3],db_reservation[0][4],db_reservation[0][5])
            reservation._id = db_reservation[0][0]
            return reservation

    def getClientByMail(self,_mail) :

        self._cursor.execute(""" Select * from CLIENTS where Mail = '"""+_mail+"""'""")
        db_client = self._cursor.fetchall()
        if len(db_client)== 0 :
            return None
        else :
            client = Client(db_client[0][1],db_client[0][2],db_client[0][3],db_client[0][4],db_client[0][5])
            client._id = db_client[0][0]
            return client

    def getAllClients(self):
            clients = []
            self._cursor.execute("""Select * from CLIENTS ORDER BY Nom """)
            db_client = self._cursor.fetchall()
            for i in range(0,len(db_client)) :
                
                client = Client(db_client[i][1],db_client[i][2],db_client[i][3],db_client[i][4],db_client[0][5])
                client._id = db_client[i][0]
                clients.append(client)
               
            return clients
    
    def getAllChambres(self):
        chambres = []
        self._cursor.execute("""Select * from CHAMBRES ORDER BY Num_ch""")
        db_chambre = self._cursor.fetchall()
        for i in range(0,len(db_chambre)) :
                
                chambre = Chambre(db_chambre[i][1],db_chambre[i][2])
                chambre._id = db_chambre[i][0]
                chambres.append(chambre)
               
        return chambres


    def print_all(self):
        
        self._cursor.execute("""Select * from CLIENTS ORDER BY Nom """)
        db_resultat = self._cursor.fetchall()
        for i in range (0, len(db_resultat)):
            print (db_resultat[i])
        self._cursor.execute("""Select * from CHAMBRES ORDER BY Num_ch""")
        db_resultat = self._cursor.fetchall()
        for i in range (0,len(db_resultat)):
            print(db_resultat[i])
        self._cursor.execute("""Select * from RESERVATIONS ORDER BY Id""")
        db_resultat = self._cursor.fetchall()
        for i in range (0,len(db_resultat)):
            print(db_resultat[i])

    def modifier_client_byId (self,client):

        self._cursor.execute("""UPDATE CLIENTS
        SET nom = '"""+client._nom+"""',
        prenom = '"""+client._prenom+"""',
        adresse = '"""+client._adresse+"""',
        mail = '"""+client._mail+"""',
        telephone = '"""+client._telephone+"""'
        WHERE id = """+str(client._id))

    def supprimer_client_byId(self,client) :
        self._cursor.execute("""Delete from CLIENTS where id = """+str(client._id))

    def get_reservation_byDateandRoomNumber(self, date, id_chambre):
        
        self._cursor.execute("""Select * from RESERVATIONS where id_chambre = '""" + str(id_chambre) + """' 
                                and (julianday(date_arrivee) - julianday('""" + date + """'))<=0
                                and (julianday(date_depart) - julianday('""" + date + """'))>=0"""
                            )
        
        db_reservation = self._cursor.fetchall()
        if len(db_reservation)== 0 :
            return None
        else :
            reservation = Reservation(db_reservation[0][1],db_reservation[0][2],db_reservation[0][3],db_reservation[0][4],db_reservation[0][5])
            reservation._id = db_reservation[0][0]
            return reservation

    def get_id_byNumChambre (self, id_chambre) : 

        self._cursor.execute("Select id from CHAMBRES where num_ch = '""" + id_chambre + """' """)
        db_chambre = self._cursor.fetchall()
        if len(db_chambre)== 0 :
            return -1
        else :
            return db_chambre[0][0]
    



