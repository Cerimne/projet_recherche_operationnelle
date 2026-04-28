def nord_ouest(n, m, provisions, commandes):
    print("\n" + "=" * 50)
    print("  ALGORITHME NORD-OUEST")
    print("=" * 50)

    transport = [[0] * m for _ in range(n)]
    prov = provisions[:]
    comm = commandes[:]

    i, j = 0, 0
    while i < n and j < m:
        quantite = min(prov[i], comm[j])
        transport[i][j] = quantite
        print(f"  -> Affectation ({i+1},{j+1}) = {quantite}  "
              f"(reste P{i+1}={prov[i]-quantite}, C{j+1}={comm[j]-quantite})")
        prov[i] -= quantite
        comm[j] -= quantite

        if prov[i] == 0 and comm[j] == 0:
            # Ajouter une case fictive pour éviter la dégénérescence
            if j + 1 < m:
                transport[i][j + 1] = 0
            elif i + 1 < n:
                transport[i + 1][j] = 0
            i += 1
            j += 1
        elif prov[i] == 0:
            i += 1
        else:
            j += 1
            

    return transport