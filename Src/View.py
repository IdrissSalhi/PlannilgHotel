from calendar import month
from distutils import command
from tkinter import *
from tkinter import messagebox
from datetime import *
import tkinter.font as font
from turtle import width

from numpy import expand_dims
from Src.Controller import *
from Src.Model import *
from tkcalendar import *
from tkinter import ttk
from Src.Config import *
from Src.Bellevue.pdf_bellevue import *
from PIL import Image, ImageTk


JOURS = ["LUNDI","MARDI","MERCREDI","JEUDI","VENDREDI","SAMEDI","DIMANCHE"]
MOIS = ["JANVIER","FEVRIER","MARS","AVRIL","MAI","JUIN","JUILLET","AOUT","SEPTEMBRE","OCTOBRE","NOVEMBRE","DECEMBRE"]

class View :

    def __init__(self, controller) :
        
        self.window = Tk()
        self.element_height = self.window.winfo_screenheight()/9 - 5
        self.element_width = self.window.winfo_screenwidth()/9 - 5
        self.window.title("Planning Hotel")
        self.window.resizable(False, False)
        self.window.state("zoomed")
        self.master_calendar = Frame(master = self.window)
        self.button_calendar = Frame(master = self.master_calendar)
        self.data_calendar = Frame(master = self.master_calendar)
        self.master_clients = Frame ( master = self.button_calendar,height = self.element_height)
        self.master_add = Frame ( master = self.button_calendar,height = self.element_height)

        self.pivot_day = datetime.now()
        self.page = 0

        self.wingdings_font = font.Font(family='Wingdings 3', size=30, weight='bold')
        self.verdana_font = font.Font(family='Verdana', size=12)
        self.controller = controller
        
        self.ROOMS = [[101,102,202,203,204],
        [302,303,304,402,403,404,502,503],
        [504,602,603,604,702,704],
        [201,301,401,501,601,701,703],
        [206,506,606,706,306,406],
        [103,205,305,405,505,605,705]]
        
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
        dict["up"] = PhotoImage(file="Images/up.png").subsample(17,17)
        dict["down"] = PhotoImage(file="Images/down.png").subsample(17,17)
        dict["right"] = PhotoImage(file="Images/right.png").subsample(17,17)
        dict["left"] = PhotoImage(file="Images/left.png").subsample(17,17)
        return dict
       
    def update_days(self):

        for i in range(0,7):
            data_cell = self.data_calendar.winfo_children()[i+1]
            temp = (self.pivot_day + timedelta(i-self.pivot_day.weekday()))
            machaine ="" + JOURS[i] +" "+ str(temp.day)+ "\n" +str(MOIS[temp.month-1]) + ""
            data_cell.winfo_children()[0].configure(text = machaine,
                        command=lambda arg1 = temp,arg2 = self.controller  : generer_pdf(arg1, arg2))
        self.update_data()

    def next_week(self) :
   
        self.pivot_day += timedelta(7)
        self.update_days()
    
    def previous_week(self) :
        self.pivot_day -= timedelta(7)
        self.update_days()


    def destroy_data(self) :
        while (len(self.data_calendar.winfo_children()) > 8) :
            self.data_calendar.winfo_children()[8].destroy()

    def recreate_data(self) :
        self.data_calendar.columnconfigure(0, weight=1)
        for i in range(0,8):
            self.data_calendar.columnconfigure(i+1, weight=1)
            data_cell = Frame (master=self.data_calendar, borderwidth=1,relief = RAISED) #########
            if i < len(self.ROOMS[self.page]) :
                label = Label(master=data_cell,text=self.ROOMS[self.page][i] ,bg = COUL_CHAMBRES_CAL,fg = COUL_POLICE_CHAMBRES, font = font.Font(family = POLICE_CHAMBRES, size =POLICE_CHAMBRES_TAILLE))
            else :
                label = Label(master=data_cell,text= "" ,bg = COUL_FOND_CAL)

            data_cell.grid(row = 0, column=i+1,sticky=N+S+E+W)
            label.pack(fill=BOTH, side=LEFT,expand = True)
        
      

        for r in range(1,8):
            for c in range(1,9):
                data_cell = Frame (master=self.data_calendar, borderwidth=1,relief = SUNKEN)
                #########
                if c < len(self.ROOMS[self.page])+1 :
                    temp = (self.pivot_day + timedelta((r-1)-self.pivot_day.weekday()))
                    machaine = str(temp.year)+"-"+str(temp.month).zfill(2)+"-"+str(temp.day).zfill(2)
                    chambre = self.ROOMS[self.page][c-1] 
                    id_chambre = int(self.ROOMS[self.page][c-1])
                    id_chambre = self.controller.get_id_byNumChambre(id_chambre) 
                    resa = self.controller.get_reservation_byDateandRoomId(machaine, id_chambre) 
                    if resa != None :
                        c_height = self.element_height - 5
                        c_width = self.element_width - 5
                        margin = 5
                        client = self.controller.getClientById(resa._id_client)
                        machaineresa = client._nom + "\n" + client._prenom + "\n" + str(resa._nb_occupants) +" pers"
                        """resa_client = Button (master = data_cell,text=machaineresa, 
                                              command=lambda arg1 = resa : self.fenetre_infos_resa(arg1), 
                                              bg = COUL_RESERVATION_IMPAYEE,
                                              fg = COUL_POLICE_DATA, 
                                              font = font.Font(family = POLICE_DATA, size = POLICE_DATA_TAILLE), 
                                              height = 3)"""
    
                        canva = Canvas(master = data_cell,height = c_height, width = c_width, background= COUL_RESERVATION_IMPAYEE,  )
                        if (resa._est_reglee) :
                            canva.configure (background = COUL_RESERVATION_PAYEE)
                    
                        canva.create_text(c_width/2, c_height/2, text=machaineresa, width= 8*c_width/10, justify= 'center', font = font.Font(family = POLICE_DATA, size = POLICE_DATA_TAILLE))

                        if resa._origine == "Booking" :
                            canva.create_line(0,0, c_width/10 - margin, c_height/8, 0, c_height/4,
                            c_width/10 - margin, 3*c_height/8, 0, c_height/2, 
                            c_width/10 - margin, 5*c_height/8,  0, 6*c_height/8, 
                            c_width/10 - margin, 7*c_height/8,  0, c_height, width = 2)
                            
                            canva.create_line(c_width,0, 9*c_width/10 + margin,c_height/8, c_width, c_height/4,
                            9*c_width/10 + margin, 3*c_height/8, c_width, c_height/2, 
                            9*c_width/10 + margin, 5*c_height/8,  c_width, 6*c_height/8, 
                            9*c_width/10 + margin, 7*c_height/8,  c_width, c_height, width = 2)
                        elif resa._origine == "Fastbooking" :
                            canva.create_rectangle(0, 0, c_width/10 - margin, c_height, width = 2)
                            canva.create_rectangle(0, c_height/4 , c_width/10 - margin, 3*c_height/4, width = 2)
                            canva.create_line(0, c_height/2, c_width/10 - margin, c_height/2, width = 2)

                            canva.create_rectangle(c_width, 0, 9*c_width/10 + margin, c_height, width = 2)
                            canva.create_rectangle(c_width, c_height/4 , 9*c_width/10 + margin, 3*c_height/4, width = 2)
                            canva.create_line(c_width, c_height/2, 9*c_width/10 + margin, c_height/2, width = 2)
                        canva.bind("<Button-1>", lambda event, arg1 = resa : self.fenetre_infos_resa(arg1))


                        canva.pack()

                #########
                data_cell.configure(width=self.element_width, height = self.element_height )
                data_cell.grid(row = r, column=c,sticky=N+S+E+W)
        self.data_calendar.pack(fill=BOTH,expand = True)
        
        #creer les données a partir de old_update_data et initialisation

    def update_data(self) :
        self.destroy_data()   
        self.recreate_data()
    

    
    def next_page(self) :
      
        if self.page < len(self.ROOMS) - 1: 
            self.page = self.page + 1
            self.update_data()

    def previous_page(self):

        if self.page >  0:
            self.page = self.page - 1
            self.update_data()

