import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Initialisation des variables
current_objet = None
current_year = None
current_department = None
current_qte = 0

year = None
objet = None
department = None
qte = 0

dict_année_nbr_com_par_objet = {}  # Dictionnaire pour stocker les données par objet
list_dict = []  # Liste temporaire pour stocker les données par année et département

for line in sys.stdin:
    # Suppression des espaces en début et en fin de ligne
    line = line.strip()
    # Analyse de l'entrée provenant de mapper.py
    objet, year, department, code_commande, qte = line.split(',')

    try:
        qte = float(qte)  # Conversion de la quantité en nombre à virgule flottante
    except ValueError:
        continue  # Ignorer les lignes avec des quantités non valides

    if current_objet is None:
        # Initialisation des valeurs pour le premier objet
        current_objet = objet
        current_department = department
        current_year = year
        current_qte = qte
    elif current_objet == objet:
        if current_year == year:
            if current_department == department:
                current_qte += qte  # Ajout de la quantité à la quantité actuelle
            else:
                list_dict.append((current_year, current_department, current_qte))
                current_year = year
                current_department = department
                current_qte = qte
        else:
            list_dict.append((current_year, current_department, current_qte))
            current_year = year
            current_department = department
            current_qte = qte
    else:
        list_dict.append((current_year, current_department, current_qte))
        dict_année_nbr_com_par_objet[current_objet] = list_dict
        current_objet = objet
        current_year = year
        current_department = department
        current_qte = qte
        list_dict = []

if current_objet == objet:
    list_dict.append((current_year, current_department, current_qte))
    dict_année_nbr_com_par_objet[current_objet] = list_dict

pdf_filename = 'plot_evolution_par_objet_departement.pdf'  # Nom du fichier PDF à générer

# Création du fichier PDF avec les graphiques
with PdfPages(pdf_filename) as pdf:
    for object_name, data_points in dict_année_nbr_com_par_objet.items():
        departments = set([department for _, department, _ in data_points])

        for department in departments:
            plt.figure(figsize=(8, 5))  # Ajuster la taille de la figure si nécessaire

            filtered_data = [(year, nbr_objets) for year, dep, nbr_objets in data_points if dep == department]
            years, nbr_objets = zip(*filtered_data)

            plt.plot(years, nbr_objets, marker='o', label=f'Department {department}')
            plt.xlabel('Année')
            plt.ylabel('Nombre d\'objets')
            plt.title(f'Évolution du nombre d\'objets pour {object_name} - Département {department}')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()

            pdf.savefig()  # Sauvegarde du graphique dans le PDF
            plt.close()  # Fermeture de la figure après sauvegarde
