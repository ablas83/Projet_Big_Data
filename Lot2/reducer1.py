import sys
from operator import itemgetter
import openpyxl

current_codecde = None
current_ville = None
current_nbr_timbrecde = 0
current_nbr_colis = 0

codecde = None
ville = None
nbr_timbrecde = 0
nbr_colis = 0

list_codecde = [[]]

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    codecde, ville, nbr_colis, nbr_timbrecde = line.split(',')
    try:
        nbr_colis = float(nbr_colis)
        nbr_timbrecde = float(nbr_timbrecde)
    except ValueError:
        continue

    if current_codecde is None:
        current_codecde = codecde
        current_ville = ville
        current_nbr_colis = nbr_colis
        current_nbr_timbrecde = nbr_timbrecde

    elif current_codecde == codecde :

        current_nbr_timbrecde += nbr_timbrecde

    else:
        list_codecde.append([current_codecde, current_ville, current_nbr_colis, round(current_nbr_timbrecde, 2)])
        current_codecde = codecde
        current_ville = ville
        current_nbr_colis = nbr_colis
        current_nbr_timbrecde = nbr_timbrecde

if current_codecde:
    list_codecde.append([current_codecde, current_ville, current_nbr_colis, round(current_nbr_timbrecde, 2)])


list_codecde.remove([])

sorted_list_codecde = sorted(list_codecde, key=itemgetter(2), reverse=True)[:100]

# Créer un nouveau classeur Excel
workbook = openpyxl.Workbook()
lot2_ex1 = workbook.active

# En-tête des colonnes
header = ['Code Commande', 'Ville', 'Nbr Colis', 'Somme timbrecde']

lot2_ex1.append(header)
# Ajouter les données à la feuille Excel
for row in sorted_list_codecde:
    lot2_ex1.append(row)

# Sauvegarder le classeur Excel
excel_file_path = 'lot2_ex1.xlsx'
workbook.save(excel_file_path)

'''with open("output4.txt", "a") as f:
    for line in sorted_list_codecde:
        print(line,file=f)'''




