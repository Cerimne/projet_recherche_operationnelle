def afficher_matrice_couts(n, m, couts, provisions, commandes):
    col_w = 8

    print("\n" + "=" * (col_w * (m + 2) + 4))
    print("  MATRICE DES COÛTS")
    print("=" * (col_w * (m + 2) + 4))

    # En-tête
    header = " " * col_w
    for j in range(m):
        header += f"{'C' + str(j+1):^{col_w}}"
    header += f"{'Provis.':^{col_w}}"
    print(header)
    print("-" * (col_w * (m + 2)))

    for i in range(n):
        ligne = f"{'P' + str(i+1):<{col_w}}"
        for j in range(m):
            ligne += f"{couts[i][j]:^{col_w}}"
        ligne += f"{provisions[i]:^{col_w}}"
        print(ligne)

    print("-" * (col_w * (m + 2)))
    footer = f"{'Comm.':^{col_w}}"
    for j in range(m):
        footer += f"{commandes[j]:^{col_w}}"
    print(footer)
    print("=" * (col_w * (m + 2) + 4))


def afficher_proposition(n, m, transport, provisions, commandes, titre="PROPOSITION DE TRANSPORT"):
    col_w = 8

    print("\n" + "=" * (col_w * (m + 2) + 4))
    print(f"  {titre}")
    print("=" * (col_w * (m + 2) + 4))

    header = " " * col_w
    for j in range(m):
        header += f"{'C' + str(j+1):^{col_w}}"
    header += f"{'Provis.':^{col_w}}"
    print(header)
    print("-" * (col_w * (m + 2)))

    for i in range(n):
        ligne = f"{'P' + str(i+1):<{col_w}}"
        for j in range(m):
            v = transport[i][j]
            ligne += f"{v if v != 0 else '-':^{col_w}}"
        ligne += f"{provisions[i]:^{col_w}}"
        print(ligne)

    print("-" * (col_w * (m + 2)))
    footer = f"{'Comm.':^{col_w}}"
    for j in range(m):
        footer += f"{commandes[j]:^{col_w}}"
    print(footer)
    print("=" * (col_w * (m + 2) + 4))


def afficher_potentiels(n, m, ui, vj):
    col_w = 8
    print("\n  POTENTIELS :")
    ligne_u = "  ui : "
    for i in range(n):
        ligne_u += f"u{i+1}={ui[i] if ui[i] is not None else '?':<{col_w-3}}"
    print(ligne_u)
    ligne_v = "  vj : "
    for j in range(m):
        ligne_v += f"v{j+1}={vj[j] if vj[j] is not None else '?':<{col_w-3}}"
    print(ligne_v)


def afficher_table_potentiels(n, m, couts, ui, vj):
    col_w = 8
    print("\n" + "=" * (col_w * (m + 2) + 4))
    print("  TABLE DES COÛTS POTENTIELS (ui + vj)")
    print("=" * (col_w * (m + 2) + 4))

    header = " " * col_w
    for j in range(m):
        header += f"{'C' + str(j+1):^{col_w}}"
    print(header)
    print("-" * (col_w * (m + 1)))

    for i in range(n):
        ligne = f"{'P' + str(i+1):<{col_w}}"
        for j in range(m):
            if ui[i] is not None and vj[j] is not None:
                val = ui[i] + vj[j]
                ligne += f"{val:^{col_w}}"
            else:
                ligne += f"{'?':^{col_w}}"
        print(ligne)
    print("=" * (col_w * (m + 2) + 4))


def afficher_table_marginaux(n, m, couts, ui, vj, transport):
    col_w = 8
    print("\n" + "=" * (col_w * (m + 2) + 4))
    print("  TABLE DES COÛTS MARGINAUX (cij - ui - vj) [cases vides]")
    print("=" * (col_w * (m + 2) + 4))

    header = " " * col_w
    for j in range(m):
        header += f"{'C' + str(j+1):^{col_w}}"
    print(header)
    print("-" * (col_w * (m + 1)))

    best_i, best_j, best_val = -1, -1, 0

    for i in range(n):
        ligne = f"{'P' + str(i+1):<{col_w}}"
        for j in range(m):
            if transport[i][j] == 0:  # case vide (hors base)
                if ui[i] is not None and vj[j] is not None:
                    marginal = couts[i][j] - ui[i] - vj[j]
                    ligne += f"{marginal:^{col_w}}"
                    if marginal < best_val:
                        best_val = marginal
                        best_i, best_j = i, j
                else:
                    ligne += f"{'?':^{col_w}}"
            else:
                ligne += f"{'[base]':^{col_w}}"
        print(ligne)
    print("=" * (col_w * (m + 2) + 4))

    return best_i, best_j, best_val