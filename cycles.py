
import copy
from collections import deque


def detecter_cycle_bfs(n, m, base):
    adj = [[] for _ in range(n + m)]
    # On stocke aussi les arêtes pour retrouver le cycle
    edges_set = set()
    for (i, j) in base:
        adj[i].append(n + j)
        adj[n + j].append(i)
        edges_set.add((i, n + j))
        edges_set.add((n + j, i))

    visité = [-1] * (n + m)
    parent = [-1] * (n + m)

    for source in range(n + m):
        if visité[source] != -1:
            continue
        file = deque([source])
        visité[source] = source
        parent[source] = -1

        while file:
            u = file.popleft()
            for v in adj[u]:
                if visité[v] == -1:
                    visité[v] = source
                    parent[v] = u
                    file.append(v)
                elif v != parent[u]:
                    # Cycle détecté ! Reconstituer le cycle
                    cycle = _reconstituer_cycle(u, v, parent)
                    return True, cycle

    return False, []


def _reconstituer_cycle(u, v, parent):
    # Remonter depuis u et v jusqu'à leur ancêtre commun
    chemin_u = []
    chemin_v = []
    cu, cv = u, v
    visited_u = {}
    visited_v = {}

    node = cu
    while node != -1:
        visited_u[node] = len(chemin_u)
        chemin_u.append(node)
        node = parent[node]

    node = cv
    while node != -1:
        if node in visited_u:
            # Trouver le LCA
            lca = node
            idx_u = visited_u[lca]
            cycle = chemin_u[:idx_u + 1] + list(reversed(chemin_v))
            return cycle
        visited_v[node] = len(chemin_v)
        chemin_v.append(node)
        node = parent[node]

    return chemin_u + list(reversed(chemin_v))


def afficher_cycle(cycle, n):
    desc = []
    for noeud in cycle:
        if noeud < n:
            desc.append(f"P{noeud+1}")
        else:
            desc.append(f"C{noeud-n+1}")
    print(f"  Cycle détecté : {' -> '.join(desc)} -> {desc[0]}")



def est_connexe_bfs(n, m, base):
    adj = [[] for _ in range(n + m)]

    for (i, j) in base:
        adj[i].append(n + j)
        adj[n + j].append(i)

    visite = [False] * (n + m)
    composantes = []

    for s in range(n + m):
        if visite[s]:
            continue

        file = deque([s])
        visite[s] = True
        comp = []

        while file:
            u = file.popleft()
            comp.append(u)
            for v in adj[u]:
                if not visite[v]:
                    visite[v] = True
                    file.append(v)

        composantes.append(comp)

    return len(composantes) == 1, composantes

def extraire_cases_cycle(cycle, n):
    cases = []
    for k in range(len(cycle) - 1):
        u = cycle[k]
        v = cycle[k + 1]
        if u < n:
            cases.append((u, v - n))
        else:
            cases.append((v, u - n))
    # Fermer le cycle
    u = cycle[-1]
    v = cycle[0]
    if u < n:
        cases.append((u, v - n))
    else:
        cases.append((v, u - n))
    return cases


def maximiser_sur_cycle(n, m, transport, cycle, arête_entrante):

    cases_cycle = []
    for k in range(len(cycle)):
        u = cycle[k]
        v = cycle[(k + 1) % len(cycle)]
        if u < n and v >= n:
            cases_cycle.append((u, v - n))
        elif v < n and u >= n:
            cases_cycle.append((v, u - n))

    # Trouver la position de arête_entrante dans le cycle
    idx_entree = None
    for k, case in enumerate(cases_cycle):
        if case == arête_entrante:
            idx_entree = k
            break

    if idx_entree is None:
        print("  [Erreur] Arête entrante non trouvée dans le cycle.")
        return transport, []

    signes = []
    for k in range(len(cases_cycle)):
        if (k - idx_entree) % 2 == 0:
            signes.append('+')
        else:
            signes.append('-')

    print("\n  CONDITIONS DU CYCLE :")
    for k, (case, signe) in enumerate(zip(cases_cycle, signes)):
        i, j = case
        print(f"    ({i+1},{j+1}) : {signe}  [transport actuel = {transport[i][j]}]")

    # δ = minimum sur les cases de signe '-'
    cases_moins = [(case, transport[case[0]][case[1]])
                   for case, s in zip(cases_cycle, signes) if s == '-']
    delta = min(val for _, val in cases_moins)
    print(f"\n  δ = {delta}")

    if delta == 0:
        print("  [Cas dégénéré] δ = 0 → suppression d'une arête artificielle")

        # supprimer une arête '-' avec 0
        for case, signe in zip(cases_cycle, signes):
            i, j = case
            if signe == '-' and transport[i][j] == 0:
                return transport, [case]

    # Application
    transport_new = copy.deepcopy(transport)
    for case, signe in zip(cases_cycle, signes):
        i, j = case
        if signe == '+':
            transport_new[i][j] += delta
        else:
            transport_new[i][j] -= delta

    # Cases supprimées (transport = 0 après soustraction, signe '-', hors arête_entrante)
    supprimées = []
    for case, signe in zip(cases_cycle, signes):
        i, j = case
        if signe == '-' and transport_new[i][j] == 0:
            supprimées.append(case)

    print(f"  Arête(s) supprimée(s) : {[(i+1,j+1) for i,j in supprimées]}")
    return transport_new, supprimées