def calculer_potentiels(n, m, couts, base):
    ui = [None] * n
    vj = [None] * m
    ui[0] = 0

    # Construction de l'adjacence pour la base On propage tant qu'il y a des valeurs à calculer
    changed = True
    while changed:
        changed = False
        for (i, j) in base:
            if ui[i] is not None and vj[j] is None:
                vj[j] = couts[i][j] - ui[i]
                changed = True
            elif vj[j] is not None and ui[i] is None:
                ui[i] = couts[i][j] - vj[j]
                changed = True

    return ui, vj
