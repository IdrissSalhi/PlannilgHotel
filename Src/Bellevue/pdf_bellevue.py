from calendar import calendar
import pdfkit
from datetime import datetime
import locale
import calendar
import Src.Model
import Src.Controller


def generer_pdf(date, controller) :
    fichier = "hotel.pdf"
    content = ""
    #chargement du fichier css
    content += "<style>"
    css = open("Src/Bellevue/pdf_bellevue.css", "r")
    lecture = css.readlines()
    for i in lecture :
        content += i
    css.close()
    content += "</style>"


    #Début doc : date
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    content += str(date.day) + " " + calendar.month_name[date.month] + " " + str(date.year)
    content += "<br><br>"

    #Table chambres 101 à 103"
    content += "<table class=principale>"
    content += "<tr class=tr_principale>"
    for j in range (1,4):
        content += "<td>"
        content += "<table><tr class = bordures>"
        resa = controller.get_reservation_byDateandRoomId(str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)
            , controller.get_id_byNumChambre(100+j))
    
        if resa != None and date.date() == resa._date_arrivee.date() :
            content += "<td class=\"num_chambre arrive_ajd\">"
        else :
            content += "<td class=num_chambre>"
        content += str(100+j)
       
        content += "</td><td class=client>"
                
         
        if resa != None :
            client = controller.getClientById(resa._id_client)
            content += " " +  client._nom + " " + client._prenom 
        
        
        if j==3 :
            content += "</td><td class = \"nb_nuits fin_de_ligne\">"
        else :
            content += "</td><td class = nb_nuits>"    
        
        if resa != None:
            content += " " + str(resa.getNuitees(date)) + "j "


        content += "</td></tr></table>"
        content += "</td>"
    content += "</tr>"
    content += "</table>"

    #Table chambres 201 à 406"
    content += "<table class=principale>"
    for i in range(1,7) :
        content += "<tr class=tr_principale>"
        for j in range (2,5):
            content += "<td>"
            content += "<table><tr>"
            resa = controller.get_reservation_byDateandRoomId(str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)
            , controller.get_id_byNumChambre(100*j+i))
    
            if resa != None and date.date() == resa._date_arrivee.date() :
                content += "<td class=\"num_chambre arrive_ajd\">"
            else :
                content += "<td class=num_chambre>"
            
            content += str(100*j+i)
       
            
            content += "</td><td class=client>"

            if resa != None :
                client = controller.getClientById(resa._id_client)
                content += " " +  client._nom + " " + client._prenom 
        
        
            if j==4 :
                content += "</td><td class = \"nb_nuits fin_de_ligne\">"
            else :
                content += "</td><td class = nb_nuits>"    
        
            if resa != None:
                content += " " + str(resa.getNuitees(date)) + "j "
            content += "</td></tr></table>"
            content += "</td>"
        content += "</tr>"

    content += "</table>"

    #Table chambres 501 à 706"
    content += "<table class=principale>"
    for i in range(1,7) :
        content += "<tr class=tr_principale>"
        for j in range (5,8):
            content += "<td>"
            content += "<table><tr>"
            resa = controller.get_reservation_byDateandRoomId(str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)
            , controller.get_id_byNumChambre(100*j+i))
    
            if resa != None and date.date() == resa._date_arrivee.date() :
                content += "<td class=\"num_chambre arrive_ajd\">"
            else :
                content += "<td class=num_chambre>"
            content += str(100*j+i)
            
            content += "</td><td class=client>"

            if resa != None :
                client = controller.getClientById(resa._id_client)
                content += " " +  client._nom + " " + client._prenom 
        
        
            if j==7 :
                content += "</td><td class = \"nb_nuits fin_de_ligne\">"
            else :
                content += "</td><td class = nb_nuits>"    
            
            if resa != None:
                content += " " + str(resa.getNuitees(date)) + "j "
                
            content += "</td></tr></table>"
            content += "</td>"
        content += "</tr>"

    content += "</table>"

    #Table encodage cartes"
    content += "<table class=principale>"
    cpt = 1
    centaine = 1
    for i in range(0,4) :
        content += "<tr class=\"tr_principale encodage\">"
        for j in range (0,10):
            content += "<td>"
            content += "<table><tr><td class=\"num_chambre encodage\">"
            if (i == 0 and j == 3) or (cpt == 7):
                centaine += 1 
                cpt = 1
            if centaine != 8 :
                content += str(100*centaine+cpt)
            else :
                content += " X "
            cpt += 1
            if j == 9 :
                content += "</td><td class=\"encodage_client fin_de_ligne\"></td></tr></table>"
            else :
                content += "</td><td class=encodage_client></td></tr></table>"
            content += "</td> "
        content += "</tr>"

    content += "</table>"









    f = open("essai.html","w")
    f.write(content)
    f.close()
    #pdfkit.from_string(content, fichier)