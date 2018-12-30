#https://blog.csdn.net/quiet_girl/article/details/81227904
import networkx as nx
import random
from string import ascii_letters
from matplotlib import pyplot as plt
def generate_name(): return ''.join([random.choice(ascii_letters.upper()) for _ in range(3)])
print(generate_name())

social_graph = {
    "Yao": ['Guo', 'Wang', 'Tian', 'Tim'] + [generate_name() for _ in range(4)],
    "Guo": ['Li'] + [generate_name() for _ in range(5)],
    "Wang": ["Li_2"] + [generate_name() for _ in range(5)],
    "Li_2": [generate_name() for _ in range(5)],
    "Li": [generate_name() for _ in range(1)],
}

print(social_graph)
social_network = nx.graph.Graph(social_graph)
#%matplotlib inline
nx.draw_networkx(social_network)
sorted_id=sorted(nx.pagerank(social_network).items(), key=lambda x: x[1], reverse=True)
print(sorted_id)
plt.show()