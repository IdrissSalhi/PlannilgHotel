from calendar import calendar
from datetime import datetime
import calendar
import Src.Model
import Src.Controller
import webbrowser


def generer_pdf(date, controller) :
    content = ""
    #chargement css
    content += "<style>"
    content += """.principale{
    border : none;
    border-collapse: collapse;
    margin: 5% 0;
}

table{  
    width: 100%;
}

.bordures{
    border-left: 1px solid black;
    border-right: 1px solid black;
    padding-top: 20%;
}

.tr_principale{
    border: 1px solid black;
}

.tr_principale:not(.encodage) > td{
    width: 33%;
}

.num_chambre{ 
    font-weight: bold;
    font-size: larger;
}

.num_chambre:not(.encodage):not(.arrive_ajd) {
    padding: 20;
}

.arrive_ajd{
    padding: 18;
    border-radius: 50%;
    border: 2px solid black;   
}

.client{
    border-left: 1px solid black;
    width: 80%;
    padding-left: 2%;    
}

.nb_nuits{
    width: 5%;
}

.nb_nuits:not(.fin_de_ligne){
    border-right: 1px solid black;
    padding-right: 20%;
}

.encodage_client{
    border-left: 1px solid black;
    width: 80%;
    padding-left: 2%; }

.encodage_client:not(.fin_de_ligne){
    border-right: 1px solid black;
    width: 80%;
    padding-left: 2%; }"""
    content += "</style>"


    #Début doc : date
    content += str(date.day) + " " + calendar.month_name[date.month] + " " + str(date.year)
    content += "<br><br>"

    #Table chambres 101 à 103"
    content += "<table class=principale>"
    content += "<tr class=tr_principale>"
    for j in range (1,4):
        content += "<td>"
        content += "<table><tr class = bordures>"
        resa_pdf = controller.get_reservation_byDateandRoomId(str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)
            , controller.get_id_byNumChambre(100+j))
    
        if resa_pdf != None and date.date() == resa_pdf._date_arrivee.date() :
            content += "<td class=\"num_chambre arrive_ajd\">"
        else :
            content += "<td class=num_chambre>"
        content += str(100+j)
       
        content += "</td><td class=client>"
                
         
        if resa_pdf != None :
            client_pdf = controller.getClientById(resa_pdf._id_client)
            content += " " +  client_pdf._nom + " " + client_pdf._prenom 
        
        
        if j==3 :
            content += "</td><td class = \"nb_nuits fin_de_ligne\">"
        else :
            content += "</td><td class = nb_nuits>"    
        
        if resa_pdf != None:
            content += " " + str(resa_pdf.getNuitees(date)) + "j "


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
            resa_pdf = controller.get_reservation_byDateandRoomId(str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)
            , controller.get_id_byNumChambre(100*j+i))
    
            if resa_pdf != None and date.date() == resa_pdf._date_arrivee.date() :
                content += "<td class=\"num_chambre arrive_ajd\">"
            else :
                content += "<td class=num_chambre>"
            
            content += str(100*j+i)
       
            
            content += "</td><td class=client>"

            if resa_pdf != None :
                client_pdf = controller.getClientById(resa_pdf._id_client)
                content += " " +  client_pdf._nom + " " + client_pdf._prenom 
        
        
            if j==4 :
                content += "</td><td class = \"nb_nuits fin_de_ligne\">"
            else :
                content += "</td><td class = nb_nuits>"    
        
            if resa_pdf != None:
                content += " " + str(resa_pdf.getNuitees(date)) + "j "
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
            resa_pdf = controller.get_reservation_byDateandRoomId(str(date.year)+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)
            , controller.get_id_byNumChambre(100*j+i))
    
            if resa_pdf != None and date.date() == resa_pdf._date_arrivee.date() :
                content += "<td class=\"num_chambre arrive_ajd\">"
            else :
                content += "<td class=num_chambre>"
            content += str(100*j+i)
            
            content += "</td><td class=client>"

            if resa_pdf != None :
                client_pdf = controller.getClientById(resa_pdf._id_client)
                content += " " +  client_pdf._nom + " " + client_pdf._prenom 
        
        
            if j==7 :
                content += "</td><td class = \"nb_nuits fin_de_ligne\">"
            else :
                content += "</td><td class = nb_nuits>"    
            
            if resa_pdf != None:
                content += " " + str(resa_pdf.getNuitees(date)) + "j "
                
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








    html_path = "Logs\\Feuilles_de_jour\\feuille_du_jour_" + str(date.day) + "-" + calendar.month_name[date.month] + "-" + str(date.year)+".html"
    fichier_html = open(html_path,"w")
    fichier_html.write(content)
    fichier_html.close()
    webbrowser.open(html_path)
