from copyreg import constructor
import re
import sqlite3
import sys
sys.path.append("C:\\Users\\idris\\Desktop\\PlannilgHotel-master")
from Src.Model import *
from Src.Database import *
import time
import os
from datetime import datetime

def reset_database(file_name, db):
    db.execute_query("""DROP TABLE IF EXISTS CHAMBRES;""")
    db.execute_query("""DROP TABLE IF EXISTS CLIENTS;""")
    db.execute_query("""DROP TABLE IF EXISTS RESERVATIONS;""")
    db.execute_query("""CREATE TABLE IF NOT EXISTS CHAMBRES (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            num_ch INTEGER UNIQUE,
            capacite Integer
        )""")
    db.execute_query("""CREATE TABLE IF NOT EXISTS CLIENTS(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            Nom TEXT,
            Prenom TEXT,
            Adresse TEXT,
            mail Text UNIQUE,
            telephone Text
        )
        """)
    db.execute_query("""CREATE TABLE IF NOT EXISTS RESERVATIONS (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            id_client INTEGER NOT NULL,
            id_chambre INTEGER NOT NULL,
            date_arrivee DATE,
            date_depart DATE,
            nb_occupants INTEGER NOT NULL,
            est_reglee INTEGER,
            origine TINYTEXT,
            FOREIGN KEY (id_client) references CLIENTS (id),
            FOREIGN KEY (id_chambre) references CHAMBRES(id))""")
    db.execute_query("""INSERT INTO CLIENTS(nom,prenom,adresse,mail,telephone) VALUES('Dupont', 'Emile', '13 rue Chappe', 'dupont@gmail.com', '0756958445')""")
    db.execute_query("""INSERT INTO CLIENTS(nom,prenom,adresse,mail,telephone) VALUES('Nourd', 'Ryan', '847 rue Lamarck', 'nourd@gmail.com', '0659856454')""")
    db.execute_query("""INSERT INTO CLIENTS(nom,prenom,adresse,mail,telephone) VALUES('Menard', 'Alice', '3 rue des Abbesses', 'menard@gmail.com', '0659874235')""")       
    db.execute_query("""INSERT INTO CHAMBRES(num_ch,capacite) VALUES(101,2)""")
    db.execute_query("""INSERT INTO CHAMBRES(num_ch,capacite) VALUES(304,1)""")
    db.execute_query("""INSERT INTO CHAMBRES(num_ch,capacite) VALUES(706,3)""")
    db.execute_query("""INSERT INTO RESERVATIONS(id_client, id_chambre, date_arrivee, date_depart, nb_occupants, est_reglee, origine) VALUES (1,2,'2022-06-05 00:00:00', '2022-06-09 00:00:00',1,1,'Booking')""")
    db.execute_query("""INSERT INTO RESERVATIONS(id_client, id_chambre, date_arrivee, date_depart, nb_occupants, est_reglee, origine) VALUES (2,3,'2024-07-01 00:00:00', '2024-07-06 00:00:00',3,0,'Fastbooking')""")
    db.execute_query("""INSERT INTO RESERVATIONS(id_client, id_chambre, date_arrivee, date_depart, nb_occupants, est_reglee, origine) VALUES (3,1,'2023-12-25 00:00:00', '2023-12-27 00:00:00',2,0,'')""")


