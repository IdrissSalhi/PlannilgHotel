import sqlite3
import sys
sys.path.append("C:\\Users\\idris\\Desktop\\PlannilgHotel-master")
from Src.Model import *
from Src.Database import *
import time
import os


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

def run_tests(db) :

    file_name = "Bellevue_test_DB" + time.strftime("%Y%m%d_%H%M%S")
    f = open("Test/" + file_name + ".txt", "w")
    f.write("RAPPORT DE TESTS DU " + time.strftime("%d/%m/%Y") + " a " + time.strftime("%H:%M:%S") + "\n\n")
    f.close()

    test_create_tables(file_name, db)
















if os.path.exists('Test/TestBDD.db') :
    os.remove('Test/TestBDD.db')
else :
    print("pas trouve")
db = Database('Test/TestBDD.db')
run_tests(db)
db._connexion.close()