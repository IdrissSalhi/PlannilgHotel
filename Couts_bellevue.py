from Src.Model import *
from Src.Controller import *
import locale


locale.setlocale(locale.LC_TIME, 'fr_FR')
db = Database('DB/HotelBDD.db')
controller = Controller(db)
class Cout_View :
    def __init__(self, reservation):
        self.window = Tk()
        self.element_height = self.window.winfo_screenheight()/9 - 5
        self.element_width = self.window.winfo_screenwidth()/9 - 5
        self.window.title("Couts reservation")
        self.window.resizable(False, False)
        self.window.state("zoomed")
        self.master_couts = Frame(master = self.window)
        self._reservation = reservation
    
    def initialisation (self) :
        self.master_couts.pack(fill=BOTH, side=LEFT,expand = True)
        
        
        self.window.mainloop()
        


































####################
resa_test = controller.getReservationById(14)
cv = Cout_View(resa_test)
cv.initialisation()


