from tkinter import *
from tkinter import messagebox
#from tkinter import Widget
from datetime import *
import tkinter.font as font
from typing import Optional
from Controller import *
from Model import *


JOURS = ["LUNDI","MARDI","MERCREDI","JEUDI","VENDREDI","SAMEDI","DIMANCHE"]
MOIS = ["JANVIER","FEVRIER","MARS","AVRIL","MAI","JUIN","JUILLET","AOUT","SEPTEMBRE","OCTOBRE","NOVEMBRE","DECEMBRE"]

"""ROOMS = [   [101,102,103,104,105,106],
            [201,202,203,204],
            [301,302,303,304,305,306,307,308,309,310],
            [401,402,403,404,405,406,407,408]
        ]"""

class View :

    def __init__(self, controller) :
        
        self.window = Tk()
        self.master_calendar = Frame(master = self.window)
        self.button_calendar = Frame(master = self.master_calendar)
        self.data_calendar = Frame(master = self.master_calendar)
        self.master_clients = Frame ( master = self.button_calendar,height=100)

        self.pivot_day = datetime.now()
        self.etage = 1

        self.wingdings_font = font.Font(family='Wingdings 3', size=30, weight='bold')
        self.verdana_font = font.Font(family='Verdana', size=12)
        self.controller = controller
        self.set_ROOMS(self.controller.getRoomsAsArray())
        
        self.client_sv = StringVar()
    
        self.images = self.creer_image()
        

    def creer_image(self) :

        dict = {}
        dict["loupe"] = PhotoImage(file = "Images/loupe.png").subsample(20,20)
        dict["pixel"] = PhotoImage(height=1, width=1)
        dict["quitter"] = PhotoImage (file="Images/quitter.png").subsample(25,25)
        dict["lock"] = PhotoImage(file = "Images/lock.png").subsample(22,22)
        dict["unlock"] = PhotoImage(file = "Images/unlock.png").subsample(27,27)
        dict["disk"] = PhotoImage(file = "Images/disk.png").subsample(30,30)
        dict["corbeille"]= PhotoImage(file = "Images/corbeille.png").subsample(18,18)
        dict["adduser"]= PhotoImage(file="Images/adduser.png").subsample(20,20)
        return dict

    def set_ROOMS(self, r) :
        self.ROOMS = r
        if len(self.ROOMS)== 0 :
            self.MAX_ROOMS = 0
        else :    
            self.MAX_ROOMS = len(self.ROOMS[0])
            for i in range(1,len(self.ROOMS)) :
                if len(self.ROOMS[i]) > self.MAX_ROOMS :
                    self.MAX_ROOMS = len(self.ROOMS[i])


    def update_days(self):

        for i in range(0,7):
            data_cell = self.data_calendar.winfo_children()[i+1]
            temp = (self.pivot_day + timedelta(i-self.pivot_day.weekday()))
            machaine = JOURS[i] +" "+ str(temp.day)+ "\n" +str(MOIS[temp.month-1])
            data_cell.winfo_children()[0].configure(text = machaine)
        self.update_data()

    def next_week(self) :
   
        self.pivot_day += timedelta(7)
        self.update_days()
    
    def previous_week(self) :
        self.pivot_day -= timedelta(7)
        self.update_days()

    def update_floors(self) :
        for i in range (0,self.MAX_ROOMS):
            data_cell = self.data_calendar.winfo_children()[i+8]
            if i < len (self.ROOMS[self.etage-1]) :
                data_cell.winfo_children()[0].configure(text = str(self.ROOMS[self.etage-1][i]), bg="pink3")
            else :
                data_cell.winfo_children()[0].configure(text = "\n",bg = "grey95")
        self.update_data()

    def update_data(self):
        for c in range (1,self.MAX_ROOMS+1):
            for j in range (1,8) :
                data_cell = self.data_calendar.winfo_children()[7+self.MAX_ROOMS+j+(c-1)*7]

                if c < len (self.ROOMS[self.etage-1])+1 :
                    
                    temp = (self.pivot_day + timedelta((j-1)-self.pivot_day.weekday()))
                   #############################################################
                    machaine = str(temp.year)+"-"+str(temp.month).zfill(2)+"-"+str(temp.day).zfill(2)
                    id_chambre = int(self.ROOMS[self.etage-1][c-1])
                    id_chambre = self.controller.get_id_byNumChambre(id_chambre)
                    resa = self.controller.get_reservation_byDateandRoomId(machaine, id_chambre) 
                    if resa != None :
                    #machaine = str(self.ROOMS[self.etage-1][c-1])+"\n" + str(temp.day)+"/"+str(temp.month)+"/"+str(temp.year)
                        client = self.controller.getClientById(resa._id_client)
                        if len(data_cell.winfo_children()) > 1 :
                            data_cell.winfo_children()[1].destroy()
                        data_cell.winfo_children()[0].pack_forget()
                        nomclient = client._nom
                        #resa_client = Button (master = data_cell,text=nomclient, command=lambda : self.fenetre_infos_resa(resa._id), bg = "SeaGreen3")
                        resa_client = Button (master = data_cell,text=nomclient, command=lambda arg1 = resa._id : self.fenetre_infos_resa(arg1), bg = "SeaGreen3")

                        resa_client.pack(expand=True, fill=BOTH, side = LEFT)
                    
                    else : 
                        if len(data_cell.winfo_children()) > 1 :
                            data_cell.winfo_children()[1].destroy()
           


    def next_floor(self) :
      
        if self.etage < len(self.ROOMS): 
            self.etage = self.etage + 1
            self.update_floors()

    def previous_floor(self):

        if self.etage > 1 :
            self.etage = self.etage - 1
            self.update_floors()

