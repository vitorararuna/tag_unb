"""
Projeto 1 - TEORIA E APLICAÇÃO DE GRAFOS - UNB
Vitor Araruna - 202060980

Explicação para os algoritmos BRON-KERBOSCH realizados:

Sem Pivo (BK_sem_pivo):
O algoritmo BRON-KERBOSCH é responsável por gerar cliques maximais em quaisquer tipo de grafo, apesar de não 
achar todos. Ele funciona da seguinte maneira: Inicializa com 3 conjuntos distintos de vértices que são os 
conjuntos R, P e X. O conjunto P guarda os vértices que têm ligação com todos os vértices de R (candidatos), este que 
inicia vazio. Já o conjunto X contém vértices já analisados e que nao levam a uma extensão do conjunto R. Ou seja, é usado para
evitar comparação excessiva (também inicia vazio). Logo, na chamada inicial, apenas P não é vazio e contém todos os vértices do grafo.
Em cada chamada recursiva da função, se P está vazio, um clique maximal é encontrado, caso X também esteja vazio. Ou seja , P_união_X 
seriam os vértices unidos a cada elemento de R. Caso P e X estejam vazios, não há mais elementos que possam ser adicionados a R , assim R é 
um clique máximo.

Com Pivo (BK_com_pivo):
O algoritmo BRON-KERBOSCH com pivotamento é visto como uma boa alternativa em casos de grafos com muitos cliques maximos, uma vez
que sem ele, nem todos os maximais são encontrados e chamadas recursivas são realizadas para cada clique, eja maximo ou não. A fim de 
gatar menos tempo em sua complexidade, esta função retrocede mais rápido nos ramos que não contém clique máximo, com o auxílio de um 
vértice pivô, escolhido de P.

"""


from collections import defaultdict
import random

# Classe para implementação de um grafo que será populado a partir do arquivo soc-dolphins.txt
class Grafo(object):
    def __init__(self, elos): 
        #Utilizando defaultDict para sobrescrita
        self.arestas = defaultdict(set) 
        self.set_arestas(elos)

    # Referenciando todos os elos para cada aresta possível
    def set_arestas(self, elos): 
        for a, b in elos:
            self.arestas[b].add(a)
            self.arestas[a].add(b)


# Montando Grafo a partir do arquivo
def CriarGrafo():
    elos = []
    with open('soc-dolphins.txt') as arq:
        for line in arq:
            item = [int(i) for i in line.split()]
            elos.append((item[0], item[1]))
    grafo = Grafo(elos)
    return (grafo.arestas)

def BK_sem_pivo(grafo, P_, R_=None, X_=None):
    R_ = set() if R_ is None else R_
    X_ = set() if X_ is None else X_
    P_ = set(P_)

    if not P_ and not X_: yield R_ 
    while P_:
        v = P_.pop()
        yield from BK_sem_pivo(
            grafo=grafo ,P_=P_.intersection(grafo[v]), R_=R_.union([v]), X_=X_.intersection(grafo[v]))
        X_.add(v)


def BK_com_pivo(grafo, P_, R_=None, X_=None):
    R_ = set() if R_ is None else R_
    X_ = set() if X_ is None else X_
    P_ = set(P_)

    if not P_ and not X_: yield R_
    try:
        #escolha do pivô aleatorianente
        piv = random.choice(list(P_.union(X_)))  
        S = P_.difference(grafo[piv])
    #caso piv não esteja na lista
    except IndexError:  
        S = P_
    for v in S:
        yield from BK_com_pivo(
            grafo=grafo, P_=P_.intersection(grafo[v]), R_=R_.union([v]), X_=X_.intersection(grafo[v]))
        P_.remove(v)
        X_.add(v)



# A função é responsavel por calcular o coeficiente de aglomeração do grafo
def aglomeracao(_grafo_):

    #verificação de elos existentes
    def conectos(no_1, no_2): 
        vizinhos = _grafo_.get(no_1, [])
        if no_2 in vizinhos: return True
        vizinhos = _grafo_.get(no_2, [])
        if no_2 in vizinhos: return True
        return False

    _retorno_ = {}
    
    #identificando coeficiente de cada vértice (caso nmr de vizinhos > 1 verifica cada um deles estão conectados, calculando o coeficiente)
    for node in _grafo_: 
        qtd_links = 0
        vizinhos = _grafo_[node]
        vizinhos_totais = len(vizinhos)

        if vizinhos_totais > 1:
            for no_1 in vizinhos:
                for no_2 in vizinhos:
                    if conectos(no_1, no_2):
                        qtd_links += 1

            qtd_links /= 2  #evitando duplicatas dividindo por 2
            _retorno_[node] = (2*qtd_links) / (vizinhos_totais*(vizinhos_totais-1))
        else:
            _retorno_[node] = 0

    #Calculando coeficiente geral pela fórmula padrão 1/(nmr de nós) * soma(coeficiente de agl. do atual nó)
    coeficiente = 0
    for i in _retorno_: coeficiente += _retorno_[i]
    coeficiente = (1 / 62) * coeficiente
    return coeficiente

"""
**********************************************************************************
*******EXECUTE O PROGRAMA PARA QUE OS PRÓXIMOS PASSOS SEJAM INTERPRETADOS*********
**********************************************************************************
"""

grafo = CriarGrafo()
vertices = grafo.keys()  

print("*******************************************************************")
print("                   BRON-KERBOSCK SEM PIVOTAMENTO                   ")
print("*******************************************************************")
print(f'CLIQUES MAXIMAIS ENCONTRADOS: {len(list(BK_sem_pivo(grafo=grafo, P_= vertices)))}')
print("*******************************************************************")
print(f'CLIQUES MAXIMAIS: {list(BK_sem_pivo(grafo=grafo, P_= vertices))}')

print("\n")

print("*******************************************************************")
print("                   BRON-KERBOSCK COM PIVOTAMENTO                   ")
print("*******************************************************************")
print(f'CLIQUES MAXIMAIS ENCONTRADOS: {len(list(BK_com_pivo(grafo=grafo, P_= vertices)))}')
print("*******************************************************************")
print(f'CLIQUES MAXIMAIS: {list(BK_com_pivo(grafo=grafo, P_= vertices))}')

print("\n")


print("*******************************************************************")
print(f'COEFICIENTE DE AGLOMERAÇÃO: {aglomeracao(grafo)}') 
