import matplotlib.pyplot as plt
import networkx as nx
from collections import deque, defaultdict

graphs = {
    0: {
        'S': [('A', 4), ('B', 4), ('C', 1)],
        'A': [('D', 2), ('E', 4)],
        'B': [('A', 4), ('F', 4)],
        'C': [('F', 2)],
        'D': [('T', 2)],
        'E': [('T', 6)],
        'F': [('T', 5), ('E', 1)],
        'T': []
    },
    1: {
        'S': [('A', 4), ('B', 4), ('C', 2)],
        'A': [('D', 2), ('E', 4)],
        'B': [('A', 4), ('F', 4)],
        'C': [('F', 2), ('E', 3)],
        'D': [('T', 2)],
        'E': [('T', 6)],
        'F': [('T', 5), ('E', 1)],
        'T': []
    },
    2: {
        'S': [('A', 4), ('B', 4)],
        'A': [('D', 2)],
        'B': [('F', 4)],
        'D': [('T', 2)],
        'F': [('T', 5)],
        'T': []
    },
    3: {
        'S': [('A', 4), ('B', 4), ('C', 2)],
        'A': [('D', 2), ('E', 4)],
        'B': [('A', 4), ('F', 4)],
        'C': [('F', 2)],
        'D': [('T', 2)],
        'E': [('T', 6), ('F', 1), ('A', 1)],
        'F': [('T', 5)],
        'T': []
    },
    4: {
        'S': [('A', 4), ('B', 4), ('C', 2)],
        'A': [('D', 2), ('E', 4)],
        'B': [('A', 4), ('F', 4)],
        'C': [('F', 2)],
        'D': [('T', 2)],
        'E': [('T', 6)],
        'F': [('G', 5), ('E', 1)],
        'G': [('T', 5)],
        'T': []
    },

    5: {
        'S': [('A', 10), ('B', 8)],
        'A': [('C', 5), ('D', 4)],
        'B': [('D', 7), ('E', 6)],
        'C': [('F', 6)],
        'D': [('F', 3), ('G', 4)],
        'E': [('G', 8)],
        'F': [('H', 5)],
        'G': [('H', 4), ('I', 6)],
        'H': [('T', 9)],
        'I': [('T', 5)],
        'T': []
    }
}

graph_number = 0
graph = graphs[graph_number]


def bfs_with_path(capacity, flow, source, sink, parent):
    visited = set()
    queue = deque([(source, [])])
    visited.add(source)
    while queue:
        u, path = queue.popleft()
        for v in capacity[u]:
            if v not in visited and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited.add(v)
                if v == sink:
                    return path + [(u, v)]
                queue.append((v, path + [(u, v)]))
    return None


def edmonds_karp_paths(graph, source, sink):
    capacity = defaultdict(lambda: defaultdict(int))
    flow = defaultdict(lambda: defaultdict(int))
    for u in graph:
        for v, cap in graph[u]:
            capacity[u][v] = cap
            capacity[v][u] = 0

    total_flow = 0
    all_paths = []

    while True:
        parent = {}
        path = bfs_with_path(capacity, flow, source, sink, parent)
        if not path:
            break
        path_flow = min(capacity[u][v] - flow[u][v] for u, v in path)
        for u, v in path:
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
        total_flow += path_flow
        all_paths.append((path, path_flow))

    return total_flow, flow, all_paths


max_flow, flow_result, flow_paths = edmonds_karp_paths(graph, 'S', 'T')

G = nx.DiGraph()
for u in graph:
    for v, cap in graph[u]:
        f = flow_result[u][v]
        G.add_edge(u, v, label=f'{f}/{cap}')

pos = nx.spring_layout(G, seed=42)
if 'G' in graph:
    pos['G'] = (pos['T'][0], pos['T'][1] - 0.4)

used_edges = set()
for path, _ in flow_paths:
    used_edges.update(path)

edge_colors = ['red' if (u, v) in used_edges else 'gray' for u, v in G.edges()]
edge_labels = nx.get_edge_attributes(G, 'label')

plt.figure(figsize=(12, 7))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000,
        font_size=12, font_weight='bold', arrowsize=20, edge_color=edge_colors, width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

plt.text(1.0, 0.97, f"Максимальный поток: {max_flow}", transform=plt.gca().transAxes,
         fontsize=14, fontweight='bold', ha='right', va='bottom', color='darkgreen')

plt.title(f"Граф #{graph_number}\nКрасные рёбра — задействованные в потоке", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()
