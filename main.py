from Model import *
from Controller import *
from View import *
from Database import *

db = Database()
controller = Controller(db)
view = View(controller)
db.create_tables()


controller.ajouter_client( Client("LOPO","Polo","15 rue moliere","polo@efrei.net","0605896412"))
controller.ajouter_client( Client("EOL","Leo","1 rue racine","Leo@efrei.net","0659897435"))
controller.ajouter_client( Client("AEL","Lea","5 rue masque","Lea@efrei.net","0632589744"))
controller.ajouter_client( Client("DIREF","Farid","18 rue Puget","Farid@efrei.net","0756512489"))
controller.ajouter_client( Client("LAPU","Paul","50 blvd Pigale","Paul@efrei.net","0653214585"))
controller.ajouter_client( Client("MARIKA","Karima","89 place de la republique","Karima@efrei.net","0652489525"))

controller.ajouter_chambre( Chambre(205,3))
controller.ajouter_chambre( Chambre(207,3))
controller.ajouter_chambre( Chambre(202,3))
controller.ajouter_chambre( Chambre(215,3))
controller.ajouter_chambre( Chambre(305,3))
controller.ajouter_chambre( Chambre(203,2))
controller.ajouter_chambre( Chambre(101,1))
controller.ajouter_chambre( Chambre(505,4))
controller.ajouter_chambre( Chambre(603,2))


controller.ajouter_reservation(Reservation(2,3,"2021-07-01","2021-07-03",1))
controller.ajouter_reservation(Reservation(1,5,"2021-07-02","2021-07-03",1))
controller.ajouter_reservation(Reservation(3,7,"2021-08-15","2021-08-17",1))
controller.ajouter_reservation(Reservation(3,7,"2021-08-15","2021-08-20",1))



view.set_ROOMS(controller.getRoomsAsArray())



view.initialisation()