########################################################
    def creer_option_infos(self):
        
        clients = self.controller.getAllClients()
        if clients != []  :   
            tab = []
            for i in range(0,len(clients)) :
                tab.append(clients[i]._nom +" "+ clients[i]._prenom+" |"+clients[i]._mail)
           
            self.client_sv.set(tab[0])
            opt = OptionMenu(self.master_clients, self.client_sv, *tab)
            
            opt.config(image=self.images["pixel"], width=300,height=40, font=('Helvetica', 12), anchor='w',compound="left" ) #############################
            opt.pack(side=LEFT)
            
        ##Bouton infos client
            
            check = Button(master = self.master_clients, text = " Infos" ,height=45, command= lambda : self.fenetre_infos_client(opt,self.client_sv), font = self.verdana_font, image= self.images["loupe"], compound="left")
            check.pack(side=LEFT)
          

##########################################################
    def maj_option_menu(self) :
        
        clients = self.controller.getAllClients()
        if clients != []:
            if len(self.master_clients.winfo_children()) == 1 :
                self.creer_option_infos()
            menu = self.master_clients.winfo_children()[1]["menu"]
            menu.delete(0, "end")
            tab = []
            for i in range(0,len(clients)) :
                tab.append(clients[i]._nom +" "+ clients[i]._prenom+" |"+clients[i]._mail)
                menu.add_command(label=tab[i], command=lambda value=tab[i]: self.client_sv.set(value))
            self.client_sv.set(tab[0])

        else:
        
            while len(self.master_clients.winfo_children()) != 1 :
                self.master_clients.winfo_children()[1].destroy()
           


            

            
    
    def initialisation (self):

        ##Creation des boutons
        button_semainesuiv=Button(master = self.button_calendar, text="u", command=self.next_week ,bg ="pink1", font = self.wingdings_font )
        button_semaineprec=Button(master = self.button_calendar, text="t", command=self.previous_week,bg = 'pink1',font = self.wingdings_font)

        button_floor = Frame (master = self.data_calendar)
        button_floor.grid(row = 0, column=0,sticky=N+S+E+W)


        button_etageprec = Button (master = button_floor, text = "q",command=self.previous_floor ,bg ="pink1", font = self.wingdings_font)
        button_etagesuiv = Button (master = button_floor, text = "p",command=self.next_floor ,bg ="pink1", font = self.wingdings_font )

        button_semaineprec.pack(side = LEFT)
        button_semainesuiv.pack(side = RIGHT)
        self.button_calendar.pack(padx = 10,pady=5,fill=BOTH, expand=False)


        button_etageprec.pack (side = LEFT,expand = True,fill=BOTH)
        button_etagesuiv.pack (side = RIGHT,expand = True,fill=BOTH)

       

        ##Creation de la ligne des jours
        self.data_calendar.columnconfigure(0, weight=1, minsize=150)
        for i in range(7):
            self.data_calendar.columnconfigure(i+1, weight=1, minsize=150)
            data_cell = Frame (master=self.data_calendar, borderwidth=1,relief = RAISED)
            temp = (self.pivot_day + timedelta(i-self.pivot_day.weekday()))
            machaine = JOURS[i] +" "+ str(temp.day)+ "\n" +str(MOIS[temp.month-1])
            label = Label(master=data_cell, text=machaine,bg = "pink2",font = self.verdana_font)
            data_cell.grid(row = 0, column=i+1,sticky=N+S+E+W)
            label.pack(fill=BOTH, side=LEFT,expand = True)


        ##Creation des colonnes chambres
        self.data_calendar.rowconfigure(0, weight=1, minsize=20)
        for i in range(self.MAX_ROOMS):
            self.data_calendar.rowconfigure(i+1, weight=2, minsize=20)
            data_cell = Frame (master=self.data_calendar, borderwidth=1,relief = RAISED) #########
            label = Label(master=data_cell,text="\n" ,bg = "pink3",font = self.verdana_font)


            data_cell.grid(row = i+1, column=0,sticky=N+S+E+W)
            label.pack(fill=BOTH, side=LEFT,expand = True)


        ##Creation des données
        for r in range(1,self.MAX_ROOMS+1):
            for c in range(1,8):
                data_cell = Frame (master=self.data_calendar, borderwidth=1,relief = SUNKEN)
                label = Label(master=data_cell,text="\n",font = self.verdana_font)
                data_cell.grid(row = r, column=c,sticky=N+S+E+W)
                label.pack(fill=BOTH, side=LEFT,expand = True)
        self.update_floors()

        self.data_calendar.pack(fill=BOTH,expand = True)
        
        
        ## Ajout nouveau client
        creer_client = Button(master = self.master_clients, text = " Ajouter Client" , height= 45, command= lambda : self.fenetre_infos_client(self.master_clients,None), font = self.verdana_font,image=self.images["adduser"],compound="left")
        creer_client.pack(side=RIGHT)
  
        #Option + infos 
        self.creer_option_infos()
        self.master_clients.propagate(0)
        self.master_clients.pack(padx = 10,fill=X,expand = False)
        self.master_calendar.pack(fill=BOTH, side=LEFT,expand = True)

        self.window.mainloop()

    def sv_to_client(self,sv,clients,client) :
        
        for c in clients :
            if clients._mail == sv.get().split(sep = "|")[1] :
                client[0] = c

