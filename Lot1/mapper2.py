import re
import sys

i = 0


for line in sys.stdin:
    line = line.replace(",,", ',"",')
    if i > 0:
        line = line.strip()
        fields = re.split(r'",|L,',line)
        year = int(fields[7].replace('"', '').split('-')[0]) if (fields[7].replace('"', '').split('-')[0]).isdecimal() else 0
        name = fields[0].replace('"', '') + " "+ fields[2].replace('"', '')
        nbcolis = int(fields[10].replace('"', '')) if fields[10].replace('"', '') != 'NUL' else 0
        city = fields[5].replace('"', '')
        department = int(fields[4][:3].replace('"', '')) if fields[4][:3].replace('"', '').isdecimal() else 0
        if year >= 2008 and nbcolis != 0:
            print('%s\t%s\t%s\t%s' % (name, city, department, nbcolis))
    i += 1 # nous voulons sauter la première ligne car il s'agit du nom des colonnes.
