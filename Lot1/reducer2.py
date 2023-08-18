import heapq
import sys
import math

# Initialisation des variables pour suivre l'état en cours
current_name = None
current_city = None
current_department = None
current_nbcolis = 0

# Dictionnaires pour stocker les informations relatives à chaque client
colis_per_client = {}         # Stocke les colis par client
city_per_client = {}          # Stocke les villes par client
department_per_client = {}    # Stocke les départements par client
codcde_per_client = set()
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
        codcde_per_client.add(codcde)
    # Si le nom du client est le même que précédemment, accumule les colis
    elif current_name == name:
        current_nbcolis += nbcolis
        codcde_per_client.add(codcde)

    # Si le nom du client change, stocke les valeurs et réinitialise les variables
    else:
        clientDict = {"name": current_name, "ville": current_city, "dep":current_department, "nbcode": len(codcde_per_client)}
        liste.append(clientDict)
        colis_per_client[current_name] = colis_per_client.get(current_name, []) + [current_nbcolis]
        city_per_client[current_name] = current_city
        department_per_client[current_name] = current_department
        codcde_per_client = set()
        codcde_per_client.add(codcde)
        current_name = name
        current_city = city
        current_department = department
        current_nbcolis = nbcolis


# Stocke les valeurs du dernier client
if current_name:
    clientDict = {"name": current_name, "ville": current_city, "dep": current_department,
                  "nbcode": len(codcde_per_client)}
    liste.append(clientDict)
    colis_per_client[current_name] = colis_per_client.get(current_name, []) + [current_nbcolis]
    city_per_client[current_name] = current_city
    department_per_client[current_name] = current_department
    codcde_per_client = set()
    codcde_per_client.add(codcde)

newliste = sorted(liste, key=lambda x: x['nbcode'], reverse=True)[:10]
print(newliste)

# Parcours et affiche les informations pour chaque client
'''for client in top_clients:
    colis = colis_per_client[client]
    moyenne = sum(colis) / len(colis)
    ecart_type = math.sqrt(sum((x - moyenne)**2 for x in colis) / len(colis))
    city = city_per_client[client]
    department = department_per_client[client]
'''
