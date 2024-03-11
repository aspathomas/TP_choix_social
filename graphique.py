import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import sys

electre = pd.read_csv("generatedData/matrice_electre_vi.csv", sep=';', decimal=',')
electre = electre.set_index(electre.columns[0]).rename_axis('Country')
G = nx.DiGraph()
pays = ["Serbia", "Bulgaria", "Macedonia", "Romania", "Greece", "Montenegro","Albania", "Bosnia", "Croatia", "Slovenia"]
G.add_nodes_from(pays)
print(len(pays))

surclassement = float(sys.argv[1])
for i_first in range(len(pays)):
    for i_second in range(len(pays)):
        if i_first == i_second:
            continue
        if (electre.iloc[i_first, i_second]) >= surclassement and electre.iloc[i_first, i_second] > electre.iloc[i_second, i_first]:
            G.add_edge(pays[i_first], pays[i_second])

in_degrees = G.in_degree()

# Déterminer la couleur de chaque nœud
node_colors = []
font_colors = []
for node in G.nodes():
    if in_degrees[node] == 0:
        node_colors.append('green')
        font_colors.append('white')
    elif 1 <= in_degrees[node] <= 5:
        node_colors.append('orange')
        font_colors.append('black')
    else:
        node_colors.append('red')
        font_colors.append('white')

# Dessiner le graphe
pos = nx.spring_layout(G, k=2)  # Position des nœuds
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='white', node_size=5000, edge_color='black', arrows=True)
plt.show()

