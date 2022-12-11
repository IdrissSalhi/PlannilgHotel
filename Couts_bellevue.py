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
        self.scroll=Scrollbar(self.window, orient='horizontal')
        self.master_couts_canvas = Canvas(master = self.window, width = self.element_width*8, xscrollcommand = self.scroll.set, scrollregion = (0,0,len(reservation._couts)*self.element_width,0))
        self.master_couts = Frame(master = self.master_couts_canvas)
        self.master_couts.propagate(0)
        self.master_titre= Frame(master = self.window)
        self.master_boutons = Frame(master = self.window)
        self.images = {}
        self.images["disk"] = PhotoImage(file = "Images/disk.png").subsample(30,30)
        self.images["quitter"] = PhotoImage (file="Images/quitter.png").subsample(25,25)
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
        b_names = ["Chambre", "Petit-dejeuner", "Téléphone", "Bar", "Taxe Séjour"]
        for i in range(len(b_names)) :
            data_cell = Frame( master = self.master_titre)
            Button(master = data_cell, text = b_names[i], font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE)).pack(fill=BOTH, side=LEFT,expand = True)
            data_cell.configure(height = self.element_height, width = self.element_width)
            data_cell.propagate(0)
            data_cell.grid(column = 0, row = i+1, sticky= NSEW)
        
        
        
        
        
        
        data_stringvar = []
        j = 0
        for cout in self._reservation._couts :
            jour_stringvar = []
            data_cell = Frame(master = self.master_couts)
            Label(master = data_cell, text = cout._date_jour.strftime("%d-%m-%Y"), font = font.Font(family = POLICE_JOURS, size = POLICE_JOURS_TAILLE)).pack(fill=BOTH, side=LEFT,expand = True)
            data_cell.configure(height = self.element_height, width = self.element_width )
            data_cell.propagate(0)
            data_cell.grid(column = j, row = 0, sticky = W)
            



        
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
                data_cell.grid(column = j, row = i+1, sticky = W)
                jour_stringvar.append(var)


            
            data_stringvar.append(jour_stringvar)
            j += 1
            #fin couts jour

        #TO DO 
        for i in range (0, len(self._reservation._couts)) :
            data_stringvar[i][0].set(int(self._reservation._couts[i]._total_chambre))
            data_stringvar[i][1].set(int(self._reservation._couts[i]._total_petit_dej))
            data_stringvar[i][2].set(int(self._reservation._couts[i]._total_telephone))
            data_stringvar[i][3].set(int(self._reservation._couts[i]._total_bar))
            data_stringvar[i][4].set(int(self._reservation._couts[i]._total_taxe_sejour))

        def sauvegarder_infos() :
            x = False
            for i in range (0, len(data_stringvar)) : 
                for j in range (0, len(data_stringvar[i])) : 
                    if data_stringvar[i][j].get()== "" or not data_stringvar[i][j].get().isnumeric() :
                        x = True
            if x == True :
                print("Erreur")
                messagebox.showerror(title=None, message="Au moins un des champs est invalide", parent = self.window )
            else :
                
                for i in range (0, len(self._reservation._couts)) : 
                    self._reservation._couts[i]._total_chambre = int(data_stringvar[i][0].get())
                    self._reservation._couts[i]._total_petit_dej = int(data_stringvar[i][1].get())
                    self._reservation._couts[i]._total_telephone = int(data_stringvar[i][2].get())
                    self._reservation._couts[i]._total_bar = int(data_stringvar[i][3].get())
                    self._reservation._couts[i]._total_taxe_sejour = int(data_stringvar[i][4].get())
                controller.modifier_reservation_byId(self._reservation)


                        

        def exit_button ():
            self.window.quit()
            self.window.destroy()

        
        bouton_sauvegarder = Button (master = self.window, 
                text = " Sauvegarder", height=50,width=150, command = sauvegarder_infos,
                fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),image = self.images["disk"],compound="left") 
        boutton_quitter = Button( master = self.window,
                text='Quitter', 
                command=exit_button, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),
                height=50,width=150,image=self.images["quitter"],compound="left")






        self.master_titre.grid(column = 0, row = 0)
        self.master_couts_canvas.create_window((0,0), window=self.master_couts, anchor="nw")
        self.master_couts_canvas.grid(column = 1, row = 0, columnspan = 7, sticky=NSEW)
        self.scroll.config(command = self.master_couts_canvas.xview)
        self.scroll.grid(column = 1, row = 1, columnspan = 7, sticky = NSEW)
        bouton_sauvegarder.grid(column = 0, row = 2)
        boutton_quitter.grid(column = 0, row = 4)


        self.window.mainloop()
        


































####################
resa_test = controller.getReservationById(2)
cv = Cout_View(resa_test)
cv.initialisation()


