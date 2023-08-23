
import sys
import re
i = 0
for line in sys.stdin:
    line = line.replace(",,", ',"",')

    # remove leading and trailing whitespace
    if i > 0:
        line = line.strip()
        # split the line into words
        words = re.split(r'",|L,', line)
        commande = words[6].replace('"', '')
        qte = int(words[15].replace('"', '')) if words[15].replace('"', '').isdecimal() else 0
        cp = words[4].replace('"', '')
        ville = words[5].replace('"', '')
        objet = words[17].replace('"', '')
        year = int(words[7].replace('"', '').split("-")[0]) \
            if (words[7].replace('"', '').split("-")[0]).isdecimal() else 0
        if cp.startswith("53") and year >= 2010 and qte > 0:
            print('%s,%s,%s,%s,%s,%s' % (commande, ville, cp, objet, year, qte))
    i += 1
