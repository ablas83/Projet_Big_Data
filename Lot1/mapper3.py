import re
import sys

i = 0


for line in sys.stdin:
    line = line.replace(",,", ',"",')
    if i > 0:
        line = line.strip()
        fields = re.split(r'",|L,',line)
        year = int(fields[7].replace('"', '').split('-')[0]) if (fields[7].replace('"', '').split('-')[0]).isdecimal() else 0
        #name = fields[0].replace('"', '') + " "+ fields[2].replace('"', '')
        objet = fields[17].replace('"', '')
        nbcolis = int(fields[10].replace('"', '')) if fields[10].replace('"', '') != 'NUL' else 0
        #city = fields[5].replace('"', '')
        department = int(fields[4][:3].replace('"', '')) if fields[4][:3].replace('"', '').isdecimal() else 0
        code_commande =  fields[6].replace('"', '')
        if department in (53,72,49) and nbcolis != 0:
            print('%s, %s, %s, %s, %s' % (objet, year, department, code_commande, nbcolis))
    i += 1 # nous voulons sauter la première ligne car il s'agit du nom des colonnes.