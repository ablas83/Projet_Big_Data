import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Initialisation des variables
current_objet = None
current_year = None
current_qte = 0

year = None
objet = None
qte = 0

dict_année_nbr_com_par_objet = {}  # Dictionnaire pour stocker les données par objet
list_dict = []  # Liste temporaire pour stocker les données par année
current_nbr_commande = 0

# Parcours des lignes d'entrée
for line in sys.stdin:
    # Suppression des espaces en début et en fin de ligne
    line = line.strip()
    # Analyse de l'entrée provenant de mapper.py
    objet, year, department, code_commande, qte = line.split(',')

    try:
        qte = float(qte)
    except ValueError:
        continue

    if current_objet is None:
        # Initialisation des valeurs pour le premier objet
        current_objet = objet
        current_year = year
        current_qte = qte
    elif current_objet == objet:
        if current_year == year:
            # Mise à jour du nombre d'objets pour la même année et le même objet
            current_qte += qte
        else:
            # Ajout des données de l'année précédente à la liste et réinitialisation
            list_dict.append((current_year, current_qte))
            current_year = year
            current_qte = qte
    else:
        # Changement d'objet, ajout des données précédentes au dictionnaire et réinitialisation
        list_dict.append((current_year, current_qte))
        dict_année_nbr_com_par_objet[current_objet] = list_dict
        current_objet = objet
        current_year = year
        current_qte = qte
        list_dict = []

# Ajout des dernières données à la liste et au dictionnaire
if current_objet == objet:
    list_dict.append((current_year, current_qte))
    dict_année_nbr_com_par_objet[current_objet] = list_dict

pdf_filename = 'plot_evolution_par_objet.pdf'  # Nom du fichier PDF à générer

# Création du fichier PDF avec les graphiques
with PdfPages(pdf_filename) as pdf:
    for object_name, data_points in dict_année_nbr_com_par_objet.items():
        plt.figure(figsize=(8, 5))  # Ajuster la taille de la figure si nécessaire

        years, nbr_objets = zip(*data_points)
        plt.plot(years, nbr_objets, marker='o', label=object_name)

        plt.xlabel('Year')
        plt.ylabel("Nombres d'objets")
        plt.title(f'Evolution de nombre d objets pour {object_name}')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        pdf.savefig()  # Sauvegarde du graphique dans le PDF
        plt.close()  # Fermeture de la figure après sauvegarde
