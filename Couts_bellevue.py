from ctypes import resize
from textwrap import fill
from Src.Model import *
from Src.Controller import *
import locale
from Src.Config import *
import tkinter.ttk as ttk


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

        
        self._reservation = reservation

        #to do   deux frames : - titre (colonne de gauche)
        #                       - zone slider (les couts, le reste des colonnes) 
        #                       - frame boutons (quitter, sauvegarder, GENERER FACTURE)
        #           
    def initialisation (self) :
        
        #remplir les titres et peupler zone des slider
        data_cell = Frame( master = self.master_titre)
        Label(master = data_cell, text = "DATE", font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE)).pack(fill=BOTH, side=LEFT,expand = True)
        data_cell.configure( height = self.element_height, width = self.element_width)
        data_cell.propagate(0)
        data_cell.grid(column = 0, row = 0, sticky= NSEW)
        b_names = ["Chambre", "Petit-dejeuner", "Téléphone", "Bar", "", "Taxe Séjour"]
        for i in range(len(b_names)) :
            data_cell = Frame( master = self.master_titre)
            Button(master = data_cell, text = b_names[i], font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE)).pack(fill=BOTH, side=LEFT,expand = True)
            data_cell.configure(height = self.element_height, width = self.element_width)
            data_cell.propagate(0)
            data_cell.grid(column = 0, row = i+1, sticky= NSEW)
        #TO DO : Ajouter commande bouton
        
        
        data_stringvar = []
        #début couts jour
        jour_stringvar = []
        data_cell = Frame(master = self.master_couts)
        Label(master = data_cell, text="").pack(fill=BOTH, side=LEFT,expand = True)
        data_cell.configure(height = self.element_height, width = self.element_width )
        data_cell.propagate(0)
        data_cell.grid(column = 0, row = 0, sticky = W)
        
        for i in range(len(b_names)) :
            var = StringVar()
            data_cell = Frame(master = self.master_couts)
            style = ttk.Style(self.window)
            style.theme_use("default")
            style.layout('resize1.TSpinbox', [('Spinbox.field',
            {'expand': 1,
            'sticky': 'nswe',
            'children': [('null',
                {'side': 'right',
                'sticky': 'ns',
                'children': [('Spinbox.uparrow', {'side': 'top', 'sticky': 'e'}),
                ('Spinbox.downarrow', {'side': 'bottom', 'sticky': 'e'})]}),
                ('Spinbox.padding',
                {'sticky': 'nswe',
                'children': [('Spinbox.textarea', {'sticky': 'nswe'})]})]})])
            
            style.configure('resize1.TSpinbox', arrowsize = 30)
            ttk.Spinbox(master= data_cell, textvariable = var, from_ = 0 , to = 10000, style = 'resize1.TSpinbox',
               font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE)).pack(fill=BOTH, side=BOTTOM,expand = True)
            data_cell.configure(height = self.element_height, width = self.element_width )
            data_cell.propagate(0)
            data_cell.grid(column = 0, row = i+1, sticky = W)
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


