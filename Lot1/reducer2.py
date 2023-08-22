import math
import sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO

# Initialisation des variables pour suivre l'état en cours
current_name = None
current_city = None
current_department = None
current_nbcolis = 0
current_codcde = 0
codcde_per_client = set()
colis_per_client = []  # Liste pour calculer l'écart type
liste = []

# Parcourir chaque ligne d'entrée
for line in sys.stdin:
    line = line.strip()
    name, city, department, codcde, nbcolis = line.split('\t')
    try:
        nbcolis = float(nbcolis)
    except ValueError:
        continue

    # Si c'est le premier client traité, initialise les valeurs
    if current_name is None:
        current_name = name
        current_city = city
        current_department = department
        current_nbcolis = nbcolis
        current_codcde = codcde
        codcde_per_client.add(codcde)
        colis_per_client.append(nbcolis)
    # Si le nom du client est le même que précédemment, accumule les colis
    elif current_name == name:
        codcde_per_client.add(codcde)
        # le nombre de colis ne change pas tant que l'on ne change pas de commande. Réinitialisation ensuite
        if current_codcde != codcde:
            colis_per_client.append(nbcolis)
            current_nbcolis += nbcolis
            current_codcde = codcde
    # Si le nom du client change, stocke les valeurs et réinitialise les variables
    else:
        moyenne = current_nbcolis / len(codcde_per_client)
        somme_carres_ecarts = sum((x - moyenne) ** 2 for x in colis_per_client)
        variance = somme_carres_ecarts / len(colis_per_client)
        ecart_type = math.sqrt(variance)
        clientRow = [current_name, current_city, current_department,
                     len(codcde_per_client), current_nbcolis,
                     "%.2f" % (current_nbcolis / len(codcde_per_client)),
                     "%.2f" % ecart_type]
        liste.append(clientRow)
        colis_per_client = [nbcolis]
        codcde_per_client = set()
        codcde_per_client.add(codcde)
        current_name = name
        current_city = city
        current_codcde = codcde
        current_department = department
        current_nbcolis = nbcolis

# Stocke les valeurs du dernier client
if current_name:
    moyenne = current_nbcolis / len(codcde_per_client)
    somme_carres_ecarts = sum((x - moyenne) ** 2 for x in colis_per_client)
    variance = somme_carres_ecarts / len(colis_per_client)
    ecart_type = math.sqrt(variance)
    clientRow = [current_name, current_city, current_department,
                 len(codcde_per_client), current_nbcolis,
                 "%.2f" % (current_nbcolis / len(codcde_per_client)),
                 "%.2f" % ecart_type]
    liste.append(clientRow)

newliste = sorted(liste, key=lambda x: x[3], reverse=True)[:10]
print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
    "Nom", "Ville", "Departement", "Nb Commandes", "Nb Colis", "Moy Colis par commande", "Ecart Type"))
for row in newliste:
    print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(*row))


# Récupérer les noms de ville uniques dans l'ordre d'apparition
villes_set = set()
villes_order = []

for row in newliste:
    ville = row[1]
    if ville not in villes_set:
        villes_order.append(ville)
        villes_set.add(ville)

# Créer un fichier PDF en utilisant la bibliothèque reportlab
pdf_buffer = BytesIO()
doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))
elements = []

# Styles pour les en-têtes et les cellules
styles = getSampleStyleSheet()
header_style = styles['Heading1']
header_style.alignment = TA_CENTER
cell_style = ParagraphStyle('TableCellStyle', alignment=TA_LEFT)

# Parcourir les villes dans l'ordre d'apparition
for ville in villes_order:
    # Filtrer les résultats pour la ville actuelle
    ville_rows = [row for row in newliste if row[1] == ville]

    # En-tête de la ville (nom de la ville et numéro de département)
    ville_header = Paragraph("<b>Ville:</b> {}<br/><b>Département:</b> {}"
                             .format(ville, ville_rows[0][2]), header_style)
    elements.append(ville_header)

    # En-têtes de colonnes pour le tableau
    header = ["Nom", "Nb Commandes", "Nb Colis", "Moy Colis/commande", "Écart Type"]
    data = [header] + [[row[0], row[3], row[4], row[5], row[6]] for row in ville_rows]

    # Créer une table avec les données de la ville
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    elements.append(table)
    elements.append(PageBreak())  # Saut de page après chaque tableau de ville

# Construire le document PDF
doc.build(elements)

# Écrire le contenu PDF dans un fichier
with open("Lot1/resultats_par_ville_exo2.pdf", "wb") as pdf_file:
    pdf_file.write(pdf_buffer.getvalue())
