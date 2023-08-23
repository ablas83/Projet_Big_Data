import sys
from operator import itemgetter
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import openpyxl
from statistics import mean

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

list_codecde = [[]]

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    codecde, ville, nbr_colis, qte, points = line.split(',')
    try:
        nbr_colis = float(nbr_colis)
        qte = float(qte)
        points = float(points)
    except ValueError:
        continue

    if current_codecde is None:
        current_codecde = codecde
        current_ville = ville
        current_nbr_colis = nbr_colis
        current_nbr_commande = 1
        current_qte = qte
        current_points = points
        current_total_points = current_qte * current_points
        current_moyenne = current_total_points/current_nbr_commande

    elif current_codecde == codecde :
        current_nbr_colis = nbr_colis
        current_nbr_commande += 1
        current_qte += qte
        current_points += points
        current_total_points = current_points * current_qte
        current_moyenne = current_total_points/current_nbr_commande
    else :
        list_codecde.append([current_codecde, current_ville, current_nbr_colis, current_moyenne])
        current_codecde = codecde
        current_ville = ville
        current_nbr_colis = nbr_colis
        current_nbr_commande = 1
        current_qte = qte
        current_points = points
        current_total_points = qte * points

if current_codecde :
    list_codecde.append([current_codecde, current_ville, current_nbr_colis, current_moyenne])


list_codecde.remove([])

sorted_list_codecde = sorted(list_codecde,key=itemgetter(3),reverse=True)[:100]

random_list = random.sample(sorted_list_codecde,int(len(sorted_list_codecde)*0.05))


code = [item[0] for item in random_list]
moyennes = [item[3] for item in random_list]

# Création du graphique
fig, ax = plt.subplots()
ax.pie(moyennes, labels=code, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Assure que le graphique est un cercle et non une ellipse

# Ajouter un titre
plt.title("Répartition des moyennes de commandes totales")

# Enregistrer le graphique au format PDF
pdf_file_path = 'graphique_pie.pdf'
with PdfPages(pdf_file_path) as pdf:
    pdf.savefig(fig)
    plt.close()


# Créer un nouveau classeur Excel
workbook = openpyxl.Workbook()
lot2_ex2 = workbook.active

# En-tête des colonnes
header = ['Code Commande', 'Ville', 'Nbr Colis', 'Moyenne commandes']

lot2_ex2.append(header)
# Ajouter les données à la feuille Excel
for row in random_list:
    lot2_ex2.append(row)

# Sauvegarder le classeur Excel
excel_file_path = 'lot2_ex2.xlsx'
workbook.save(excel_file_path)

'''with open("output3.txt", "a") as f:
    for line in sorted_list_codecde:
        print(line,file=f)

'''

