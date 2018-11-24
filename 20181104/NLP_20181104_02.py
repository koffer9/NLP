import networkx
import matplotlib.pyplot as plt


# 定义无向图
graph = {
    'A' :'B B B C',
    'B' : 'A D',
    'C' : 'A E',
    'D' : 'F',
    'E' : 'G',
    'F' : 'D',
    'G' : 'E'
}


for k in graph:
    graph[k] = set(graph[k].split())
print(graph)
Graph = networkx.Graph(graph)
networkx.draw(Graph, with_labels=True)


def search(graph):
    been=set()
    next=['A']
    while next:
        p=next.pop(0)
        if p in been:
            # print('I have been to {}'.format(p))
            continue
        else:
            print('I arrived {} now'.format(p))
            been.add(p)
            #next = list(graph[p]) + next # deep search
            next = next + list(graph[p]) # deep search
            # print(next)


search(graph)
