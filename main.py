import git
from graphviz import Graph
import itertools
def draw_dot_graph(nodes, edges):
    dot = Graph(name="MyPicture", comment="the test", format="svg")
    weighted_edges = {}
    for node in nodes:
        dot.node(name=node, label=node, color='blue')
    for e in edges:
        e.sort()
        for x in itertools.product(e, e):
            if x[0] != x[1] and x[0] < x[1]:
                if x[0] + "---" + x[1] not in weighted_edges:
                    weighted_edges[x[0] + "---" + x[1]] = 0
                weighted_edges[x[0] + "---" + x[1]] += 1
    for e, weight in weighted_edges.items():
        src, dst = e.split("---")
        dot.edge(src, dst, label=str(weight), color='red' if weight >= 20 else ("green" if weight < 5 else "purple"), width = '10' if weight > 10 else ('1' if weight < 5 else '5'))
    print(dot.source)
    dot.render(filename='res4.dot', directory=".")



nodes = set()
edges = []
with git.Repo.init(path='../ai_engine') as repo:
    commits = list(repo.iter_commits('master'))
    single_modify = []
    for c in commits:
        file_changes = c.stats.files
        print(file_changes)
        files = list('/'.join(x.split("/")[:4]) for x in file_changes.keys() if "test" not in x)
        if len(files) > 1 and len(files) < 40:
            single_modify.append(c)
            nodes = nodes | set(files)
            edges.append(files)
draw_dot_graph(nodes, edges)
print(len(commits))
print(len(single_modify))