def test_constructor(file_name, db) :
    all_passed = True
    f = open("Test/" + file_name + ".txt", "a")
    f.write("DEBUT TEST __init__ : \n")
    f.write("### SCENARIO 1 : chargement du fichier csv des chambres dans constructeur ###\n")
    res_count = db.execute_query(""" SELECT COUNT(*) FROM CHAMBRES""")
    if (len(res_count) >= 1 and len(res_count[0]) >=1 and res_count[0][0] == 39) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    res_chambre = db.execute_query(""" SELECT * FROM CHAMBRES WHERE num_ch = '205' """)
    if (len(res_chambre) == 1 and len(res_chambre[0])>=3 and res_chambre [0][2] == 3) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    res_chambre = db.execute_query(""" SELECT * FROM CHAMBRES WHERE num_ch = '103' """)
    if (len(res_chambre) == 1 and len(res_chambre[0])>=3 and res_chambre [0][2] == 2) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False    
    res_chambre = db.execute_query(""" SELECT * FROM CHAMBRES WHERE num_ch = '401' """)
    if (len(res_chambre) == 1 and len(res_chambre[0])>=3 and res_chambre [0][2] == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False   

    f.write("### FIN SCENARIO 1 ###\n")
    f.write("FIN TEST __init__ \n")
    f.close()
    return all_passed

def test_create_tables(file_name, db) :
    all_passed = True
    f = open("Test/" + file_name + ".txt", "a")
    f.write("DEBUT TEST create_tables : \n")
    f.write("### SCENARIO 1 : chargement constructeur database ###\n")
    res = db.execute_query("""SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;""")
    if(len(res) == 4) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    if(len([item for item in res if "CHAMBRES" in item]) > 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    if(len([item for item in res if "CLIENTS" in item]) > 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    if(len([item for item in res if "RESERVATIONS" in item]) > 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    f.write("### FIN SCENARIO 1 ###\n")

    f.write("### SCENARIO 2 : create_tables avec table manquante ###\n")
    db.execute_query("""DROP TABLE CHAMBRES;""")
    db.execute_query("""DROP TABLE CLIENTS;""")
    db.execute_query("""DROP TABLE RESERVATIONS;""")
    res = db.execute_query("""SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;""")
    if(len(res) == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    if(len([item for item in res if "CHAMBRES" in item]) == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    if(len([item for item in res if "CLIENTS" in item]) == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    if(len([item for item in res if "RESERVATIONS" in item]) == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False

    db.create_tables()
    res = db.execute_query("""SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;""")
    if(len(res) == 4) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False

    if(len([item for item in res if "CHAMBRES" in item]) > 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    if(len([item for item in res if "CLIENTS" in item]) > 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    if(len([item for item in res if "RESERVATIONS" in item]) > 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    f.write("### FIN SCENARIO 2 ###\n")

    f.write("FIN TEST create_tables \n")
    f.close()
    return all_passed

def test_ajouter_client (file_name, db):
    all_passed = True
    f = open("Test/" + file_name + ".txt", "a")
    f.write("DEBUT TEST ajouter_client : \n")
    db.execute_query(""" DELETE FROM  CLIENTS """)
    f.write("### SCENARIO 1 : Ajout d'un client sur db vide ### \n")
    res_count = db.execute_query(""" SELECT COUNT(*) FROM CLIENTS""")
    res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE nom = 'Dupond' """)
    if(len(res_count) >= 1 and len(res_count[0]) >= 1 and res_count[0][0] == 0 and res_client == []) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    client = Client("Dupond", "Antoine", "13 rue labas", "dupond@gmail.com", "0654859632")
    db.ajouter_client(client)
    res_count = db.execute_query(""" SELECT COUNT(*) FROM CLIENTS""")
    res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE nom = 'Dupond' """)
    if(len(res_count) >= 1 and len(res_count[0]) >= 1 and res_count[0][0] == 1 and res_client != []) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    if (len(res_client) >= 1 and len(res_client[0]) >= 6 and res_client[0][1] == "Dupond" and res_client[0][2] == "Antoine" and res_client[0][3] == "13 rue labas"and res_client[0][4] == "dupond@gmail.com" and res_client[0][5] == "0654859632") :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    f.write("### FIN SCENARIO 1 ###\n")
    f.write("### SCENARIO 2 : Ajout d'un deuxieme client ### \n")
    client = Client("Dupont", "Emile", "13 rue Ici", "dupont@gmail.com", "0756958445")
    db.ajouter_client(client)
    res_count = db.execute_query(""" SELECT COUNT(*) FROM CLIENTS""")
    res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE nom = 'Dupont' """)
    if(len(res_count) >= 1 and len(res_count[0]) >= 1 and res_count[0][0] == 2 and len(res_client) == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    if (len(res_client) >= 1 and len(res_client[0]) >= 6 and res_client[0][1] == "Dupont" and res_client[0][2] == "Emile" and res_client[0][3] == "13 rue Ici"and res_client[0][4] == "dupont@gmail.com" and res_client[0][5] == "0756958445") :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    f.write("### FIN SCENARIO 2 ###\n")
    f.write("FIN TEST ajouter_client \n")
    f.close()
    return all_passed

def test_ajouter_chambre (file_name, db) :
    all_passed = True
    f = open("Test/" + file_name + ".txt", "a")
    f.write("DEBUT TEST ajouter_chambre : \n")
    f.write("### SCENARIO 1 : Ajout d'une chambre sur db vide ### \n")
    res_count = db.execute_query(""" SELECT COUNT(*) FROM CHAMBRES""")
    if(len(res_count) >= 1 and len(res_count[0]) >= 1 and res_count[0][0] == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
    chambre =  Chambre (801, 2)
    db.ajouter_chambre (chambre)
    res_count = db.execute_query(""" SELECT COUNT(*) FROM CHAMBRES""")
    if(len(res_count) >= 1 and len(res_count[0]) >= 1 and res_count[0][0] == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
    res_chambre = db.execute_query(""" SELECT * FROM CHAMBRES WHERE num_ch = '801' """)
    if (len(res_chambre) == 1 and len(res_chambre[0]) >= 3  and res_chambre [0][2] == 2) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False  
    f.write ("### FIN SCENARIO 1 ###\n")
    f.write("### SCENARIO 2 : AJOUT D'UN DEUXIEME CHAMBRE ###\n")
    chambre =  Chambre (805, 3)
    db.ajouter_chambre (chambre)
    res_count = db.execute_query(""" SELECT COUNT(*) FROM CHAMBRES""")
    if(len(res_count) >= 1 and len(res_count[0]) >= 1 and res_count[0][0] == 2) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
    res_chambre = db.execute_query(""" SELECT * FROM CHAMBRES WHERE num_ch = '805' """)
    if (len(res_chambre) == 1 and len(res_chambre[0]) >= 3 and res_chambre [0][2] == 3) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False  
    f.write ("### FIN SCENARIO 2 ###\n")
    f.write("FIN TEST ajouter_client \n")
    f.close()
    return all_passed



def test_ajouter_reservation (file_name, db) :
    all_passed = True
    f = open("Test/" + file_name + ".txt", "a")
    f.write("DEBUT TEST ajouter_reservation : \n")
    f.write("### SCENARIO 1 : Ajout d'une reservation ### \n")
    res_count = db.execute_query(""" SELECT COUNT(*) FROM RESERVATIONS""")
    if(len(res_count) >= 1 and len(res_count[0]) >= 1 and res_count[0][0] == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
    reservation = Reservation(1, 2, "20220605", "20220609", 2, True, "Booking" )
    db.ajouter_reservation(reservation)
    res_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS """)
    if(len(res_reservation) == 1 and len(res_count[0]) >= 8 and res_reservation[0][1] == 1 and res_reservation[0][2] == 2 and res_reservation[0][3] == 20220605 and res_reservation[0][4] == 20220609 and res_reservation[0][5] == 2 and res_reservation[0][6] == True and res_reservation[0][7] == "Booking" ) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
    f.write ("### FIN SCENARIO 1 ###\n")
    f.write("### SCENARIO 2 : Ajout d'une deuxieme et troisieme reservations ### \n")
    reservation = Reservation(2, 1, "20220703", "20220709", 1, False, "Fastbooking" )
    db.ajouter_reservation(reservation)
    res_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS """)
    if(len(res_reservation) == 2 and len(res_reservation[1]) >= 8 and res_reservation[1][1] == 2 and res_reservation[1][2] == 1 and res_reservation[1][3] == 20220703 and res_reservation[1][4] == 20220709 and res_reservation[1][5] == 1 and res_reservation[1][6] == False and res_reservation[1][7] == "Fastbooking" ) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
    reservation = Reservation(2, 2, "20231215", "20231220", 2, True, "" )
    db.ajouter_reservation(reservation)
    res_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS """)
    if(len(res_reservation) == 3 and len(res_reservation[2]) >= 8 and res_reservation[2][1] == 2 and res_reservation[2][2] == 2 and res_reservation[2][3] == 20231215 and res_reservation[2][4] == 20231220 and res_reservation[2][5] == 2 and res_reservation[2][6] == True and res_reservation[2][7] == "" ) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
    f.write ("### FIN SCENARIO 2 ###\n")
    f.write("FIN TEST ajouter_reservation \n")
    f.close()
    return all_passed

def test_modifier_client_byId(file_name, db) :
    reset_database(file_name,db)
    all_passed = True
    f = open("Test/" + file_name + ".txt", "a")
    f.write("DEBUT TEST modifier_client_byId : \n")
    f.write("### SCENARIO 1 : modification client 1 ### \n")
    res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Dupont' AND Prenom = 'Emile' AND Adresse = '13 rue Chappe' AND mail = 'dupont@gmail.com' AND telephone = '0756958445' """)
    if(len(res_client) == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    test_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Prix' AND Prenom = 'Frank' AND Adresse = '50 rue Achat' AND mail = 'prix@gmail.com' AND telephone = '0656985425' """)
    if(len(test_client) == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    if (len(res_client) >= 1 and len(res_client[0]) >= 1) :
        id_client = res_client[0][0]
        new_client = Client("Prix","Frank", "50 rue Achat", "prix@gmail.com", "0656985425")
        new_client._id = id_client
        db.modifier_client_byId(new_client)
        res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Dupont' AND Prenom = 'Emile' AND Adresse = '13 rue Chappe' AND mail = 'dupont@gmail.com' AND telephone = '0756958445' """)
        if(len(res_client) == 0) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        test_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Prix' AND Prenom = 'Frank' AND Adresse = '50 rue Achat' AND mail = 'prix@gmail.com' AND telephone = '0656985425' """)
        if(len(test_client) == 1) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        if(len(test_client) >= 1 and len(test_client[0]) >= 1 and test_client[0][0] == id_client) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
    f.write ("### FIN SCENARIO 1 ###\n")

    f.write("### SCENARIO 2 : modification client 2 ### \n")
    res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Nourd' AND Prenom = 'Ryan' AND Adresse = '847 rue Lamarck' AND mail = 'nourd@gmail.com' AND telephone = '0659856454' """)
    if(len(res_client) == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    test_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Four' AND Prenom = 'Carl' AND Adresse = '25 rue Promo' AND mail = 'four@gmail.com' AND telephone = '0659865478' """)
    if(len(test_client) == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    if(len(res_client) >= 1 and len(res_client[0]) >= 1) :
        id_client = res_client[0][0]
        new_client = Client("Four","Carl", "25 rue Promo", "four@gmail.com", "0659865478")
        new_client._id = id_client
        db.modifier_client_byId(new_client)
        res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Nourd' AND Prenom = 'Ryan' AND Adresse = '847 rue Lamarck' AND mail = 'nourd@gmail.com' AND telephone = '0659856454' """)
        if(len(res_client) == 0) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        test_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Four' AND Prenom = 'Carl' AND Adresse = '25 rue Promo' AND mail = 'four@gmail.com' AND telephone = '0659865478' """)
        if(len(test_client) == 1) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        if(len(test_client) >= 1 and len(test_client[0]) >= 1 and test_client[0][0] == id_client) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        
    f.write ("### FIN SCENARIO 2 ###\n")
    f.write("FIN TEST modifier_client_byId \n")
    f.close()
    return all_passed

def test_supprimer_client_byId (file_name, db) :
    reset_database(file_name,db)
    all_passed = True
    f = open("Test/" + file_name + ".txt", "a")
    f.write("DEBUT TEST supprimer_client_byId : \n")
    f.write("### SCENARIO 1 : supression client 1 ### \n")
    res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Dupont' AND Prenom = 'Emile' AND Adresse = '13 rue Chappe' AND mail = 'dupont@gmail.com' AND telephone = '0756958445' """)
    if(len(res_client) == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False 
    if(len(res_client) >= 1 and len(res_client[0]) >= 1) :
        new_client = Client("x","x", "x", "x", "x")
        new_client._id = res_client[0][0]
        db.supprimer_client_byId(new_client)
        res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Dupont' AND Prenom = 'Emile' AND Adresse = '13 rue Chappe' AND mail = 'dupont@gmail.com' AND telephone = '0756958445' """)
        if(len(res_client) == 0) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
    f.write ("### FIN SCENARIO 1 ###\n")

    f.write("### SCENARIO 2 : suppression client 2 ### \n")
    res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Nourd' AND Prenom = 'Ryan' AND Adresse = '847 rue Lamarck' AND mail = 'nourd@gmail.com' AND telephone = '0659856454' """)
    if(len(res_client) == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    
    if(len(res_client) >= 1 and len(res_client[0]) >= 1) :
        new_client = Client("x","x", "x", "x", "x")
        new_client._id = res_client[0][0]  
        db.supprimer_client_byId(new_client)
        res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Nourd' AND Prenom = 'Ryan' AND Adresse = '847 rue Lamarck' AND mail = 'nourd@gmail.com' AND telephone = '0659856454' """)
        if(len(res_client) == 0) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
    f.write ("### FIN SCENARIO 2 ###\n")
    f.write("### SCENARIO 3 :  verification table vide ### \n")
    res_client = db.execute_query(""" SELECT * FROM CLIENTS WHERE Nom = 'Menard' AND Prenom = 'Alice' AND Adresse = '3 rue des Abbesses' AND mail = 'menard@gmail.com' AND telephone = '0659874235' """)
    if(len(res_client) >= 1 and len(res_client[0]) >= 1) :
        new_client = Client("x","x", "x", "x", "x")
        new_client._id = res_client[0][0]
        db.supprimer_client_byId(new_client)
        res_client = db.execute_query(""" SELECT * FROM CLIENTS """)
        if(len(res_client) == 0) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
    else :
        f.write("FAIL \n")
        all_passed = False
    f.write ("### FIN SCENARIO 3 ###\n")
    f.write("FIN TEST supprimer_client_byId \n")
    f.close()
    return all_passed

def test_modifier_reservation_byID(file_name,db):
    reset_database(file_name,db)
    all_passed = True
    f = open("Test/" + file_name + ".txt", "a")
    f.write("DEBUT TEST modifier_reservation_byId : \n")
    f.write("### SCENARIO 1 : modification reservation 1 ### \n")
    res_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS WHERE id_client = 1 AND id_chambre = 2 AND date_arrivee = '2022-06-05 00:00:00' AND date_depart = '2022-06-09 00:00:00' AND nb_occupants = 1 AND est_reglee = 1 AND origine = 'Booking' """)
    if(len(res_reservation) == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    test_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS WHERE id_client = 1 AND id_chambre = 1 AND date_arrivee = '2024-05-08 00:00:00' AND date_depart = '2024-05-11 00:00:00' AND nb_occupants = 2 AND est_reglee = 0 AND origine = 'Fastbooking' """)
    if(len(test_reservation) == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    if (len(res_reservation)>=1 and len(res_reservation[0])>=2) :
        id_reservation = res_reservation[0][0]
        id_client_resa = res_reservation[0][1]
        new_reservation = Reservation(id_client_resa,1,datetime.strptime("20240508", "%Y%m%d"),datetime.strptime("20240511", "%Y%m%d"), 2, 0, "Fastbooking")
        new_reservation._id = id_reservation
        db.modifier_reservation_byId(new_reservation)
        res_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS WHERE id_client = 1 AND id_chambre = 2 AND date_arrivee = '2022-06-05 00:00:00' AND date_depart = '2022-06-09 00:00:00' AND nb_occupants = 1 AND est_reglee = 1 AND origine = 'Booking' """)
        if(len(res_reservation) == 0) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        test_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS WHERE id_client = 1 AND id_chambre = 1 AND date_arrivee = '2024-05-08 00:00:00' AND date_depart = '2024-05-11 00:00:00' AND nb_occupants = 2 AND est_reglee = 0 AND origine = 'Fastbooking' """)
        if(len(test_reservation) == 1) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        if(len(test_reservation) == 1 and len(test_reservation[0]) >= 1 and test_reservation[0][0] == id_reservation) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
    else :
        f.write("FAIL \n")
        all_passed = False
    f.write ("### FIN SCENARIO 1 ###\n")

    f.write("### SCENARIO 2 : modification reservation 2 ### \n")
    res_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS WHERE id_client = 2 AND id_chambre = 3 AND date_arrivee = '2024-07-01 00:00:00' AND date_depart = '2024-07-06 00:00:00' AND nb_occupants = 3 AND est_reglee = 0 AND origine = 'Fastbooking' """)
    if(len(res_reservation) == 1) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    test_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS WHERE id_client = 2 AND id_chambre = 1 AND date_arrivee = '2025-07-11 00:00:00' AND date_depart = '2025-07-15 00:00:00' AND nb_occupants = 2 AND est_reglee = 1 AND origine = '' """)
    if(len(test_reservation) == 0) :
        f.write("OK \n")
    else :
        f.write("FAIL \n")
        all_passed = False
    if (len(res_reservation)>=1 and len(res_reservation[0])>=2) :
        id_reservation = res_reservation[0][0]
        id_client_resa = res_reservation[0][1]
        new_reservation = Reservation(id_client_resa,1,datetime.strptime("20250711", "%Y%m%d"),datetime.strptime("20250715", "%Y%m%d"), 2, 1, "")
        new_reservation._id = id_reservation
        db.modifier_reservation_byId(new_reservation)
        res_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS WHERE id_client = 2 AND id_chambre = 3 AND date_arrivee = '2024-07-01 00:00:00' AND date_depart = '2024-07-06 00:00:00' AND nb_occupants = 3 AND est_reglee = 0 AND origine = 'Fastbooking' """)
        if(len(res_reservation) == 0) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        test_reservation = db.execute_query(""" SELECT * FROM RESERVATIONS WHERE id_client = 2 AND id_chambre = 1 AND date_arrivee = '2025-07-11 00:00:00' AND date_depart = '2025-07-15 00:00:00' AND nb_occupants = 2 AND est_reglee = 1 AND origine = '' """)
        if(len(test_reservation) == 1) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
        if(len(test_reservation) == 1 and len(test_reservation[0]) >= 1 and test_reservation[0][0] == id_reservation) :
            f.write("OK \n")
        else :
            f.write("FAIL \n")
            all_passed = False
    else :
        f.write("FAIL \n")
        all_passed = False
    f.write ("### FIN SCENARIO 2 ###\n")
    
    f.write("FIN TEST modifier_reservation_byId \n")
    f.close()
    return all_passed

def run_tests(db) :

    file_name = "Bellevue_test_DB" + time.strftime("%Y%m%d_%H%M%S")
    rapport = "Rapport_test_DB" + time.strftime("%Y%m%d_%H%M%S")
    f = open("Test/" + file_name + ".txt", "w")
    fr = open("Test/" + rapport + ".txt", "w")
    f.write("RAPPORT DE TESTS DU " + time.strftime("%d/%m/%Y") + " a " + time.strftime("%H:%M:%S") + "\n\n")
    f.close()
    validation = True
    if (not test_constructor(file_name, db)):
        validation = False
        fr.write("Constructor FAILED \n")
    if (not test_create_tables(file_name, db)):
        validation = False
        fr.write("Create tables FAILED \n")
    if (not test_ajouter_client(file_name, db)):
        validation = False
        fr.write("Ajouter clients FAILED \n")
    if (not test_ajouter_chambre(file_name, db)):
        validation = False
        fr.write("Ajouter chambres FAILED \n")
    if (not test_ajouter_reservation(file_name, db)):
        validation = False
        fr.write("Ajouter reservations FAILED \n")
    if (not test_modifier_client_byId(file_name, db)):
        validation = False
        fr.write("Modifier clients FAILED \n")
    if (not test_supprimer_client_byId(file_name, db)):
        validation = False
        fr.write("Supprimer clients FAILED \n")
    if (not test_modifier_reservation_byID(file_name, db)):
        validation = False
        fr.write("Modifier reservations FAILED \n")


    if (validation == True) :
        fr.write("################ \n ALL PASSED \n################")

    fr.close()


















if os.path.exists('Test/TestBDD.db') :
    os.remove('Test/TestBDD.db')
else :
    print("pas trouve")
db = Database('Test/TestBDD.db')
run_tests(db)
db._connexion.close()