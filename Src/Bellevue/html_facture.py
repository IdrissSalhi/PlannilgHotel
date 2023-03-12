import Src.Model
import webbrowser
import Src.Controller
from Src.Config import *
from datetime import *



def generer_facture(reservation : Src.Model.Reservation, controller) :
    content = "<head>"
    content = """ <style>

    @media print {
    body{
        width: 21cm;
        height: 29.7cm;
        margin: 5mm 5mm 5mm 5mm;
        } 
    }


    header{
        display:flex;
        flex-direction: column;
    }

    #header_top{
        display:flex;
        flex-direction: row;
        justify-content: space-between;
    }

    tr,td,th{
        border: 1px solid black;
    }



    </style>"""


    content += "</head> \n  <body>"
    content += """<header>
        <div id=\"header_top\">
            <div id=\"infos_bellevue\">
                <h1>Hotel Bellevue</h1>
                SARL TOURDES & CIE
                46 rue Pasquier - 75008 PARIS <br>
                Téléphone 0143875068 <br>
                bellevue.saint.lazare@wanadoo.fr
            </div>
            <div id=\"infos_facture\">
                <h2>FACTURE</h2>
                n°"""
    content += str(datetime.now().year)+"."+ str(datetime.now().month)
    content += """</div>
        </div>
        
        <div id=\"header_bottom\">
        CHAMBRE N°"""
    content += str(controller.getChambreById(reservation._id_chambre)._numero)
    content += "<br>"
    content += str(controller.getClientById(reservation._id_client)._nom)+"  "+ str(controller.getClientById(reservation._id_client)._prenom)
    content += """</div>
    </header>"""

    
    content+= """<div id="Tableau_detail">

    <table>
        <tr>
            <th>
               DATE 
            </th>"""
    for i in range(0,len(reservation._couts)):
        content+=" <th> le "
        content+= JOURS[reservation._couts[i]._date_jour.weekday()] 
        content+= "<br>"
        content+=str(reservation._couts[i]._date_jour.day)+ "\n" +str(MOIS[reservation._couts[i]._date_jour.month-1]) + "\n" + str(reservation._couts[i]._date_jour.year)
        content+="</th>"
    content+= "</tr>"

    content+="""<tr>
            <td> CHAMBRE </td>"""
    for i in range(0,len(reservation._couts)):
        content += "<td>"
        content += str(reservation._couts[i]._total_chambre)
        content +="</td>"
    content += "</tr>"

    content += """<tr>
            <td> PETIT-DEJ </td>"""
    for i in range(0,len(reservation._couts)):
        content += "<td>"
        content += str(reservation._couts[i]._total_petit_dej)
        content +="</td>"
    content += "</tr>"
        
    content +=  """<tr>
            <td>TELEPHONE </td>"""
    for i in range(0,len(reservation._couts)):
        content += "<td>"
        content += str(reservation._couts[i]._total_telephone)
        content +="</td>"
    content += "</tr>"
        
    content +=  """    <tr>
            <td>BAR </td>"""
    for i in range(0,len(reservation._couts)):
        content += "<td>"
        content += str(reservation._couts[i]._total_bar)
        content +="</td>"
    content += "</tr>"
    content+= """    <tr>
            <td>  </td>"""
    for i in range(0,len(reservation._couts)):
        content+= "<td><br></td>"
    content += "</tr>"
    content+= """     <tr>
            <td> </td>"""
    for i in range(0,len(reservation._couts)):
        content+= "<td><br></td>"
    content += "</tr>"
    content+= """    <tr>
            <td>  </td>"""
    for i in range(0,len(reservation._couts)):
        content+= "<td><br></td>"
    content += "</tr>"
    content+= """     <tr>
            <td>TAXE SEJOUR</td>"""
    for i in range(0,len(reservation._couts)):
        content += "<td>"
        content += str(reservation._couts[i]._total_taxe_sejour)
        content +="</td>"
    content += "</tr>"
    content+= """    <tr>
            <td> TOTAL JOUR </td>"""
    for i in range(0,len(reservation._couts)):
        content += "<td>"
        content += str(reservation._couts[i]._total_chambre + reservation._couts[i]._total_petit_dej + reservation._couts[i]._total_telephone + reservation._couts[i]._total_bar + reservation._couts[i]._total_taxe_sejour)
        content +="</td>"

    content+= """</table>



    </div>"""


    content += "</body>"









    
    
    
    
    
    
    
    
    
    html_path = "Logs\\Factures\\Facture" + controller.getClientById(reservation._id_client)._nom + "_" + reservation._date_arrivee.strftime("%Y-%m-%d")+ "_" + reservation._date_depart.strftime("%Y-%m-%d") +".html"
    fichier_html = open(html_path,"w")
    fichier_html.write(content)
    fichier_html.close()
    webbrowser.open(html_path)