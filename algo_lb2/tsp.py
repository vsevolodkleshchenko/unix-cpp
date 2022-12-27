import networkx as nx
import matplotlib.pyplot as plt
import scipy.spatial.distance as ssd
import numpy as np


def dp_tcp(dsts_table):
    n = len(dsts_table)
    t = [[float("inf")] * (1 << n) for _ in range(n)]
    t[0][1] = 0
    for s in range(1 << n):
        if sum(((s >> j) & 1) for j in range(n)) <= 1 or not (s & 1):
            continue
        for i in range(1, n):
            if not ((s >> i) & 1):
                continue
            for j in range(n):
                if j == i or not ((s >> j) & 1):
                    continue
                t[i][s] = min(t[i][s], t[j][s ^ (1 << i)] + dsts_table[i][j])
    result = min(t[i][(1 << n) - 1] + dsts_table[0][i] for i in range(1, n))

    s, p = (1 << n) - 1, 0
    path = [0]
    for i in range(1, n):
        if p == i or not ((s >> i) & 1):
            continue
        if t[i][s] + dsts_table[p][i] == result:
            p = i
            path.append(p)
            break
    while s ^ (1 << p) != 1:
        for i in range(1, n):
            if p == i or not ((s >> i) & 1) or not ((s >> p) & 1):
                continue
            if t[i][s ^ (1 << p)] + dsts_table[p][i] == t[p][s]:
                s, p = s ^ (1 << p), i
                path.append(p)
                break
    path.append(0)
    return path, result


def build_distances_table(pts):
    table = np.zeros((len(pts), len(pts)))
    for i in range(len(pts)):
        for j in range(len(points)):
            table[i][j] = ssd.pdist([pts[i], pts[j]])
    return table


def build_graph(pts, nms=None):
    graph = nx.Graph()
    for i in range(len(pts)):
        graph.add_node(i, pos=pts[i])
        if nms:
            graph.nodes[i]['name'] = nms[i]
    return graph


def draw_result_graph(graph, path, pts):
    for i in range(len(path)-1):
        graph.add_edge(path[i], path[i+1])
    nx.draw(graph, pts, with_labels=True)
    plt.show()


if __name__ == '__main__':
    points = [(1, 2), (3, -2), (5, 1), (-3, 4), (-4, -1), (1, -3), (-0.5, 0)]
    # names = ['sch', 'spb', 'msk', 'nov', 'ekb', 'kzn']

    tbl = build_distances_table(points)
    grf = build_graph(points)

    pth, pth_length = dp_tcp(tbl)
    print(pth, pth_length)

    draw_result_graph(grf, pth, points)


# points = [(1, 2), (3, -2), (5, 1), (-2.5, 2), (-3, -2.5), (-2.1, 0), (3, 5),
#           (0.1, 0.7), (-0.3, 2), (-0.4, -1.5), (-3, 4), (-4, -1), (1, -3)]
