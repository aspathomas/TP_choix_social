import pandas as pd
import numpy as np
pays = ["Serbia", "Bulgaria", "Macedonia", "Romania", "Greece", "Montenegro","Albania", "B&H", "Croatia", "Slovenia"]
critere = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"]
donnees = pd.read_csv("donnees.csv", header=None)
poids = pd.read_csv("poids.csv", header=None)

matrice = np.zeros((len(pays), len(pays))) 
for i_first in range(len(pays)):
    for i_second in range(len(pays)):
        if i_first == i_second:
            matrice[i_first][i_second] = -1
            continue
        
        score = 0
        for j in range(len(critere)):
            if donnees.iloc[j, i_first] > donnees.iloc[j, i_second]:
                score += poids[j]
        matrice[i_first][i_second] = score
            
print(matrice)