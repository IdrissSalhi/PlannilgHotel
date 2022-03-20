from Src.Model import *
from Src.Controller import *
from Src.View import *
from Src.Database import *

db = Database()
controller = Controller(db)
view = View(controller)



#view.set_ROOMS(controller.getRoomsAsArray())



view.initialisation()
db._connexion.close()