def construire_graphe(n, m, transport):
    adj = [[] for _ in range(n + m)]
    aretes = []
    for i in range(n):
        for j in range(m):
            if transport[i][j] > 0:
                adj[i].append(n + j)
                adj[n + j].append(i)
                aretes.append((i, j))
    return adj, aretes


def construire_graphe_avec_zeros_base(n, m, transport, base):
    adj = [[] for _ in range(n + m)]
    for (i, j) in base:
        adj[i].append(n + j)
        adj[n + j].append(i)
    return adj