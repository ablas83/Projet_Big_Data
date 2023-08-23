import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

current_objet = None
current_year = None

year = None
objet = None

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
        current_year = year
        current_nbr_commande = 1
    elif current_objet == objet:
        if current_year == year:
            current_nbr_commande += 1
        else:
            list_dict.append((current_year, current_nbr_commande))
            current_year = year
            current_nbr_commande = 1

    else:
        list_dict.append((current_year, current_nbr_commande))
        dict_annee_nbr_com_par_objet[current_objet] = list_dict
        current_objet = objet
        current_year = year
        current_nbr_commande = 1
        list_dict = []

if current_objet == objet:
    list_dict.append((current_year, current_nbr_commande))
    dict_annee_nbr_com_par_objet[current_objet] = list_dict

pdf_filename = 'plot_evolution_par_objet.pdf'  # Name of the PDF file to be generated

with PdfPages(pdf_filename) as pdf:
    for object_name, data_points in dict_annee_nbr_com_par_objet.items():
        plt.figure(figsize=(8, 5))  # Adjust the figure size if needed

        years, nbr_commande = zip(*data_points)
        plt.plot(years, nbr_commande, marker='o', label=object_name)

        plt.xlabel('Year')
        plt.ylabel('Number of Commands')
        plt.title(f'Evolution of Number of Commands for {object_name}')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        pdf.savefig()
        plt.close()


'''with open('abc3.txt', 'w') as temp_file:
    for item in dict_année_nbr_com_par_objet:
        temp_file.write("%s\n"  %item + str(dict_année_nbr_com_par_objet[item][0]) +' '
        + str(dict_année_nbr_com_par_objet[item][1]+ ' '))
'''
