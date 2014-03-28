## generate a preferential attachment graph
import random
import networkx as nx

def choose(agents, G): ## G is a list of edges
    edge = [x for x in random.choice(G)]
    random.shuffle(edge)
    return [agents[edge[0]],agents[edge[1]]]

def Complete(n):
    graph = nx.complete_graph(n)
    return graph.edges()

def Barabasi(n):
    if n<=2:
        return Complete(n)
    graph = nx.barabasi_albert_graph(n,2)
    return graph.edges()

def Tree(n):
    graph = nx.barabasi_albert_graph(n,1)
    return graph.edges()

def Circle(n):
    graph = nx.cycle_graph(n)
    return graph.edges()

def Path(n):
    graph = nx.path_graph(n)
    return graph.edges()
