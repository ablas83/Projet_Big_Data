import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


current_objet = None
current_year = None
current_department = None

year = None
objet = None
department = None

dict_annee_nbr_com_par_objet = {}
list_dict = []
current_nbr_commande = 0

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    objet, year, department, code_commande, nbcolis = line.split(',')

    if current_objet is None:
        current_objet = objet
        current_department = department
        current_year = year
        current_nbr_commande = 1
    elif current_objet == objet:
        if current_year == year:
            if current_department == department:
                current_nbr_commande += 1
            else:
                list_dict.append((current_year, current_department, current_nbr_commande))
                current_year = year
                current_department = department
                current_nbr_commande = 1
        else:
            list_dict.append((current_year, current_department, current_nbr_commande))
            current_year = year
            current_department = department
            current_nbr_commande = 1

    else:
        list_dict.append((current_year, current_department, current_nbr_commande))
        dict_annee_nbr_com_par_objet[current_objet] = list_dict
        current_objet = objet
        current_year = year
        current_department = department
        current_nbr_commande = 1
        list_dict = []

if current_objet == objet:
    list_dict.append((current_year, current_department, current_nbr_commande))
    dict_annee_nbr_com_par_objet[current_objet] = list_dict

pdf_filename = 'plot_evolution_par_objet_departement.pdf'  # Nom du fichier PDF à générer

with PdfPages(pdf_filename) as pdf:
    for object_name, data_points in dict_annee_nbr_com_par_objet.items():
        departments = set([department for _, department, _ in data_points])

        for department in departments:
            plt.figure(figsize=(8, 5))  # Ajustez la taille de la figure si nécessaire

            filtered_data = [(year, nbr_commande) for year, dep, nbr_commande in data_points if dep == department]
            years, nbr_commande = zip(*filtered_data)

            plt.plot(years, nbr_commande, marker='o', label=f'Department {department}')
            plt.xlabel('Année')
            plt.ylabel('Nombre de commandes')
            plt.title(f'Évolution du nombre de commandes pour {object_name} - Department {department}')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()

            pdf.savefig()
            plt.close()
