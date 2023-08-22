import re
import sys

# Initialisation du compteur pour sauter la première ligne
i = 0

for line in sys.stdin:
    # Remplace les virgules adjacentes par une virgule vide entre guillemets
    line = line.replace(",,", ',"",')

    # Vérifie si nous avons dépassé la première ligne
    if i > 0:
        line = line.strip()
        fields = re.split(r'",|L,', line)

        # Extraction des informations pertinentes
        year = int(fields[7].replace('"', '').split('-')[0]) if (
        fields[7].replace('"', '').split('-')[0]).isdecimal() else 0
        name = fields[0].replace('"', '') + " " + fields[2].replace('"', '')
        codcde = fields[6].replace('"', '')
        nbcolis = int(fields[10].replace('"', '')) if fields[10].replace('"', '') != 'NUL' else 0
        city = fields[5].replace('"', '')
        department = int(fields[4][:3].replace('"', '')) \
            if fields[4][:3].replace('"', '').isdecimal() else 0

        # Vérifie si l'année est supérieure ou égale à 2008 et si le nombre de colis n'est pas nul
        # (les vides et erreurs ayant été transformés en 0)
        if year >= 2008 and nbcolis != 0:
            print('%s\t%s\t%s\t%s\t%s' % (name, city, department, codcde, nbcolis))

    # Incrémente le compteur pour sauter la première ligne
    i += 1