########################################################
    def creer_option_infos(self):
        
        clients = self.controller.getAllClients()
        if clients != []  :   
            tab = []
            for i in range(0,len(clients)) :
                tab.append(clients[i]._nom +" "+ clients[i]._prenom+" |"+clients[i]._mail)
           
            self.client_sv.set(tab[0])
            opt = ttk.Combobox(self.master_clients, values = tab, textvariable = self.client_sv )
            opt.configure(state="readonly")
            opt.configure(height = 200, width = 30, font = font.Font(family = POLICE_COMBOBOX, size =POLICE_COMBOBOX_TAILLE))
            opt.pack(side=LEFT)
            
        ##Bouton infos client
            
            check = Button(master = self.master_clients, text = " Infos" ,height=45, command= lambda : self.fenetre_infos_client(self.client_sv), fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE), bg = COUL_BOUTON_INFOS, image= self.images["loupe"], compound="left")
            check.pack(side=LEFT, padx = 15)
          

##########################################################
    def maj_option_menu(self) :
        
        clients = self.controller.getAllClients()
        if clients != []:
            if len(self.master_clients.winfo_children()) == 0 :
                self.creer_option_infos()
            cbox = self.master_clients.winfo_children()[0]
            tab = []
            for i in range(0,len(clients)) :
                tab.append(clients[i]._nom +" "+ clients[i]._prenom+" |"+clients[i]._mail)
            self.client_sv.set(tab[0])
            cbox['values'] = tab
            
        else:
        
            while len(self.master_clients.winfo_children()) != 0 :
                self.master_clients.winfo_children()[0].destroy()
           

            

            
    
    def initialisation (self):

        ##Creation des boutons
        button_pagesuiv=Button(master = self.button_calendar, command=self.next_page ,bg =COUL_BOUTTONS_NAVIGATION, image=self.images["right"], height = self.element_height * 0.8, width = self.element_width / 2)
        button_pageprec=Button(master = self.button_calendar, command=self.previous_page,bg = COUL_BOUTTONS_NAVIGATION, image=self.images["left"], height = self.element_height * 0.8, width = self.element_width / 2)

        button_floor = Frame (master = self.data_calendar)
        button_floor.grid(row = 0, column=0,sticky=N+S+E+W)


        button_semainesuiv = Button (master = button_floor, command=self.next_week ,bg =COUL_BOUTTONS_NAVIGATION, image=self.images["down"], height = self.element_height, width = self.element_width / 2)
        button_semaineprec = Button (master = button_floor ,command=self.previous_week ,bg =COUL_BOUTTONS_NAVIGATION, image=self.images["up"], height = self.element_height, width = self.element_width / 2)
        button_pageprec.pack(side = LEFT)
        button_pagesuiv.pack(side = RIGHT)
        self.button_calendar.pack(padx = 10,pady=5,fill=BOTH, expand=False)


        button_semaineprec.pack (side = LEFT,expand = True,fill=BOTH)
        button_semainesuiv.pack (side = RIGHT,expand = True,fill=BOTH)

       

        ##Creation de la colonne des jours
        self.data_calendar.rowconfigure(0, weight=1)
        for i in range(7):
            self.data_calendar.rowconfigure(i+1, weight=1, minsize=20)
            data_cell = Frame (master=self.data_calendar, borderwidth=1,relief = RAISED)
            temp = (self.pivot_day + timedelta(i-self.pivot_day.weekday()))
            machaine = "" + JOURS[i] +" "+ str(temp.day)+ "\n" +str(MOIS[temp.month-1]) + ""
            label = Button(master=data_cell,command=lambda arg1 = temp,arg2 = self.controller  : generer_pdf(arg1, arg2), text=machaine,bg = COUL_JOURS_CAL,fg = COUL_POLICE_JOURS, font = font.Font(family = POLICE_JOURS, size =POLICE_JOURS_TAILLE))
            label.pack(fill=BOTH, side=LEFT,expand = True)
            data_cell.configure(height = self.element_height, width = self.element_width)
            data_cell.grid(row = i+1, column=0,sticky=N+S+E+W)
            


        self.update_data()
         
         
          ## Ajout nouvelle resa
        creer_resa = Button(master = self.master_add, text = " Creer Reservation", height = 0.8 * self.element_height, width = 1.3 * self.element_width, command= self.creer_reservation, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),bg = COUL_BOUTTONS_AJOUTER, image=self.images["adduser"],compound="left")
        creer_resa.pack(side=RIGHT, padx = 10, pady = 5)
        
        ## Ajout nouveau client
        creer_client = Button(master = self.master_add, text = " Ajouter Client" , height = 0.8 * self.element_height, width = 1.3 * self.element_width, command= lambda : self.fenetre_infos_client(None), fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),bg =COUL_BOUTTONS_AJOUTER ,image=self.images["adduser"],compound="left")
        creer_client.pack(side=RIGHT, padx = 10, pady = 5)
      
  
        #Option + infos 
        self.creer_option_infos()
        self.master_clients.propagate(0)
        self.master_add.pack(padx = 10,expand = False, side = RIGHT)

        self.master_clients.pack(padx = 10,fill = X, expand = False)
        self.master_calendar.pack(fill=BOTH, side=LEFT,expand = True)

        self.window.mainloop()

    def sv_to_client(self,sv,clients,client) :
        
        for c in clients :
            if clients._mail == sv.get().split(sep = "|")[1] :
                client[0] = c