################################################################################
#INFOS CLIENTS
################################################################################
        
    def fenetre_infos_client (self,frame,client_sv) :
        if client_sv == None :
            client = Client()
        else :
            mail_client = client_sv.get().split(sep="|")[1]
            client = self.controller.getClientByMail(mail_client)
        
        window_infos = Toplevel(self.window)
        master_infos = Frame(master = window_infos,padx = 10,pady= 10)
        
        nom_client = StringVar()
        nom_client.set(client._nom)
        prenom_client = StringVar()
        prenom_client.set(client._prenom)
        adresse_client = StringVar()
        adresse_client.set(client._adresse)
        mail_client = StringVar()
        mail_client.set(client._mail)
        telephone_client = StringVar()
        telephone_client.set(client._telephone)

        Label(master_infos, 
                text="NOM :",font=self.verdana_font).grid(row=0,sticky=E)
        Label(master_infos, 
                text="PRENOM :",font=self.verdana_font).grid(row=1,sticky=E)
        Label(master_infos, 
                text="ADRESSE :",font=self.verdana_font).grid(row=2,sticky=E)
        Label(master_infos, 
                 text="MAIL :",font=self.verdana_font).grid(row=3,sticky=E)
        Label(master_infos, 
                text="TELEPHONE :",font=self.verdana_font).grid(row=4,sticky=E)

        e_nom = Entry(master_infos,state = "disabled",textvariable= nom_client,font=self.verdana_font, width= 70)
        e_prenom = Entry(master_infos,state = "disabled",textvariable= prenom_client,font=self.verdana_font,width= 70)
        e_adresse = Entry(master_infos,state = "disabled",textvariable= adresse_client,font=self.verdana_font,width= 70)
        e_mail = Entry(master_infos,state = "disabled",textvariable= mail_client,font=self.verdana_font,width= 70)
        e_telephone = Entry(master_infos,state = "disabled",textvariable= telephone_client,font=self.verdana_font,width= 70)

        e_nom.grid(row=0, column=1, sticky=W)
        e_prenom.grid(row=1, column=1, sticky=W)
        e_adresse.grid(row=2, column=1 ,sticky=W)
        e_mail.grid(row=3, column=1, sticky=W)
        e_telephone.grid(row=4, column=1, sticky=W)
        
        def exit_button ():
            window_infos.quit()
            window_infos.destroy()

        bout_quitter_frame = Frame (master_infos, height= 50)
        Button( bout_quitter_frame,
                text='Quitter', 
                command=exit_button, font=self.verdana_font,
                height=50,width=120,image=self.images["quitter"],compound="left").pack(side = "right")
        bout_quitter_frame.propagate(0)
        bout_quitter_frame.grid (row=5,column=1, pady=4,sticky= EW)
        
        bout_editer_frame = Frame (master_infos, height= 50, width = 100)
        
        def sauvegarder_infos ():
            client._nom = nom_client.get()
            client._prenom = prenom_client.get()
            client._adresse = adresse_client.get()
            client._mail = mail_client.get()
            client._telephone = telephone_client.get()
            if client._mail != "" and client._nom != "" :
                
                if self.controller.modifier_client_byId(client) == "MAIL EXISTANT" :
                    messagebox.showerror(title=None, message="Le client existe deja", parent = window_infos )
                else :
                    messagebox.showinfo(title = None, message= "Le client a bien été modifié", parent = window_infos)
                    self.maj_option_menu()
            else :
                messagebox.showwarning(title = None, message= "Veuillez remplir au moins les champs nom et mail", parent = window_infos)
                
                      
        def activer_modif () :
            if bout_editer_frame.winfo_children()[0]['bg'] == "red" :
                e_nom.configure(state="normal")
                e_prenom.configure(state="normal")
                e_adresse.configure(state="normal")
                e_mail.configure(state="normal")
                e_telephone.configure(state="normal")
                bout_editer_frame.winfo_children()[0].configure(bg = "green", image = self.images["unlock"])
                Button ( bout_quitter_frame, command=sauvegarder_infos, text = " Sauvegarder",
                height=50,width=150, font = self.verdana_font,image = self.images["disk"],compound="left").pack(side = "left")
                if client_sv != None :
                    Button (bout_quitter_frame, command= supprimer_client, text = "Supprimer",
                    height=50,width=120,font = self.verdana_font,image= self.images["corbeille"],compound="left").pack(side = "right",padx = 15)
            else :
                e_nom.configure(state= "disabled")
                e_prenom.configure(state="disabled")
                e_adresse.configure(state="disabled")
                e_mail.configure(state="disabled")
                e_telephone.configure(state="disabled")
                bout_editer_frame.winfo_children()[0].configure(bg = "red", image = self.images["lock"])
                bout_quitter_frame.winfo_children()[1].destroy()
                if client_sv != None :
                    bout_quitter_frame.winfo_children()[1].destroy()
        

        def supprimer_client():
            msgbox = messagebox.askquestion('Suppression','Êtes-vous sûr de vouloir supprimer ce client ?',icon = 'error', parent = window_infos) 
            if msgbox == 'yes' :
                self.controller.supprimer_client_byId(client)
                window_infos.destroy()
                self.maj_option_menu()
          

        Button(bout_editer_frame, command =activer_modif, image = self.images["lock"], bg = "red", font=self.verdana_font ).pack(fill=BOTH,expand = True)
        bout_editer_frame.propagate(0)
        bout_editer_frame.grid (row=5,column=0, sticky=W, pady=4)
        if (client_sv == None) :
            activer_modif()

        master_infos.pack()
        window_infos.resizable(False,False)
        window_infos.mainloop()

