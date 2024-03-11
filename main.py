import pandas as pd
import numpy as np
pays = ["Serbia", "Bulgaria", "Macedonia", "Romania", "Greece", "Montenegro","Albania", "Bosnia and Herzegovina", "Croatia", "Slovenia"]
critere = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"]
donnees = pd.read_csv("data/donnees.csv", header=None)
poids = pd.read_csv("data/poids.csv", header=None)

# Changement de poids pour que le total soit égale à 1
poids.iloc[0, 4] = 0.08
print(poids)

# Creer les matrice de degrés de préférence multicritère pour promethee et electre
matrice_promethee = np.zeros((len(pays), len(pays)))
matrice_electre = np.zeros((len(pays), len(pays))) 
matrice_promethee_preference = np.zeros((len(pays), len(pays)))
matrice_electre_preference = np.zeros((len(pays), len(pays))) 
seuil_preference = 2
for i_first in range(len(pays)):
    for i_second in range(len(pays)):
        if i_first == i_second:
            continue
        score_promethee = 0
        score_electre = 0
        score_promethee_preference = 0
        score_electre_preference = 0
        for j in range(len(critere)):
            
            #promethee
            if donnees.iloc[j, i_first] > donnees.iloc[j, i_second]:
                if donnees.iloc[j, i_first] > donnees.iloc[j, i_second]+seuil_preference:
                    score_promethee_preference += poids[j]
                else:
                    score_promethee_preference += poids[j]*((donnees.iloc[j, i_first]-donnees.iloc[j, i_second])/seuil_preference)
                score_promethee += poids[j]
            
            #electre
            if donnees.iloc[j, i_first] >= donnees.iloc[j, i_second]:
                if donnees.iloc[j, i_first] > donnees.iloc[j, i_second]+seuil_preference:
                    score_electre_preference += poids[j]
                else:
                    score_electre_preference += poids[j]*(1-((donnees.iloc[j, i_first]-donnees.iloc[j, i_second])/seuil_preference))
                score_electre += poids[j]
            
        matrice_promethee [i_first][i_second] = score_promethee
        matrice_electre[i_first][i_second] = score_electre
        matrice_promethee_preference [i_first][i_second] = score_promethee_preference
        matrice_electre_preference[i_first][i_second] = score_electre_preference

matrice = pd.DataFrame(matrice_promethee, index=pays, columns=pays)
matrice.to_csv("generatedData/matrice_promethee.csv", sep=';', decimal=',', float_format='%.2f')
matrice = pd.DataFrame(matrice_electre, index=pays, columns=pays)
matrice.to_csv("generatedData/matrice_electre.csv", sep=';', decimal=',', float_format='%.2f')
matrice = pd.DataFrame(matrice_promethee_preference, index=pays, columns=pays)
matrice.to_csv("generatedData/matrice_promethee_preference.csv", sep=';', decimal=',', float_format='%.2f')
matrice = pd.DataFrame(matrice_electre_preference, index=pays, columns=pays)
matrice.to_csv("generatedData/matrice_electre_preference.csv", sep=';', decimal=',', float_format='%.2f')

#Calcul des flux
# Calcul flux positifs Φ+
fplus_data = matrice_promethee.sum(axis=1)
fplus = pd.DataFrame({"Country": pays, "fplus": fplus_data})
fplus = fplus.sort_values(by='fplus', ascending=False)
fplus.to_csv("generatedData/fplus.csv", sep=';', decimal=',', float_format='%.2f')

# Calcul flux négatifs Φ-
fmoins_data = matrice_promethee.sum(axis=0)
fmoins = pd.DataFrame({"Country": pays, "fmoins": fmoins_data})
fmoins = fmoins.sort_values(by='fmoins', ascending=True)
fmoins.to_csv("generatedData/fmoins.csv", sep=';', decimal=',', float_format='%.2f')

# Calcul flux net
fnet_data = fplus_data - fmoins_data
fnet = pd.DataFrame({"Country": pays, "fnet": fnet_data})
fnet = fnet.sort_values(by='fnet', ascending=False)
fnet.to_csv("generatedData/fnet.csv", sep=';', decimal=',', float_format='%.2f')


#Calcul des flux preference
# Calcul flux positifs preference Φ+
fplus_data_preference = matrice_promethee_preference.sum(axis=1)
fplus_preference = pd.DataFrame({"Country": pays, "fplus": fplus_data_preference})
fplus_preference = fplus_preference.sort_values(by='fplus', ascending=False)
fplus_preference.to_csv("generatedData/fplus_preference.csv", sep=';', decimal=',', float_format='%.2f')

# Calcul flux négatifs preference Φ-
fmoins_data_preference = matrice_promethee.sum(axis=0)
fmoins_preference = pd.DataFrame({"Country": pays, "fmoins": fmoins_data_preference})
fmoins_preference = fmoins_preference.sort_values(by='fmoins', ascending=True)
fmoins_preference.to_csv("generatedData/fmoins_preference.csv", sep=';', decimal=',', float_format='%.2f')

# Calcul flux net preference
fnet_data_preference = fplus_data_preference - fmoins_data_preference
fnet_preference = pd.DataFrame({"Country": pays, "fnet": fnet_data_preference})
fnet_preference = fnet_preference.sort_values(by='fnet', ascending=False)
fnet_preference.to_csv("generatedData/fnet_preference.csv", sep=';', decimal=',', float_format='%.2f')

print(fplus)
print(fmoins)
print(fnet)
print(fplus_preference)
print(fmoins_preference)
print(fnet_preference)