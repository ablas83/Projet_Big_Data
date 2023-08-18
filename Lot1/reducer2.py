import sys

current_name = None
current_city = None
current_department = None
current_nbcolis = 0

for line in sys.stdin:
    line = line.strip()
    name, city, department, nbcolis = line.split('\t')
    try:
        nbcolis = float(nbcolis)
    except ValueError:
        continue

    if current_name is None:
        current_name = name
        current_nbcolis = nbcolis

    if current_name == name:
        current_nbcolis += nbcolis

        if current_nbcolis == nbcolis:
            current_nbcolis += nbcolis

    else:
        if current_name:
            print('%s\t%s\t%s\t%s' % (current_name, current_city, current_department, current_nbcolis))

        current_name = name
        current_city = city
        current_department = department
        current_nbcolis = nbcolis

if current_name:
    print('%s\t%s\t%s\t%s' % (current_name, current_city, current_department, current_nbcolis))