################################################################################
#INFOS RESERVATION
################################################################################

    def fenetre_infos_resa (self,id_resa) :
        
        if id_resa == -1 :
            resa = Reservation()
        else :
            resa = self.controller.getReservationById(id_resa)
        
        window_infos = Toplevel(self.window)
        master_infos = Frame(master = window_infos,padx = 10,pady= 10)

        id_client = resa._id_client
        client = self.controller.getClientById(id_client)
        nom_client = StringVar()
        nom_client.set(client._nom)
        print (nom_client)
        #prenom_client = StringVar()
        #prenom_client.set(client._prenom)

        Label(master_infos, 
                text="NOM :",font=self.verdana_font).grid(row=0,sticky=E)
        #Label(master_infos, 
                #text="PRENOM :",font=self.verdana_font).grid(row=1,sticky=E)
        
        e_nom = Entry(master_infos,state = "disabled",textvariable= nom_client,font=self.verdana_font, width= 70)
        #e_prenom = Entry(master_infos,state = "disabled",textvariable= prenom_client,font=self.verdana_font,width= 70)

        e_nom.grid(row=0, column=1, sticky=W)
        #e_prenom.grid(row=1, column=1, sticky=W)



        master_infos.pack()
        window_infos.resizable(False,False)
        window_infos.mainloop()



