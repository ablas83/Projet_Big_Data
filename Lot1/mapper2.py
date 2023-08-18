import re
import sys
import pandas as pd

i = 0
'''df = pd.read_csv('C:/Users/FORMATION/Desktop/Projet Hadoop/dataw_fro03.csv')
df['prenomcli'] = df['prenomcli'].str.replace(',', ' ')
df.to_csv("data1.csv",index = False)'''


for line in sys.stdin:
    line = line.replace(",,", ',"",')
    if i > 0:
        line = line.strip()
        fields = re.split(r'",|L,',line)
        year = int(fields[7].replace('"', '').split('-')[0]) if (fields[7].replace('"', '').split('-')[0]).isdecimal() else 0
        nbcolis = int(fields[10].replace('"', '')) if fields[10].replace('"', '') != 'NUL' else 0
        city = fields[5].replace('"', '')
        department = int(fields[4][:3].replace('"', '')) if fields[4][:3].replace('"', '').isdecimal() else 0
        if year >= 2008 and nbcolis != 0:
            print('%s,%s,%s' % (city, department, nbcolis))
    i += 1
