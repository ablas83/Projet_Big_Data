import sys
current_ville = None
current_commande = None
commande = None
ville = None
year = None
current_year = None
cp = None
current_cp = None
qte = None
objTable =[]
villeTable ={}
def filterCommande( list):
    commandes = []
    for commande in list:
        add = False
        list_objet = commande[2]
        for objet in list_objet:
            if objet[1] > 5:
                add = True
        if add:
            commandes.append(commande)
    return commandes

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper.py
    commande,ville,cp,objet,year,qte = line.split(',')

    try:
        qte = int(qte)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    if current_commande == commande:
        l = [item for item in objTable if item[0]==objet]
        if l:
            for i in range(len(objTable)):
                if objTable[i][0] == objet:
                    objTable[i] = (objTable[i][0], objTable[i][1]+qte)
        else:
            objTable.append((objet,qte))
    else:
        if current_ville in list(villeTable):
            villeRow = villeTable[current_ville]
            villeRow.append((current_commande,current_cp, objTable, current_year))
            villeTable[current_ville] =filterCommande (villeRow)
        else:
            villeTable[current_ville] = [(current_commande,current_cp, objTable, current_year)]
        current_commande = commande
        current_ville = ville
        current_cp = cp
        current_year = year
        objTable = [(objet,qte)]

# do not forget to output the last word if needed!
if current_commande == commande:
    if ville in villeTable.keys():
        villeRow = villeTable[ville]
        villeRow.append((commande,cp , objTable, year))
        villeTable[ville] = filterCommande(villeRow)
    else:
        villeTable[ville] = [(current_commande,cp, objTable, year)]
print("ville,codePostal,nombreCommande,objets,annee")
for ville in villeTable.keys():
    if villeTable[ville] and ville is not None:
        for commande in villeTable[ville]:
            stringObjets = "["
            objets = commande[2]
            for objet in objets:
                stringObjets += objet[0] + ","
            stringObjets += "]"
            print('%s,%s,%s,%s,%s' % (ville,commande[1],len(villeTable[ville]),stringObjets,commande[3]))

