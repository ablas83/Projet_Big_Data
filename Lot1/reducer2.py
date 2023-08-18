import heapq
import sys

current_name = None
current_city = None
current_department = None
current_nbcolis = 0
list = []

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

    if current_name == name:
        current_nbcolis += nbcolis

    else:
        if current_name:
            list.append((current_name, current_city, current_department, current_nbcolis))

        current_name = name
        current_city = city
        current_department = department
        current_nbcolis = nbcolis

if current_name:
    list.append((current_name, current_city, current_department, current_nbcolis))

# Utilisation de heapq.nlargest pour obtenir les 10 premiers clients les plus fidèles
top_clients = heapq.nlargest(10, list, key=lambda x: x[3])

for client in top_clients:
    print('%s\t%s\t%s\t%s' % (client[0], client[1], client[2], client[3]))  # Impression des valeurs des clients fidèles
