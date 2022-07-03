from Src.Model import *
from Src.Controller import *
from Src.View import *
from Src.Database import *
import locale


locale.setlocale(locale.LC_TIME, 'fr_FR')
db = Database('DB/HotelBDD.db')
controller = Controller(db)
view = View(controller)




#view.set_ROOMS(controller.getRoomsAsArray())



view.initialisation()
db._connexion.close()