"""      
self._id_client = id_client
        self._id_chambre = id_chambre
        self._nb_occupants = nb_occupants
        self._date_arrivee = date_arrivee
        self._date_depart = date_depart
    
        nom_client = StringVar()
        nom_client.set(resa.id_client)

        prenom_client = StringVar()
        prenom_client.set(resa.id_client)
        nb_occupants = StringVar()
        nb_occupants.set(client._)
        mail_client = StringVar()
        mail_client.set(client._mail)
        telephone_client = StringVar()
        telephone_client.set(client._telephone)

        Label(master_infos, 
                text="NOM :",font=self.verdana_font).grid(row=0,sticky=E)
        Label(master_infos, 
                text="PRENOM :",font=self.verdana_font).grid(row=1,sticky=E)
        Label(master_infos, 
                text="ADRESSE :",font=self.verdana_font).grid(row=2,sticky=E)
        Label(master_infos, 
                 text="MAIL :",font=self.verdana_font).grid(row=3,sticky=E)
        Label(master_infos, 
                text="TELEPHONE :",font=self.verdana_font).grid(row=4,sticky=E)

        e_nom = Entry(master_infos,state = "disabled",textvariable= nom_client,font=self.verdana_font, width= 70)
        e_prenom = Entry(master_infos,state = "disabled",textvariable= prenom_client,font=self.verdana_font,width= 70)
        e_adresse = Entry(master_infos,state = "disabled",textvariable= adresse_client,font=self.verdana_font,width= 70)
        e_mail = Entry(master_infos,state = "disabled",textvariable= mail_client,font=self.verdana_font,width= 70)
        e_telephone = Entry(master_infos,state = "disabled",textvariable= telephone_client,font=self.verdana_font,width= 70)

        e_nom.grid(row=0, column=1, sticky=W)
        e_prenom.grid(row=1, column=1, sticky=W)
        e_adresse.grid(row=2, column=1 ,sticky=W)
        e_mail.grid(row=3, column=1, sticky=W)
        e_telephone.grid(row=4, column=1, sticky=W)
        
        def exit_button ():
            window_infos.quit()
            window_infos.destroy()

        bout_quitter_frame = Frame (master_infos, height= 50)
        Button( bout_quitter_frame,
                text='Quitter', 
                command=exit_button, font=self.verdana_font,
                height=50,width=120,image=self.images["quitter"],compound="left").pack(side = "right")
        bout_quitter_frame.propagate(0)
        bout_quitter_frame.grid (row=5,column=1, pady=4,sticky= EW)
        
        bout_editer_frame = Frame (master_infos, height= 50, width = 100)
        
        def sauvegarder_infos ():
            client._nom = nom_client.get()
            client._prenom = prenom_client.get()
            client._adresse = adresse_client.get()
            client._mail = mail_client.get()
            client._telephone = telephone_client.get()
            if client._mail != "" and client._nom != "" :
                
                if self.controller.modifier_client_byId(client) == "MAIL EXISTANT" :
                    messagebox.showerror(title=None, message="Le client existe deja", parent = window_infos )
                else :
                    messagebox.showinfo(title = None, message= "Le client a bien été modifié", parent = window_infos)
                    self.maj_option_menu()
            else :
                messagebox.showwarning(title = None, message= "Veuillez remplir au moins les champs nom et mail", parent = window_infos)
                
                      
        def activer_modif () :
            if bout_editer_frame.winfo_children()[0]['bg'] == "red" :
                e_nom.configure(state="normal")
                e_prenom.configure(state="normal")
                e_adresse.configure(state="normal")
                e_mail.configure(state="normal")
                e_telephone.configure(state="normal")
                bout_editer_frame.winfo_children()[0].configure(bg = "green", image = self.images["unlock"])
                Button ( bout_quitter_frame, command=sauvegarder_infos, text = " Sauvegarder",
                height=50,width=150, font = self.verdana_font,image = self.images["disk"],compound="left").pack(side = "left")
                if client_sv != None :
                    Button (bout_quitter_frame, command= supprimer_client, text = "Supprimer",
                    height=50,width=120,font = self.verdana_font,image= self.images["corbeille"],compound="left").pack(side = "right",padx = 15)
            else :
                e_nom.configure(state= "disabled")
                e_prenom.configure(state="disabled")
                e_adresse.configure(state="disabled")
                e_mail.configure(state="disabled")
                e_telephone.configure(state="disabled")
                bout_editer_frame.winfo_children()[0].configure(bg = "red", image = self.images["lock"])
                bout_quitter_frame.winfo_children()[1].destroy()
                if client_sv != None :
                    bout_quitter_frame.winfo_children()[1].destroy()
        

        def supprimer_client():
            msgbox = messagebox.askquestion('Suppression','Êtes-vous sûr de vouloir supprimer ce client ?',icon = 'error', parent = window_infos) 
            if msgbox == 'yes' :
                self.controller.supprimer_client_byId(client)
                window_infos.destroy()
                self.maj_option_menu()
          

        Button(bout_editer_frame, command =activer_modif, image = self.images["lock"], bg = "red", font=self.verdana_font ).pack(fill=BOTH,expand = True)
        bout_editer_frame.propagate(0)
        bout_editer_frame.grid (row=5,column=0, sticky=W, pady=4)
        if (client_sv == None) :
            activer_modif()

        master_infos.pack()
        window_infos.resizable(False,False)
        window_infos.mainloop()

    

        """
