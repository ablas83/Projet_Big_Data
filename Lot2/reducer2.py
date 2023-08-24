import sys
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

# Initialisation des variables
current_codecde = None
current_ville = None
current_nbr_colis = 0
current_nbr_commande = 0
current_qte = 0
current_points = 0
current_total_points = 0
current_moyenne = 0

codecde = None
ville = None
nbr_colis = 0
qte = 0
points = 0
total_points = 0

list_codecde = [[]]  # Initialisation d'une liste de listes (peut-être pour éviter une première comparaison)

# Parcours des lignes d'entrée
for line in sys.stdin:
    # Suppression des espaces en début et en fin de ligne
    line = line.strip()
    # Analyse de l'entrée provenant de mapper.py
    codecde, ville, nbr_colis, qte, points = line.split(',')

    try:
        nbr_colis = float(nbr_colis)  # Conversion en nombre à virgule flottante
        qte = float(qte)
        points = float(points)
    except ValueError:
        continue  # Ignorer les lignes avec des valeurs non valides

    if current_codecde is None:
        # Initialisation des valeurs pour la première commande
        current_codecde = codecde
        current_ville = ville
        current_nbr_colis = nbr_colis
        current_nbr_commande = 1
        current_qte = qte
        current_points = points
        current_total_points = current_qte * current_points
        current_moyenne = current_total_points / current_nbr_commande

    elif current_codecde == codecde:
        current_nbr_colis = nbr_colis
        current_nbr_commande += 1
        current_qte += qte
        current_points += points
        current_total_points = current_points * current_qte
        current_moyenne = current_total_points / current_nbr_commande
    else:
        list_codecde.append([current_codecde, current_ville, current_nbr_colis, current_moyenne])
        current_codecde = codecde
        current_ville = ville
        current_nbr_colis = nbr_colis
        current_nbr_commande = 1
        current_qte = qte
        current_points = points
        current_total_points = qte * points

if current_codecde:
    list_codecde.append([current_codecde, current_ville, current_nbr_colis, current_moyenne])

list_codecde.remove([])  # Suppression de la liste vide éventuellement générée en début

sorted_list_codecde = sorted(list_codecde, key=lambda x: x[3], reverse=True)[:100]

# Sélectionner un échantillon aléatoire de 5% des données triées
random_list = random.sample(sorted_list_codecde, int(len(sorted_list_codecde) * 0.05))

# Extraire les données pour le graphique
code = [item[0] for item in random_list]
moyennes = [item[3] for item in random_list]

# Création du graphique en secteurs (camembert)
fig, ax = plt.subplots()
ax.pie(moyennes, labels=code, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Assure que le graphique est un cercle et non une ellipse

# Ajouter un titre au graphique
plt.title("Répartition des moyennes des commandes totales")

# Enregistrer le graphique au format PDF
pdf_file_path = 'graphique_pie.pdf'
with PdfPages(pdf_file_path) as pdf:
    pdf.savefig(fig)  # Sauvegarder le graphique dans le fichier PDF
    plt.close()  # Fermer la figure après la sauvegarde

# Création d'un DataFrame pandas à partir de l'échantillon aléatoire
df = pd.DataFrame(random_list, columns=['Code Commande', 'Ville', 'Nbr Colis', 'Moyenne des commandes'])

# Définition du nom du fichier Excel
excel_filename = 'lot2_ex2.xlsx'

# Sauvegarde du DataFrame dans un fichier Excel
df.to_excel(excel_filename, index=False)

print(f"DataFrame saved to '{excel_filename}'.")
