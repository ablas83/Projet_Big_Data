import sys
import pandas as pd

# Initialisation des variables
current_codecde = None
current_ville = None
current_nbr_timbrecde = 0
current_nbr_colis = 0

codecde = None
ville = None
nbr_timbrecde = 0
nbr_colis = 0

list_codecde = [[]]  # Initialisation d'une liste de listes (peut-être pour éviter une première comparaison)

# Parcours des lignes d'entrée
for line in sys.stdin:
    # Suppression des espaces en début et en fin de ligne
    line = line.strip()
    # Analyse de l'entrée provenant de mapper.py
    codecde, ville, nbr_colis, nbr_timbrecde = line.split(',')

    try:
        nbr_colis = float(nbr_colis)  # Conversion en nombre à virgule flottante
        nbr_timbrecde = float(nbr_timbrecde)
    except ValueError:
        continue  # Ignorer les lignes avec des valeurs non valides

    if current_codecde is None:
        # Initialisation des valeurs pour la première commande
        current_codecde = codecde
        current_ville = ville
        current_nbr_colis = nbr_colis
        current_nbr_timbrecde = nbr_timbrecde

    elif current_codecde == codecde:
        current_nbr_timbrecde += nbr_timbrecde  # Ajout du timbre cde à la commande actuelle

    else:
        list_codecde.append([current_codecde, current_ville, current_nbr_colis, round(current_nbr_timbrecde, 2)])
        current_codecde = codecde
        current_ville = ville
        current_nbr_colis = nbr_colis
        current_nbr_timbrecde = nbr_timbrecde

if current_codecde:
    list_codecde.append([current_codecde, current_ville, current_nbr_colis, round(current_nbr_timbrecde, 2)])

list_codecde.remove([])  # Suppression de la liste vide éventuellement générée en début

sorted_list_codecde = sorted(list_codecde, key=lambda x: x[2], reverse=True)[:100]

# Création d'un DataFrame pandas
df = pd.DataFrame(sorted_list_codecde, columns=['Code Commande', 'Ville', 'Nbr Colis', 'Somme timbrecde'])

# Définition du nom du fichier Excel
excel_filename = 'lot2_ex1.xlsx'

# Sauvegarde du DataFrame dans un fichier Excel
df.to_excel(excel_filename, index=False)

print(f"DataFrame saved to '{excel_filename}'.")
