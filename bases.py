import affichage
import cycles
import copy

def completer_base_non_connexe(n, m, couts, base, transport):
    base_new = set(base)
    transport_new = copy.deepcopy(transport)

    connexe, composantes = cycles.est_connexe_bfs(n, m, base_new)
    if connexe:
        return base_new, transport_new

    print("\n  [Non connexe] Composantes connexes :")
    for k, comp in enumerate(composantes):
        desc = [f"P{u+1}" if u < n else f"C{u-n+1}" for u in comp]
        print(f"    Composante {k+1} : {', '.join(desc)}")

    while not connexe:
        # Recalculer les candidats à chaque itération pour exclure les arêtes déjà ajoutées et éviter la boucle infinie
        candidates = sorted(
            [(couts[i][j], i, j) for i in range(n) for j in range(m)
             if (i, j) not in base_new],
            key=lambda x: x[0]
        )

        ajout_effectue = False
        for cout, i, j in candidates:
            # Ajouter (i,j) uniquement si cela ne crée pas de cycle
            base_test = base_new | {(i, j)}
            a_cycle, _ = cycles.detecter_cycle_bfs(n, m, base_test)
            if not a_cycle:
                print(f"  -> Ajout de l'arête fictive ({i+1},{j+1}) [coût={cout}] pour connexité")
                base_new = base_test
                transport_new[i][j] = 0
                ajout_effectue = True
                break

        if not ajout_effectue:
            # Aucune arête ne peut être ajoutée sans cycle : on sort pour éviter une boucle infinie (ne devrait pas arriver sur un problème valide)
            print("  [Avertissement] Impossible de rendre le graphe connexe sans créer de cycle.")
            break

        connexe, composantes = cycles.est_connexe_bfs(n, m, base_new)

    return base_new, transport_new


def normaliser_base(n, m, couts, transport):
    base = {(i, j) for i in range(n) for j in range(m) if transport[i][j] > 0}

    # 1. Supprimer les cycles
    nb_iter = 0
    while True:
        a_cycle, cycle = cycles.detecter_cycle_bfs(n, m, base)
        if not a_cycle:
            break
        print(f"\n  [Normalisation] Cycle détecté, maximisation...")
        affichage.afficher_cycle(cycle, n)
        cases_cycle = []
        for k in range(len(cycle)):
            u = cycle[k]
            v = cycle[(k + 1) % len(cycle)]
            if u < n and v >= n:
                cases_cycle.append((u, v - n))
            elif v < n and u >= n:
                cases_cycle.append((v, u - n))

        signes = ['+' if k % 2 == 0 else '-' for k in range(len(cases_cycle))]
        cases_moins = [(c, transport[c[0]][c[1]]) for c, s in zip(cases_cycle, signes) if s == '-']
        if not cases_moins:
            break
        delta = min(v for _, v in cases_moins)
        for case, signe in zip(cases_cycle, signes):
            i, j = case
            if signe == '+':
                transport[i][j] += delta
            else:
                transport[i][j] -= delta
                if transport[i][j] == 0:
                    base.discard(case)

        nb_iter += 1
        if nb_iter > 100:
            break

    # 2. Assurer la connexité
    base, transport = completer_base_non_connexe(n, m, couts, base, transport)

    # 3. Vérification : taille de la base = n + m - 1
    taille_attendue = n + m - 1
    if len(base) < taille_attendue:
        print(f"  [Dégénérescence] Base de taille {len(base)} < {taille_attendue} attendue.")
        candidates = sorted(
            [(couts[i][j], i, j) for i in range(n) for j in range(m)
             if (i, j) not in base],
            key=lambda x: x[0]
        )
        for cout, i, j in candidates:
            if len(base) >= taille_attendue:
                break
            base_test = base | {(i, j)}
            a_cycle, _ = cycles.detecter_cycle_bfs(n, m, base_test)  # corrigé : cycles. et non cycle.
            if not a_cycle:
                print(f"  -> Ajout fictif ({i+1},{j+1}) [coût={cout}] pour dégénérescence")
                base = base_test
                transport[i][j] = 0

    return base, transport
