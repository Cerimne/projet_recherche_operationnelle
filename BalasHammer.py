def calculer_penalites(n, m, couts, lignes_actives, cols_actives):
    pen_lignes = []
    for i in range(n):
        if i not in lignes_actives:
            pen_lignes.append(None)
            continue
        vals = sorted([couts[i][j] for j in cols_actives])
        if len(vals) >= 2:
            pen_lignes.append(vals[1] - vals[0])
        elif len(vals) == 1:
            pen_lignes.append(vals[0])
        else:
            pen_lignes.append(None)

    pen_cols = []
    for j in range(m):
        if j not in cols_actives:
            pen_cols.append(None)
            continue
        vals = sorted([couts[i][j] for i in lignes_actives])
        if len(vals) >= 2:
            pen_cols.append(vals[1] - vals[0])
        elif len(vals) == 1:
            pen_cols.append(vals[0])
        else:
            pen_cols.append(None)

    return pen_lignes, pen_cols


def balas_hammer(n, m, couts, provisions, commandes):
    print("\n" + "=" * 50)
    print("  ALGORITHME BALAS-HAMMER")
    print("=" * 50)

    transport = [[0] * m for _ in range(n)]
    prov = provisions[:]
    comm = commandes[:]
    lignes_actives = set(range(n))
    cols_actives = set(range(m))
    etape = 1

    while lignes_actives and cols_actives:
        pen_lignes, pen_cols = calculer_penalites(n, m, couts, lignes_actives, cols_actives)

        print(f"\n  --- Étape {etape} ---")
        # Affichage des pénalités
        print("  Pénalités lignes : ", end="")
        for i in range(n):
            if pen_lignes[i] is not None:
                print(f"P{i+1}={pen_lignes[i]}", end="  ")
        print()
        print("  Pénalités colonnes : ", end="")
        for j in range(m):
            if pen_cols[j] is not None:
                print(f"C{j+1}={pen_cols[j]}", end="  ")
        print()

        # Trouver la pénalité maximale
        max_pen = -1
        max_type = None  # 'ligne' ou 'col'
        max_idx = -1

        for i in range(n):
            if pen_lignes[i] is not None and pen_lignes[i] > max_pen:
                max_pen = pen_lignes[i]
                max_type = 'ligne'
                max_idx = i

        for j in range(m):
            if pen_cols[j] is not None and pen_cols[j] > max_pen:
                max_pen = pen_cols[j]
                max_type = 'col'
                max_idx = j

        if max_type is None:
            break

        # Affichage de la ligne/colonne de pénalité maximale
        if max_type == 'ligne':
            print(f"  => Pénalité max = {max_pen} sur la ligne P{max_idx+1}")
            # Trouver le coût minimal sur cette ligne parmi les colonnes actives
            min_cout = float('inf')
            best_j = -1
            for j in cols_actives:
                if couts[max_idx][j] < min_cout:
                    min_cout = couts[max_idx][j]
                    best_j = j
            i, j = max_idx, best_j
        else:
            print(f"  => Pénalité max = {max_pen} sur la colonne C{max_idx+1}")
            # Trouver le coût minimal sur cette colonne parmi les lignes actives
            min_cout = float('inf')
            best_i = -1
            for i in lignes_actives:
                if couts[i][max_idx] < min_cout:
                    min_cout = couts[i][max_idx]
                    best_i = i
            i, j = best_i, max_idx

        # Affectation
        quantite = min(prov[i], comm[j])
        transport[i][j] = quantite
        print(f"  -> Affectation ({i+1},{j+1}) = {quantite}  "
              f"(coût unitaire={couts[i][j]}, "
              f"reste P{i+1}={prov[i]-quantite}, C{j+1}={comm[j]-quantite})")
        prov[i] -= quantite
        comm[j] -= quantite

        if prov[i] == 0 and comm[j] == 0:
            # Dégénérescence : on retire la ligne (convention)
            lignes_actives.discard(i)
        elif prov[i] == 0:
            lignes_actives.discard(i)
        else:
            cols_actives.discard(j)

        etape += 1

    return transport