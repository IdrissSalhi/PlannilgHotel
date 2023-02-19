import Src.Model
import webbrowser
import Src.Controller



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





    </style>"""


    content += "</head> \n  <body>"
    content += """<header>
        <div id=\"header_top\">
            <div id=\"infos_bellevue\">
                <h1>Hotel Bellevue</h1>
                46 rue Pasquier 75008 Paris
            </div>
            <div id=\"infos_facture\">
                <h2>FACTURE</h2>
                n°
            </div>
        </div>
        
        <div id=\"header_bottom\">
            lorem ipsum
        </div>
    </header>"""


    content+= """<div id="Tableau_detail">

    <table>
        <th>
            <td>
                a
            </td>
            <td>
                b
            </td>
        </th>

        <tr>
            <td>
                a
            </td>
            <td>
                b
            </td>
        </tr>

        <tr>
            <td>
                a
            </td>
            <td>
                b
            </td>
        </tr>



    </table>



    </div>"""


    content += "</body>"









    
    
    
    
    
    
    
    
    
    html_path = "Logs\\Factures\\Facture" + controller.getClientById(reservation._id_client)._nom + "_" + reservation._date_arrivee.strftime("%Y-%m-%d")+ "_" + reservation._date_depart.strftime("%Y-%m-%d") +".html"
    fichier_html = open(html_path,"w")
    fichier_html.write(content)
    fichier_html.close()
    webbrowser.open(html_path)