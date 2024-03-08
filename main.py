import pandas as pd
import numpy as np
pays = ["Serbia", "Bulgaria", "Macedonia", "Romania", "Greece", "Montenegro","Albania", "B&H", "Croatia", "Slovenia"]
critere = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"]
donnees = pd.read_csv("donnees.csv", header=None)
poids = pd.read_csv("poids.csv", header=None)

matrice_promethee = np.zeros((len(pays), len(pays)))
matrice_electre = np.zeros((len(pays), len(pays))) 
for i_first in range(len(pays)):
    for i_second in range(len(pays)):
        if i_first == i_second:
            continue
        score_promethee = 0
        score_electre = 0
        for j in range(len(critere)):
            if donnees.iloc[j, i_first] > donnees.iloc[j, i_second]:
                score_promethee += poids[j]
            if donnees.iloc[j, i_first] >= donnees.iloc[j, i_second]:
                score_electre += poids[j]
        matrice_promethee [i_first][i_second] = score_promethee
        matrice_electre[i_first][i_second] = score_electre

matrice = pd.DataFrame(matrice_promethee, index=pays, columns=pays)
matrice.to_csv("matrice_promethee.csv", sep=';', decimal=',', float_format='%.2f')
matrice = pd.DataFrame(matrice_electre, index=pays, columns=pays)
matrice.to_csv("matrice_electre.csv", sep=';', decimal=',', float_format='%.2f')

fplus_data = matrice_promethee.sum(axis=1)
fplus = pd.DataFrame({"Country": pays, "fplus": fplus_data})
fplus = fplus.sort_values(by='fplus', ascending=False)

fmoins_data = matrice_promethee.sum(axis=0)
fmoins = pd.DataFrame({"Country": pays, "fmoins": fmoins_data})
fmoins = fmoins.sort_values(by='fmoins', ascending=True)

fnet_data = fplus_data - fmoins_data
fnet = pd.DataFrame({"Country": pays, "fnet": fnet_data})
fnet = fnet.sort_values(by='fnet', ascending=False)

print(fplus)
print(fmoins)
print(fnet)