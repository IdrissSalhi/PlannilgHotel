from tkinter import messagebox
from ctypes import resize
from textwrap import fill
from Src.Model import *
from Src.Controller import *
import locale
from Src.Config import *
import tkinter.ttk as ttk
from tkinter import *
import tkinter.font as font
from tkinter.messagebox import askyesno



locale.setlocale(locale.LC_TIME, 'fr_FR')

class Cout_View :
    def __init__(self, reservation, view):

        self.view = view
        self.window = Toplevel(view.window)
        self.element_height = self.window.winfo_screenheight()/9 - 5
        self.element_width = self.window.winfo_screenwidth()/9 - 5
        self.window.title("Couts reservation")
        self.window.resizable(False, False)
        self.window.state("zoomed")
        self.scroll=ttk.Scrollbar(self.window, orient='horizontal')
        self.master_couts_canvas = Canvas(master = self.window, height = self.element_height*6, width = self.element_width*8, xscrollcommand = self.scroll.set, scrollregion =(0,0,len(reservation._couts)*self.element_width,0))                                  
        self.master_couts = Frame(master = self.master_couts_canvas)
        self.master_titre= Frame(master = self.window)
        self.master_accompte = Frame(master = self.window )
        self.master_facture = Frame(master = self.window)
        self.images = {}
        self.images["disk"] = PhotoImage(file = "Images/disk.png").subsample(30,30)
        self.images["quitter"] = PhotoImage (file="Images/quitter.png").subsample(25,25)
        self.images["no"] = PhotoImage (file="Images/no.png").subsample(25,25)
        self.images["yes"] = PhotoImage (file="Images/yes.png").subsample(25,25)
        self.images["facture"] = PhotoImage (file="Images/Facture.png").subsample(15,15)
        self._reservation = reservation
        self._controller = view.controller

        
    def initialisation (self) :
        
        data_cell = Frame( master = self.master_titre)
        Label(master = data_cell, text = "DATE", font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE)).pack(fill=BOTH, side=LEFT,expand = True)
        data_cell.configure( height = self.element_height, width = self.element_width)
        data_cell.propagate(0)
        data_cell.grid(column = 0, row = 0, sticky= NSEW)
        b_names = ["Chambre", "Petit-dejeuner", "Téléphone", "Bar", "Taxe Séjour"]
        data_stringvar = []
        
        def data_ligne (index) :
            window_data_ligne = Toplevel(self.window)
            window_data_ligne.title(b_names[index])
            infos_data_ligne = Frame(window_data_ligne, padx = 10, pady= 10)
            infos_data = StringVar()
            Label(infos_data_ligne, text = "Veuillez saisir une valeur pour " + b_names[index], fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row = 0, column = 1, columnspan = 2)
            Entry(infos_data_ligne, textvariable = infos_data, fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row = 1, column = 1, columnspan = 2)
            def annuler ():
                window_data_ligne.quit()
                window_data_ligne.destroy()
            def valider ():
                for d in range (0, len(self._reservation._couts)) :
                    data_stringvar[d][index].set(infos_data.get())
                annuler()
          
            Button(infos_data_ligne, text = "Annuler", command = annuler,fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE), image = self.images["no"], compound="left").grid(row = 2, column = 3)
            Button(infos_data_ligne, text= "Valider", command = valider,fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE), image = self.images["yes"], compound="left").grid(row = 2, column = 0)


            infos_data_ligne.pack(fill=BOTH, side=LEFT,expand = True)
            window_data_ligne.mainloop()

        for i in range(len(b_names)) :
            data_cell = Frame( master = self.master_titre)
            Button(master = data_cell, command=lambda arg1 = i  : data_ligne(arg1), text = b_names[i], font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE)).pack(fill=BOTH, side=LEFT,expand = True)
            data_cell.configure(height = self.element_height, width = self.element_width)
            data_cell.propagate(0)
            data_cell.grid(column = 0, row = i+1, sticky= NSEW)
        
        
        
        
        def highlight_save(name, index, mode):
            boutton_sauvegarder.configure(bg = COUL_CADENAS_OUVERT)
        
        
        j = 0
        for cout in self._reservation._couts :
            jour_stringvar = []
            data_cell = Frame(master = self.master_couts)
            machaine ="" + JOURS[cout._date_jour.weekday()] +" "+ str(cout._date_jour.day)+ "\n" +str(MOIS[cout._date_jour.month-1]) + "\n" + str(cout._date_jour.year)
            Label(master = data_cell, text = machaine, font = font.Font(family = POLICE_JOURS, size = POLICE_JOURS_TAILLE)).pack(fill=BOTH, side=LEFT,expand = True)
            data_cell.configure(height = self.element_height, width = self.element_width )
            data_cell.propagate(0)
            data_cell.grid(column = j, row = 0, sticky = W)
            
    
            for i in range(len(b_names)) :
                var = StringVar()
                data_cell = Frame(master = self.master_couts)
                
                ttk.Spinbox(master= data_cell, textvariable = var, from_ = 0 , to = 10000, style = 'resize1.TSpinbox', justify = 'center',
                font = font.Font(family = POLICE_SPINBOX, size = POLICE_SPINBOX_TAILLE)).pack(fill=BOTH, side=BOTTOM,expand = True)
                data_cell.configure(height = self.element_height, width = self.element_width )
                data_cell.propagate(0)
                data_cell.grid(column = j, row = i+1, sticky = NSEW)
                jour_stringvar.append(var)


            
            data_stringvar.append(jour_stringvar)
            j += 1

        for i in range (0, len(self._reservation._couts)) :
            data_stringvar[i][0].set(int(self._reservation._couts[i]._total_chambre))
            data_stringvar[i][1].set(int(self._reservation._couts[i]._total_petit_dej))
            data_stringvar[i][2].set(int(self._reservation._couts[i]._total_telephone))
            data_stringvar[i][3].set(int(self._reservation._couts[i]._total_bar))
            data_stringvar[i][4].set(int(self._reservation._couts[i]._total_taxe_sejour))
        
        for i in range (0, len(data_stringvar)) :
            for j in range(0, len(data_stringvar[i])) :
                data_stringvar[i][j].trace("w", highlight_save)
        
        #Accompte
        total_acccompte = StringVar()
        total_acccompte.set(int(self._reservation._accompte))
        total_acccompte.trace("w", highlight_save)
    
        accompte_label = Frame(master= self.master_accompte)
        Label(master = accompte_label, text = "Accompte",font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE)).pack(fill=BOTH, side=LEFT,expand = True)
        accompte_label.configure(height = int(self.element_height), width = int(self.element_width))
        accompte_label.propagate(0)
        accompte_label.grid(row = 0, column = 0)

        accompte_spinbox = Frame(master= self.master_accompte)
        ttk.Spinbox(master= accompte_spinbox, textvariable = total_acccompte, from_ = 0 , to = 100000, style = 'resize1.TSpinbox', justify = 'center',
                    font = font.Font(family = POLICE_SPINBOX, size = POLICE_SPINBOX_TAILLE)).pack(fill=BOTH, side = LEFT, expand = True)
        accompte_spinbox.configure(height = int(self.element_height), width = int(self.element_width))
        accompte_spinbox.propagate(0)
        accompte_spinbox.grid(row = 0, column = 1)

        #Facture

        Button(master = self.master_facture,# command = 
                text = " Générer Facture",font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),
                height = int(self.element_height),width = int(self.element_width),
                image =  self.images["facture"], compound = LEFT).grid(row = 0, column = 0)
        
        
        
        def sauvegarder_infos() :
            x = False
            for i in range (0, len(data_stringvar)) : 
                for j in range (0, len(data_stringvar[i])) : 
                    if data_stringvar[i][j].get()== "" or not data_stringvar[i][j].get().isnumeric() :
                        x = True
            if total_acccompte.get() == "" or not total_acccompte.get().isnumeric() :
                x= True
            if x == True :
                print("Erreur")
                messagebox.showerror(title=None, message="Au moins un des champs est invalide", parent = self.window )
            else :
                self._reservation._accompte = int(total_acccompte.get())
                
                for i in range (0, len(self._reservation._couts)) : 
                    self._reservation._couts[i]._total_chambre = int(data_stringvar[i][0].get())
                    self._reservation._couts[i]._total_petit_dej = int(data_stringvar[i][1].get())
                    self._reservation._couts[i]._total_telephone = int(data_stringvar[i][2].get())
                    self._reservation._couts[i]._total_bar = int(data_stringvar[i][3].get())
                    self._reservation._couts[i]._total_taxe_sejour = int(data_stringvar[i][4].get())
                self._controller.modifier_reservation_byId(self._reservation)
                boutton_sauvegarder.configure(bg = boutton_quitter["background"])
                self.view.update_data()
            


                     

        def exit_button ():
            if boutton_quitter["background"] == boutton_sauvegarder["background"] :
                self.window.quit()
                self.window.destroy()
            else :
                answer = askyesno(title='confirmation',
                    message="Voulez-vous continuer sans sauvegarder ?", parent = self.window)
                if answer == True :
                    self.window.quit()
                    self.window.destroy()


        
        boutton_sauvegarder = Button (master = self.window, 
                text = " Sauvegarder", height=50,width=150, command = sauvegarder_infos,
                fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),image = self.images["disk"],compound="left") 
        boutton_quitter = Button( master = self.window,
                text='Quitter', 
                command=exit_button, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),
                height=50,width=150,image=self.images["quitter"],compound="left")

        
        




        self.master_titre.grid(column = 0, row = 0, rowspan = 6)
        self.master_couts_canvas.create_window((0,0), window=self.master_couts, anchor="nw")
        self.master_couts_canvas.grid(column = 1, row = 0, columnspan = 8, rowspan = 6, sticky= EW)#modif
        self.scroll.config(command = self.master_couts_canvas.xview)
        if len(self._reservation._couts) > 8 :
            self.scroll.grid(column = 1, row = 7, columnspan = 8, sticky = NSEW)#modif
        
        self.master_accompte.grid(column = 0, row = 8, columnspan = 2)
       
        #Restreindre position nouton générer facture entre 2 et 8        
        fac_col = len(self._reservation._couts)
        if fac_col <= 1 :
            fac_col = 2
        elif fac_col >= 8 :
            fac_col = 8
        

        #Ajout de frame pour conserver l'alignement colonne
        for i in range (2,9):
            if i != fac_col :
                master_test = Frame(master = self.window)
                master_test.propagate(0)
                master_test.configure(height = self.element_height, width = self.element_width)
                master_test.grid(row = 8, column = i)
            else :
                self.master_facture.grid(column = fac_col, row = 8)

        
     


        boutton_sauvegarder.grid(column = 0, row = 9)
        boutton_quitter.grid(column = 0, row = 10)
        
        self.window.protocol("WM_DELETE_WINDOW", exit_button)   
        self.window.mainloop()
        



