from collections import defaultdict
from pathlib import Path

# Classe para implementação de um grafo que será populado a partir do arquivo soc-dolphins.txt
class Grafo(object):
    def __init__(self, elos): 
        self.arestas = defaultdict(set) #Utilizando defaultDict para sobrescrita
        self.set_arestas(elos)

    def get_elos(self):# Recuperando uma lista de elos
        return [(k, v) for k in self.arestas.keys() for v in self.arestas[k]]

    def set_arestas(self, elos): # Referenciando todos os elos para cada aresta possível
        for u, v in elos:
            self.arestas[v].add(u)
            self.arestas[u].add(v)


# Montando Grafo a partir do arquivo
def CriarGrafo():
    elos = []
    with open('soc-dolphins.txt') as arq:
        for line in arq:
            item = [int(i) for i in line.split()]
            elos.append((item[0], item[1]))

    # print(elos)

    graph = Grafo(elos)
    return (graph.get_elos())

print(CriarGrafo())