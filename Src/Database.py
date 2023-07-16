import sqlite3
from Src.Model import *
from datetime import datetime
import calendar

class Database : 

    def __init__(self, db_file) :
        self._connexion = sqlite3.connect(db_file)
        self._cursor = self._connexion.cursor()
        self.create_tables()
        if len(self.getAllChambres())== 0 :
            f_chambres= open("DB/Plan_Hotel.csv", "r")
            lignes = f_chambres.readlines()
            for i in range (1, len(lignes)) : 
                temp = lignes[i].strip('\n').split(";")
                self.ajouter_chambre(Chambre(int(temp[0]),int(temp[1])))
            
            f_chambres.close()

    def execute_query(self, query) :
        self._cursor.execute(query)
        self._connexion.commit()
        return self._cursor.fetchall()
    
    
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
            accompte INTEGER,
            origine TINYTEXT,
            id_facture INTEGER NOT NULL,
            FOREIGN KEY (id_client) references CLIENTS (id),
            FOREIGN KEY (id_chambre) references CHAMBRES(id),
            FOREIGN KEY (id_facture) references FACTURE(id)
            
            
        )
        """)
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS COUTS_JOUR(
            id_reservation INTEGER NOT NULL,
            date_jour DATE,
            total_chambre INTEGER NOT NULL,
            total_petit_dej INTEGER NOT NULL,
            total_bar  INTEGER NOT NULL,
            total_telephone INTEGER NOT NULL,
            total_taxe_sejour INTEGER NOT NULL,
            PRIMARY KEY (id_reservation, date_jour),
            FOREIGN KEY (id_reservation) references RESERVATIONS (id)
     
        )
        """)
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS FACTURE(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            numero_facture INTEGER NOT NULL,
            date_emission DATE,
            date_de_reglement DATE,
            fichier_html BLOB
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
        
        db_reservation = (reservation._id_client, reservation._id_chambre, reservation._date_arrivee, reservation._date_depart, reservation._nb_occupants, reservation._accompte, reservation._origine, -1)
        self._cursor.execute("""INSERT INTO RESERVATIONS (id_client, id_chambre, date_arrivee, date_depart, nb_occupants, accompte, origine, id_facture) VALUES (?,?,?,?,?,?,?,?)""",db_reservation)
        self._cursor.execute("""SELECT LAST_INSERT_ROWID(); """)
        self._connexion.commit()
        id_resa = self._cursor.fetchall()[0][0]
        for cj in reservation._couts :
            db_cj = (id_resa, cj._date_jour, cj._total_chambre, 
                     cj._total_petit_dej,  cj._total_bar, 
                     cj._total_telephone,  cj._total_taxe_sejour)
            self._cursor.execute(""" INSERT INTO COUTS_JOUR (id_reservation, date_jour, total_chambre, 
                                     total_petit_dej, total_bar, total_telephone,
                                     total_taxe_sejour) VALUES (?,?,?,?,?,?,?) """, db_cj) 
            self._connexion.commit()
        if reservation._facture:
            self.modifier_facture_byId(reservation._facture._id)
        

        return id_resa
        
   


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

        self._cursor.execute("""Select * from RESERVATIONS where Id = """ + str(_id))
        db_reservation = self._cursor.fetchall()
        if len(db_reservation)== 0 :
            return None
        else :
            reservation = Reservation(db_reservation[0][1],db_reservation[0][2],datetime.strptime(db_reservation[0][3],"%Y-%m-%d %H:%M:%S"),datetime.strptime(db_reservation[0][4],"%Y-%m-%d %H:%M:%S"),db_reservation[0][5],db_reservation[0][6], db_reservation[0][7])
            reservation._id = db_reservation[0][0]
            self._cursor.execute("""Select * from COUTS_JOUR where id_reservation = """ + str(_id))
            db_couts_jour = self._cursor.fetchall()
            for i in range (0, len(db_couts_jour)) :
                couts_jour = Couts_jour(datetime.strptime(db_couts_jour[i][1],"%Y-%m-%d %H:%M:%S"), db_couts_jour[i][2], db_couts_jour[i][3], db_couts_jour[i][4], db_couts_jour[i][5], db_couts_jour[i][6])
                reservation._couts.append(couts_jour)
            if db_reservation[0][8] != -1:
                reservation._facture = self.getFactureById(db_reservation[0][8])
                
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
            reservation = Reservation(db_reservation[0][1],db_reservation[0][2],datetime.strptime(db_reservation[0][3],"%Y-%m-%d %H:%M:%S"),datetime.strptime(db_reservation[0][4],"%Y-%m-%d %H:%M:%S"),db_reservation[0][5],db_reservation[0][6], db_reservation[0][7])
            reservation._id = db_reservation[0][0]
            self._cursor.execute("""Select * from COUTS_JOUR where id_reservation = """ + str(reservation._id))
            db_couts_jour = self._cursor.fetchall()
            for i in range (0, len(db_couts_jour)) :
                couts_jour = Couts_jour(datetime.strptime(db_couts_jour[i][1],"%Y-%m-%d %H:%M:%S"), db_couts_jour[i][2], db_couts_jour[i][3], db_couts_jour[i][4], db_couts_jour[i][5], db_couts_jour[i][6])
                reservation._couts.append(couts_jour)
            if db_reservation[0][8] != -1:
                reservation._facture = self.getFactureById(db_reservation[0][8])
            
            return reservation

    def get_id_byNumChambre (self, id_chambre) : 
        self._cursor.execute("Select id from CHAMBRES where num_ch = """ + str(id_chambre) + """ """)
        db_chambre = self._cursor.fetchall()
        if len(db_chambre)== 0 :
            return -1
        else :
            return db_chambre[0][0]
    
    def modifier_reservation_byId (self, reservation) :
        facture = -1 
        if reservation._facture:
            facture = reservation._facture._id
        self._cursor.execute("""UPDATE RESERVATIONS
        SET date_arrivee = '"""+ str(reservation._date_arrivee.strftime("%Y-%m-%d %H:%M:%S")) +"""',
        date_depart = '"""+ str(reservation._date_depart.strftime("%Y-%m-%d %H:%M:%S")) +"""',
        nb_occupants = '"""+ str(reservation._nb_occupants) +"""',
        accompte = '"""+ str(reservation._accompte) +"""',
        origine = '"""+ reservation._origine +"""',
        id_facture = """+ str(facture)  +""",
        id_chambre = '"""+ str(reservation._id_chambre) +"""'
        WHERE id = """+ str(reservation._id))
        self._connexion.commit()
        self._cursor.execute(""" DELETE FROM COUTS_JOUR WHERE id_reservation = '""" + str(reservation._id) + """'""")
        self._connexion.commit()
        for cj in reservation._couts :
            db_cj = (reservation._id, cj._date_jour, cj._total_chambre,
                     cj._total_petit_dej, cj._total_bar, cj._total_telephone, cj._total_taxe_sejour)
            self._cursor.execute(""" INSERT INTO COUTS_JOUR (id_reservation, date_jour, total_chambre, 
                                     total_petit_dej, total_bar, total_telephone,
                                     total_taxe_sejour) VALUES (?,?,?,?,?,?,?) """, db_cj) 
            self._connexion.commit()
        if reservation._facture:
            self.modifier_facture_byId(reservation._facture)

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
        self._cursor.execute("""Delete from COUTS_JOUR where id_reservation = """+str(reservation._id))
        if reservation._facture:
            self._cursor.execute("""Delete from FACTURE where id = """+str(reservation._facture._id))
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
        self._cursor.execute("""DELETE from COUTS_JOUR WHERE id_reservation IN (SELECT id FROM RESERVATIONS WHERE id_client = '""" +str(client._id)+ """')"""  )
        self._cursor.execute("""SELECT id_facture from RESERVATION where  id_client = """+str(client._id))
        factures = self._cursor.fetchall()
        for k in factures:
            self._cursor.execute("""Delete from FACTURE where id = """+str(k[0]))
        
        self._cursor.execute("""DELETE from RESERVATIONS WHERE id_client = """+str(client._id))       

        self._connexion.commit()

    
    def ajouter_facture(self, facture):
        date_emission = facture._date_emission
        debut_mois = date_emission.replace(day = 1, hour =0, minute = 0 , second = 0)
        fin_mois = date_emission.replace(day = calendar.monthrange(date_emission.year,date_emission.month)[1] , hour =23, minute = 59 , second = 59)
        self._cursor.execute("""SELECT * from FACTURE where date_emission >=
                             julianday('""" + debut_mois.strftime("%Y-%m-%d %H:%M:%S") + """')  and date_emission <=
                             julianday('""" + fin_mois.strftime("%Y-%m-%d %H:%M:%S") + """') ORDER BY date_emission""")
        
        db_factures = self._cursor.fetchall()
        num_fac = 1
        if db_factures != []:
            num_fac = db_factures[-1][1] + 1
        db_facture = (num_fac, facture._date_emission, None, facture._fichier_html)
        
        self._cursor.execute("""
        INSERT INTO FACTURE(numero_facture, date_emission, date_de_reglement, fichier_html) VALUES(?,?,?,?)""", db_facture)
        self._cursor.execute("""SELECT LAST_INSERT_ROWID(); """)
        self._connexion.commit()
        id_facture = self._cursor.fetchall()[0][0]
        
        return id_facture


    def getFactureById(self, _id):
        
        self._cursor.execute("""Select * from FACTURE where id = """+str(_id))
        db_facture = self._cursor.fetchall()
        if len(db_facture)==0 :
            return None
        else:
            facture = Facture(db_facture[0][4])
            facture._id = _id
            facture._numero_facture = db_facture[0][1]
            facture._date_emission = datetime.strptime(db_facture[0][2],"%Y-%m-%d %H:%M:%S")    
            facture._date_de_reglement = datetime.strptime(db_facture[0][3],"%Y-%m-%d %H:%M:%S") if db_facture[0][3] else None
            
            return facture 
   
   
    def modifier_facture_byId(self, facture): 
  
        date_reg = None
        if facture._date_de_reglement:
            date_reg = facture._date_de_reglement
        self._cursor.execute("""UPDATE FACTURE
        SET numero_facture = """+ str(facture._numero_facture) +""",
        date_emission = '"""+ str(facture._date_emission.strftime("%Y-%m-%d %H:%M:%S")) +"""',
        date_de_reglement = ?,
        fichier_html = ?
        WHERE id = """+ str(facture._id),(date_reg, facture._fichier_html))
        self._connexion.commit()
       
     #fichier_html = ?    WHERE id = """+ str(facture._id),(date_reg, facture._fichier_html))
   