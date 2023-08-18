import heapq
import sys
import math

current_name = None
current_city = None
current_department = None
current_nbcolis = 0
colis_per_client = {}  # Dictionnaire pour stocker les colis par client
city_per_client = {}   # Dictionnaire pour stocker les villes par client
department_per_client = {}  # Dictionnaire pour stocker les départements par client

for line in sys.stdin:
    line = line.strip()
    name, city, department, nbcolis = line.split('\t')
    try:
        nbcolis = float(nbcolis)
    except ValueError:
        continue

    if current_name is None:
        current_name = name
        current_city = city
        current_department = department
        current_nbcolis = nbcolis
    elif current_name == name:
        current_nbcolis += nbcolis
    else:
        colis_per_client[current_name] = colis_per_client.get(current_name, []) + [current_nbcolis]
        city_per_client[current_name] = current_city
        department_per_client[current_name] = current_department
        current_name = name
        current_city = city
        current_department = department
        current_nbcolis = nbcolis

if current_name:
    colis_per_client[current_name] = colis_per_client.get(current_name, []) + [current_nbcolis]
    city_per_client[current_name] = current_city
    department_per_client[current_name] = current_department

top_clients = heapq.nlargest(10, colis_per_client.keys(), key=lambda x: sum(colis_per_client[x]))

for client in top_clients:
    colis = colis_per_client[client]
    moyenne = sum(colis) / len(colis)
    ecart_type = math.sqrt(sum((x - moyenne)**2 for x in colis) / len(colis))
    city = city_per_client[client]
    department = department_per_client[client]
    print('%s\t%s\t%s\t%s\t%.2f\t%.2f' % (client, city, department, sum(colis), moyenne, ecart_type))
