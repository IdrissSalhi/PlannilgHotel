from textwrap import fill
from Src.Model import *
from Src.Controller import *
import locale
from Src.Config import *


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
        self.master_couts = Frame(master = self.window, highlightbackground = "blue", highlightthickness = 2)
        self.master_titre= Frame(master = self.window, highlightbackground = "green", highlightthickness = 2)
        self.pixel = PhotoImage(width = 1, height = 1)

        
        self._reservation = reservation

        #to do   deux frames : - titre (colonne de gauche)
        #                       - zone slider (les couts, le reste des colonnes) 
        #                       - frame boutons (quitter, sauvegarder, GENERER FACTURE)
        #           
    def initialisation (self) :
        
        #remplir les titres et peupler zone des slider
        self.master_titre.configure(width = 1000)
        Label(master = self.master_titre, text = "DATE", font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE), image = self.pixel, height= self.element_height, width = self.element_width, compound = CENTER).grid(column = 0, row = 0, sticky= NSEW)
        b_names = ["Chambre", "Petit-dejeuner", "Téléphone", "Bar", "", "Taxe Séjour"]
        for i in range(len(b_names)) :
            Button(master = self.master_titre, text = b_names[i], font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE), image = self.pixel, height= self.element_height, width = self.element_width, compound = CENTER).grid(column = 0, row = i+1, sticky= NSEW)
        #TO DO : Ajouter commande bouton
        

        data_stringvar = []
        #début couts jour
        jour_stringvar = []
        Label(master= self.master_couts, text="").grid(column = 0, row = 0, sticky = W)
        for i in range(len(b_names)) :
            var = StringVar()
            Spinbox(master= self.master_couts, textvariable = var, from_ = 0 , to = 10000).grid(column = 0, row = i+1, sticky = W)
            jour_stringvar.append(var)


        
        data_stringvar.append(jour_stringvar)
        #fin couts jour








        self.master_titre.grid(column = 0, row = 0)
        self.master_couts.grid(column = 1, row = 0, columnspan = 7, sticky=NSEW)


        self.window.mainloop()
        


































####################
resa_test = controller.getReservationById(14)
cv = Cout_View(resa_test)
cv.initialisation()


