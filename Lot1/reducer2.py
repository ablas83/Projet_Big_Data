import statistics
import sys
from io import BytesIO

import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

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
        # le nombre de colis ne change pas tant que l'on ne change pas de commande.
        # Réinitialisation ensuite
        if current_codcde != codcde:
            colis_per_client.append(nbcolis)
            current_nbcolis += nbcolis
            current_codcde = codcde
    # Si le nom du client change, stocke les valeurs et réinitialise les variables
    else:
        moyenne = current_nbcolis / len(codcde_per_client)
        ecart_type = statistics.stdev(colis_per_client) if len(colis_per_client) > 1 else 0
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
    print("OK;Ok")

# Stocke les valeurs du dernier client
if current_name:
    moyenne = current_nbcolis / len(codcde_per_client)
    ecart_type = statistics.stdev(colis_per_client) if len(colis_per_client) > 1 else 0
    clientRow = [current_name, current_city, current_department,
                 len(codcde_per_client), current_nbcolis,
                 "%.2f" % (current_nbcolis / len(codcde_per_client)),
                 "%.2f" % ecart_type]
    liste.append(clientRow)

newliste = sorted(liste, key=lambda x: x[3], reverse=True)[:10]

# Récupérer les noms de ville uniques dans l'ordre d'apparition
villes_set = set()
villes_order = []

for row in newliste:
    ville = row[1]
    if ville not in villes_set:
        villes_order.append(ville)
        villes_set.add(ville)

# Créer un fichier PDF en utilisant le package PdfPages de matplotlib
pdf_buffer = BytesIO()
pdf_pages = PdfPages(pdf_buffer)

# Parcourir les villes dans l'ordre d'apparition
for ville in villes_order:
    # Filtrer les résultats pour la ville actuelle
    ville_rows = [row for row in newliste if row[1] == ville]

    # Créer un DataFrame pandas pour la ville
    df = pd.DataFrame(ville_rows,
                      columns=["Nom", "Ville", "Departement", "Nb Commandes", "Nb Colis", "Moy Colis/commande", "Écart Type"])

    # Créer une figure pour le tableau
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Ajouter le titre
    ax.set_title("Statistiques pour la ville de {}\nDépartement: {}".format(ville, ville_rows[0][2]))

    # Ajouter la figure au PDF
    pdf_pages.savefig(fig, bbox_inches='tight')

    # Fermer la figure
    plt.close(fig)

# Fermer les pages PDF
pdf_pages.close()

# Écrire le contenu PDF dans un fichier
with open("resultats_par_ville.pdf", "wb") as pdf_file:
    pdf_file.write(pdf_buffer.getvalue())