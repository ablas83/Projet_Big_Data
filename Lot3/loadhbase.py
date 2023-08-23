import json

import happybase
import csv

connection = happybase.Connection("127.0.0.1", 9090)
connection.create_table("fromagerie", {"cf1": dict(max_versions=1)})


table = connection.table("fromagerie")
with open("dataw_fro03.csv", "r", encoding="utf8") as f:
    DictReader_obj = csv.DictReader(f)
    i = 0
    for item in DictReader_obj:
        s = "" + str(i)
        table.put(
            s,
            {
                "cf1:codcli": item['\ufeff"codcli"'],
                "cf1:genrecli": item["genrecli"],
                "cf1:nomcli": item["nomcli"],
                "cf1:prenomcli": item["prenomcli"],
                "cf1:cpcli": item["cpcli"],
                "cf1:villecli": item["villecli"],
                "cf1:codcde": item["codcde"],
                "cf1:datcde": item["datcde"] if item["datcde"] != "NULL" else "",
                "cf1:timbrecli": item["timbrecli"]
                if item["timbrecli"] != "NULL"
                else "0",
                "cf1:timbrecde": item["timbrecde"]
                if item["timbrecde"] != "NULL"
                else "0.0",
                "cf1:Nbcolis": item["Nbcolis"] if item["Nbcolis"] != "NULL" else "0",
                "cf1:cheqcli": item["cheqcli"],
                "cf1:barchive": item["barchive"],
                "cf1:bstock": item["bstock"],
                "cf1:codobj": item["codobj"],
                "cf1:qte": item["qte"] if item["qte"] != "NULL" else "0",
                "cf1:Colis": item["Colis"] if item["Colis"] != "NULL" else "0",
                "cf1:libobj": item["libobj"],
                "cf1:Tailleobj": item["Tailleobj"],
                "cf1:Poidsobj": item["Poidsobj"],
                "cf1:points": item["points"] if item["points"] != "NULL" else "0",
                "cf1:indispobj": item["indispobj"],
                "cf1:libcondit": item["libcondit"],
                "cf1:prixcond": item["prixcond"],
                "cf1:puobj": item["puobj"],
            },
        )
        i += 1
        print(i)