################################################################################
#INFOS CLIENTS
################################################################################
        
    def fenetre_infos_client (self,client_sv) :
        if client_sv == None :
            client = Client()
        else :
            mail_client = client_sv.get().split(sep="|")[1]
            client = self.controller.getClientByMail(mail_client)
        
        window_infos = Toplevel(self.window)
        window_infos.title('Infos Clients')
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
                text="NOM :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=0,sticky=E)
        Label(master_infos, 
                text="PRENOM :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=1,sticky=E)
        Label(master_infos, 
                text="ADRESSE :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=2,sticky=E)
        Label(master_infos, 
                 text="MAIL :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=3,sticky=E)
        Label(master_infos, 
                text="TELEPHONE :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=4,sticky=E)

        e_nom = Entry(master_infos,state = "disabled",textvariable= nom_client,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE), width= 70)
        e_prenom = Entry(master_infos,state = "disabled",textvariable= prenom_client,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 70)
        e_adresse = Entry(master_infos,state = "disabled",textvariable= adresse_client,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 70)
        e_mail = Entry(master_infos,state = "disabled",textvariable= mail_client,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 70)
        e_telephone = Entry(master_infos,state = "disabled",textvariable= telephone_client,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 70)

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
                command=exit_button, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),
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
            if client._nom != "" :
                
                if client._mail == "" :
                    client._mail = client._nom + "." + client._prenom + "@bellevue.default"
                if self.controller.modifier_client_byId(client) == "MAIL EXISTANT" :
                    messagebox.showerror(title=None, message="Le client existe deja", parent = window_infos )
                else :
                    messagebox.showinfo(title = None, message= "Le client a bien été modifié", parent = window_infos)
                    self.maj_option_menu()
                    self.update_data()
            else :
                messagebox.showwarning(title = None, message= "Veuillez remplir au moins le champ nom ", parent = window_infos)
                
                      
        def activer_modif () :
            if bout_editer_frame.winfo_children()[0]['bg'] == COUL_CADENAS_FERME :
                e_nom.configure(state="normal")
                e_prenom.configure(state="normal")
                e_adresse.configure(state="normal")
                e_mail.configure(state="normal")
                e_telephone.configure(state="normal")
                bout_editer_frame.winfo_children()[0].configure(bg = COUL_CADENAS_OUVERT, image = self.images["unlock"])
                Button ( bout_quitter_frame, command=sauvegarder_infos, text = " Sauvegarder",
                height=50,width=150, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),image = self.images["disk"],compound="left").pack(side = "left")
                if client_sv != None :
                    Button (bout_quitter_frame, command= supprimer_client, text = "Supprimer",
                    height=50,width=120,fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),image= self.images["corbeille"],compound="left").pack(side = "right",padx = 15)
            else :
                e_nom.configure(state= "disabled")
                e_prenom.configure(state="disabled")
                e_adresse.configure(state="disabled")
                e_mail.configure(state="disabled")
                e_telephone.configure(state="disabled")
                bout_editer_frame.winfo_children()[0].configure(bg = COUL_CADENAS_FERME, image = self.images["lock"])
                bout_quitter_frame.winfo_children()[1].destroy()
                if client_sv != None :
                    bout_quitter_frame.winfo_children()[1].destroy()
        

        def supprimer_client():
            msgbox = messagebox.askquestion('Suppression','Êtes-vous sûr de vouloir supprimer ce client ?',icon = 'error', parent = window_infos) 
            if msgbox == 'yes' :
                self.controller.supprimer_resa_byClient(client)
                self.controller.supprimer_client_byId(client)
                window_infos.destroy()
                self.maj_option_menu()
                self.update_data()
          

        Button(bout_editer_frame, command =activer_modif, image = self.images["lock"], bg = COUL_CADENAS_FERME, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE) ).pack(fill=BOTH,expand = True)
        bout_editer_frame.propagate(0)
        bout_editer_frame.grid (row=5,column=0, sticky=W, pady=4)
        if (client_sv == None) :
            activer_modif()
            window_infos.title("Ajouter Client")

        master_infos.pack()
        window_infos.resizable(False,False)
        window_infos.mainloop()

