import re
import sys

i = 0

for line in sys.stdin:
    line = line.replace(",,", ',"",')
    if i > 0:
        line = line.strip()
        fields = re.split(r'",|L,', line)
        year = int(fields[7].replace('"', '').split('-')[0]) \
            if (fields[7].replace('"', '').split('-')[0]).isdecimal() else 0
        # name = fields[0].replace('"', '') + " "+ fields[2].replace('"', '')
        # objet = fields[17].replace('"', '')
        nbcolis = int(fields[10].replace('"', '')) if fields[10].replace('"', '') != 'NUL' else 0
        city = fields[5].replace('"', '')
        timbrecde = fields[9].replace('"', '')
        # department = int(fields[4][:3].replace('"', '')) if fields[4][:3].replace('"', '').isdecimal() else 0
        code_commande = fields[6].replace('"', '')
        if 2016 >= year >= 2006:
            print('%s, %s, %s, %s' % (code_commande, city, nbcolis, timbrecde))
    i += 1  # nous voulons sauter la première ligne car il s'agit du nom des colonnes.
