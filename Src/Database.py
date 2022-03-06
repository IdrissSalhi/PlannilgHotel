import sqlite3
from Src.Model import *


class Database : 

    def __init__(self) :
        self._connexion = sqlite3.connect('DB/HotelBDD.db')
        self._cursor = self._connexion.cursor()
        self.create_tables()
        if len(self.getAllChambres())== 0 :
            f_chambres= open("DB/Plan_Hotel.csv", "r")
            lignes = f_chambres.readlines()
            for i in range (1, len(lignes)) : 
                temp = lignes[i].strip('\n').split(";")
                self.ajouter_chambre(Chambre(int(temp[0]),int(temp[1])))
            
            f_chambres.close()



    
    
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
            est_reglee INTEGER,
            FOREIGN KEY (id_client) references CLIENTS (id),
            FOREIGN KEY (id_chambre) references CHAMBRES(id)
            
        )
        """)
        self._connexion.commit()
        


    def ajouter_client(self,client) : 
        db_client = (client._nom,client._prenom,client._adresse,client._mail,client._telephone)
        self._cursor.execute("""
    INSERT INTO CLIENTS(nom,prenom,adresse,mail,telephone) VALUES(?,?,?,?,?)""", db_client)
        self._connexion.commit()



    def ajouter_chambre(self,chambre):
        db_chambre = (chambre._numero,chambre._capacite)
        self._cursor.execute("""
    INSERT INTO CHAMBRES(num_ch,capacite) VALUES(?,?)""", db_chambre)
        self._connexion.commit()

    def ajouter_reservation(self, reservation) :
        db_reservation = (reservation._id_client, reservation._id_chambre, reservation._date_arrivee, reservation._date_depart, reservation._nb_occupants, reservation._est_reglee)
        self._cursor.execute("""INSERT INTO RESERVATIONS (id_client, id_chambre, date_arrivee, date_depart, nb_occupants, est_reglee) VALUES (?,?,?,?,?,?)""",db_reservation)
        self._cursor.execute("""SELECT LAST_INSERT_ROWID(); """)
        self._connexion.commit()
        return self._cursor.fetchall()[0][0]
        
   


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
            reservation = Reservation(db_reservation[0][1],db_reservation[0][2],datetime.strptime(db_reservation[0][3],"%Y-%m-%d %H:%M:%S"),datetime.strptime(db_reservation[0][4],"%Y-%m-%d %H:%M:%S"),db_reservation[0][5],db_reservation[0][6])
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
                
                chambre = Chambre(int(db_chambre[i][1]),int(db_chambre[i][2]))
                chambre._id =int(db_chambre[i][0]) 
                chambres.append(chambre)
               
        return chambres


    def modifier_client_byId (self,client):

        self._cursor.execute("""UPDATE CLIENTS
        SET nom = '"""+client._nom+"""',
        prenom = '"""+client._prenom+"""',
        adresse = '"""+client._adresse+"""',
        mail = '"""+client._mail+"""',
        telephone = '"""+client._telephone+"""'
        WHERE id = """+str(client._id))
        self._connexion.commit()

    def supprimer_client_byId(self,client) :
        self._cursor.execute("""Delete from CLIENTS where id = """+str(client._id))
        self._connexion.commit()

    def get_reservation_byDateandRoomId(self, date, id_chambre):
        self._cursor.execute("""Select * from RESERVATIONS where id_chambre = """ + str(id_chambre) + """
                                and (julianday(date_arrivee) - julianday('""" + date + """'))<=0
                                and (julianday(date_depart) - julianday('""" + date + """'))>=0"""
                            )
        
        db_reservation = self._cursor.fetchall()
        if len(db_reservation)== 0 :
            return None
        else :
            reservation = Reservation(db_reservation[0][1],db_reservation[0][2],datetime.strptime(db_reservation[0][3],"%Y-%m-%d %H:%M:%S"),datetime.strptime(db_reservation[0][4],"%Y-%m-%d %H:%M:%S"),db_reservation[0][5],db_reservation[0][6])
            reservation._id = db_reservation[0][0]

            return reservation

    def get_id_byNumChambre (self, id_chambre) : 
        self._cursor.execute("Select id from CHAMBRES where num_ch = """ + str(id_chambre) + """ """)
        db_chambre = self._cursor.fetchall()
        if len(db_chambre)== 0 :
            return -1
        else :
            return db_chambre[0][0]
    
    def modifier_reservation_byId (self, reservation) :

        self._cursor.execute("""UPDATE RESERVATIONS
        SET date_arrivee = '"""+str(reservation._date_arrivee.strftime("%Y-%m-%d %H:%M:%S"))+"""',
        date_depart = '"""+str(reservation._date_depart.strftime("%Y-%m-%d %H:%M:%S"))+"""',
        nb_occupants = '"""+str(reservation._nb_occupants)+"""',
        est_reglee = '"""+str(reservation._est_reglee)+"""',
        id_chambre = '"""+str(reservation._id_chambre)+"""'
        WHERE id = """+str(reservation._id))
        self._connexion.commit()
        



    def get_capacite_max_chambre(self) : 
        self._cursor.execute("""SELECT MAX(capacite) as max_capacite
        FROM CHAMBRES;""")
        max = self._cursor.fetchall()
        if len(max)== 0 :
            return 0
        else :
            return max[0][0]
        

    def supprimer_resa_byId(self,reservation) :
        self._cursor.execute("""Delete from RESERVATIONS where id = """+str(reservation._id))
        self._connexion.commit()

    def get_chambre_dispo(self, reservation) :
        self._cursor.execute(""" Select num_ch from CHAMBRES INNER JOIN RESERVATIONS on RESERVATIONS.id_chambre = CHAMBRES.id where """ +str(reservation._id)+ """ <> RESERVATIONS.id and
            julianday('""" + reservation._date_depart.strftime("%Y-%m-%d %H:%M:%S") + """') - julianday(date_arrivee) >= 0 and
            julianday('""" + reservation._date_arrivee.strftime("%Y-%m-%d %H:%M:%S") + """') - julianday(date_depart) <= 0 
            """)
        chambres_prises_sql = self._cursor.fetchall()
        chambres_prises = []
        for i in chambres_prises_sql :
            chambres_prises.append(i[0])
       
        self._cursor.execute("""Select num_ch from CHAMBRES where capacite >= """ + str(reservation._nb_occupants) )
        num_ch_selected = self._cursor.fetchall()
        resultat = []
        for i in num_ch_selected :
            resultat.append(i[0])
        
        for i in chambres_prises :
            if i in resultat :
                resultat.remove(i)
                
        return resultat

    def supprimer_resa_byClient(self,client):
        self._cursor.execute("""DELETE from RESERVATIONS WHERE id_client = """+str(client._id))
        self._connexion.commit()

    def print_reservations(self):
        self._cursor.execute("""SELECT * from RESERVATIONS""")
        res = self._cursor.fetchall()
        for i in res :
            print(i)