################################################################################
#INFOS RESERVATION
################################################################################

    def fenetre_infos_resa (self,resa) :
        
        window_infos = Toplevel(self.window)
        window_infos.title("Infos Reservations")
        window_infos.withdraw()
        window_infos.after(0,window_infos.deiconify)
        master_infos = Frame(master = window_infos,padx = 10,pady= 10)
        
        id_client = resa._id_client
        client = self.controller.getClientById(id_client)
        nom_client = StringVar()
        prenom_client = StringVar()
        num_chambre = IntVar()
        nb_occupants = IntVar()
        est_reglee = IntVar()
        origine = StringVar()
        nom_client.set(client._nom)
        prenom_client.set(client._prenom)
        nb_occupants.set(resa._nb_occupants)
        est_reglee.set(resa._est_reglee)
        origine.set(resa._origine)
        liste_num_ch = []
        liste_nb_occupants = []
        liste_origine = ["", "Booking", "Fastbooking"]
        for i in range (0, self.controller.get_capacite_max_chambre()) :
            liste_nb_occupants.append(i+1)
        Label(master_infos, 
                text="NOM :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=0,sticky=E)
        Label(master_infos, 
                text="PRENOM :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=1,sticky=E)
        Label(master_infos, 
                text="CHAMBRE :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=3,column=2,sticky=E)
        Label(master_infos, 
                text="ARRIVEE :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=2,column = 0,sticky=E) 
        Label(master_infos, 
                text="DEPART :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=2,column = 2,sticky=E)
        Label(master_infos, 
                text="OCCUPANTS :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=3,column =0, sticky=E)
        Label(master_infos, 
                text="REGLEE :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=4,column =0, sticky=E)
        Label(master_infos, 
                text="ORIGINE :",fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE)).grid(row=4,column =2, sticky=E)
        
        def parameter_selected(event):
            resa._nb_occupants = e_nb_occupants.get() 
            resa._date_arrivee = e_date_arrivee.get_date()
            resa._date_depart = e_date_depart.get_date()
            liste_chambres_valides = self.controller.get_chambre_dispo(resa)
            if len(liste_chambres_valides) > 0 :
                e_num_chambre['values'] = liste_chambres_valides
                if resa._id_chambre == -1 or self.controller.getChambreById(resa._id_chambre)._numero not in liste_chambres_valides :
                   e_num_chambre.current(0)
                else :
                    e_num_chambre.current(liste_chambres_valides.index(self.controller.getChambreById(resa._id_chambre)._numero))
                
            else :
                e_num_chambre['values'] = []
                e_num_chambre.delete(0,"end")
            
        e_nom = Entry(master_infos,state = "disabled",textvariable= nom_client,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE))
        e_prenom = Entry(master_infos,state = "disabled",textvariable= prenom_client,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE))
        e_num_chambre = ttk.Combobox(master_infos,state = "disabled",textvariable= num_chambre, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 15)
        e_num_chambre['values'] = liste_num_ch
        e_nb_occupants = ttk.Combobox(master_infos,state = "disabled",textvariable = nb_occupants, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 15)
        e_nb_occupants['values'] = liste_nb_occupants
        e_nb_occupants.bind("<<ComboboxSelected>>", parameter_selected)
        e_date_arrivee = DateEntry(master_infos,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 15)
        e_date_arrivee.set_date(resa._date_arrivee)
        e_date_arrivee.bind("<<DateEntrySelected>>", parameter_selected)
        e_date_arrivee.configure(state = "disabled")
        e_date_depart = DateEntry(master_infos,fg = COUL_POLICE_CHAMPS, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 15)
        e_date_depart.set_date(resa._date_depart)
        e_date_depart.bind("<<DateEntrySelected>>", parameter_selected)
        e_date_depart.configure(state = "disabled")
        e_est_reglee = Checkbutton(master_infos,variable=est_reglee, onvalue=1, offvalue=0)
        e_est_reglee.configure(state = "disabled")
        e_origine = ttk.Combobox(master_infos,state = "disabled",textvariable = origine, font = font.Font(family = POLICE_CHAMPS, size =POLICE_CHAMPS_TAILLE),width= 15)
        e_origine['values'] = liste_origine
    




        parameter_selected(None)
        e_nom.grid(row=0, column=1,columnspan= 3,  sticky=W)
        e_prenom.grid(row=1, column=1, columnspan= 3, sticky=W)
        e_num_chambre.grid(row=3, column=3, sticky=W)

        e_date_arrivee.grid(row=2, column=1, sticky=W)
        e_date_depart.grid(row=2, column=3, sticky=W)
        e_nb_occupants.grid(row=3, column=1, sticky=W)
        e_est_reglee.grid(row = 4, column = 1, sticky=W)
        e_origine.grid(row = 4, column = 3, sticky=W)

       

        def exit_button ():
            window_infos.quit()
            window_infos.destroy()
            
       
        def sauvegarder_infos ():
            
            num_ch = e_num_chambre.get()
            resa._id_chambre = self.controller.get_id_byNumChambre(num_ch)
            resa._nb_occupants = int(e_nb_occupants.get())
            resa._date_arrivee = datetime.combine(e_date_arrivee.get_date(),datetime.min.time())
            resa._date_depart = datetime.combine(e_date_depart.get_date(),datetime.min.time())
            resa._est_reglee = int(est_reglee.get())
            resa._origine = origine.get()
            if resa._date_arrivee > resa._date_depart :
                messagebox.showerror(title=None, message="Les dates sont invalides", parent = window_infos )
            else :
                resa._id = self.controller.modifier_reservation_byId(resa)
                self.update_data()          
        
        def activer_modif () :
            if bout_editer_frame.winfo_children()[0]['bg'] == COUL_CADENAS_FERME :
                e_nb_occupants.configure(state="normal")
                e_num_chambre.configure(state="normal")
                e_date_arrivee.configure(state="normal")
                e_date_depart.configure(state="normal")
                e_est_reglee.configure(state="normal")
                e_origine.configure(state="normal")
                bout_editer_frame.winfo_children()[0].configure(bg = COUL_CADENAS_OUVERT, image = self.images["unlock"])
                Button ( bout_quitter_frame, command=sauvegarder_infos, text = " Sauvegarder",
                height=50,width=150, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),image = self.images["disk"],compound="left").pack(side = "left")
                Button (bout_quitter_frame, command= supprimer_resa, text = "Supprimer",
                height=50,width=120,fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),image= self.images["corbeille"],compound="left").pack(side = "right",padx = 15)
            else :
                e_nb_occupants.configure(state="disabled")
                e_num_chambre.configure(state="disabled")
                e_date_arrivee.configure(state="disabled")
                e_date_depart.configure(state="disabled")
                e_est_reglee.configure(state="disabled")
                e_origine.configure(state="disabled")
                bout_editer_frame.winfo_children()[0].configure(bg = COUL_CADENAS_FERME, image = self.images["lock"])
                bout_quitter_frame.winfo_children()[1].destroy()
                bout_quitter_frame.winfo_children()[1].destroy()
        
        

        def supprimer_resa():
            msgbox = messagebox.askquestion('Suppression','Êtes-vous sûr de vouloir supprimer la reservation ?',icon = 'error', parent = window_infos) 
            if msgbox == 'yes' :
                self.controller.supprimer_resa_byId(resa)
                window_infos.destroy()
                self.maj_option_menu()
                self.update_data()

        
        bout_quitter_frame = Frame (master_infos, height= 50)
        bout_editer_frame = Frame (master_infos, height= 50)
        bout_quitter_frame.propagate(0)
        bout_quitter_frame.grid (row=6,column=1,columnspan = 3, pady=(15,0),sticky= EW)
        Button( bout_quitter_frame,
                text='Quitter', 
                command=exit_button, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),
                height=50,width=120,image=self.images["quitter"],compound="left").pack(side = "right")
        bout_editer_frame = Frame (master_infos, height= 50, width = 100)
        Button(bout_editer_frame, command =activer_modif, image = self.images["lock"], bg = COUL_CADENAS_FERME, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE) ).pack(fill=BOTH,expand = True)
        bout_editer_frame.propagate(0)
        bout_editer_frame.grid (row=6,column=0, sticky=W, pady=(15,0))
        
        if resa._id == -1 :
            activer_modif()
            window_infos.title('Ajouter Reservation')

        master_infos.pack()
        window_infos.resizable(False,False)
        window_infos.mainloop()

    def creer_reservation(self) :
        def exit_button ():
            window_resa.quit()
            window_resa.destroy()
        
        def continue_button ():
            exit_button() 
            resa = Reservation(id_client_selected[0],-1,datetime.now(),datetime.now(),1)
            self.fenetre_infos_resa(resa)
        
        def client_selected(event):
            mail.set(clients[event.widget.current()]._mail)
            id_client_selected[0] = clients[event.widget.current()]._id
        
        
        #Création de la fenêtre générale
        window_resa = Toplevel(self.window)
        window_resa.title("Selectionner Client")
        clients = self.controller.getAllClients()
        id_client_selected = [-1]
        
        if clients != []  :   
            tab = []
            for i in range(0,len(clients)) :
                tab.append(clients[i]._nom +" "+ clients[i]._prenom)
        
            client = StringVar()
            mail = StringVar()
            client.set(tab[0])
            Label(window_resa,text="Selectionnez un client pour la réservation : ", font = font.Font(family = POLICE_COMBOBOX, size =POLICE_COMBOBOX_TAILLE) ).grid(row = 0, columnspan=2)
            Label(window_resa,text="Mail du client selectionné : ", font = font.Font(family = POLICE_COMBOBOX, size =POLICE_COMBOBOX_TAILLE) ).grid(row = 2, columnspan=2)
            liste_clients = ttk.Combobox(window_resa, values = tab, textvariable = client,state="readonly" )
            liste_clients.bind("<<ComboboxSelected>>",client_selected)
            liste_clients.event_generate("<<ComboboxSelected>>",when="tail")
            mail_client = Entry(window_resa,state="disabled", textvariable = mail )
            liste_clients.configure(height = 200, width = 30, font = font.Font(family = POLICE_COMBOBOX, size =POLICE_COMBOBOX_TAILLE))
            mail_client.configure(width = 30, font = font.Font(family = POLICE_COMBOBOX, size =POLICE_COMBOBOX_TAILLE))
            liste_clients.grid(row=1,columnspan=2)
            mail_client.grid(row=3,columnspan=2)
            Button(window_resa, text = "Continuer", command = continue_button, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),
            height=50,width=120,image=self.images["pixel"],compound="left").grid(row=4,column=0,sticky=W)
        else :
            Label(window_resa,text="Veuillez ajouter des clients avant de procéder à une réservation",font=font.Font(family = POLICE_COMBOBOX, size =POLICE_COMBOBOX_TAILLE) ).grid(row = 0, columnspan=2)
        
        Button( window_resa,
                text='Quitter', 
                command=exit_button, fg = COUL_POLICE_BOUTONS, font = font.Font(family = POLICE_BOUTONS, size =POLICE_BOUTONS_TAILLE),
                height=50,width=120,image=self.images["quitter"],compound="left").grid(row=4,column=1,sticky=E)
        

        

        for i in window_resa.winfo_children() :
            i.grid_configure(padx = 20,pady = 10)


        window_resa.resizable(False,False)
        window_resa.mainloop()