import couttotal
import affichage
import bases
import cycles
import potentiels

import copy

def marche_pied(n, m, couts, provisions, commandes, transport_initial, nom_algo=""):
    print("\n" + "=" * 60)
    print(f"  MÉTHODE DU MARCHE-PIED AVEC POTENTIELS [{nom_algo}]")
    print("=" * 60)

    transport = copy.deepcopy(transport_initial)
    iteration = 0

    historique = set()

    while True:
        iteration += 1

        print(f"\n{'=' * 60}")
        print(f"  ITÉRATION {iteration}")
        print(f"{'=' * 60}")


        etat = tuple(tuple(row) for row in transport)
        if etat in historique:
            print("  [Arrêt] Boucle détectée : solution déjà rencontrée.")
            break
        historique.add(etat)

        # Affichage
        cout_total = couttotal.calculer_cout(n, m, couts, transport)
        affichage.afficher_proposition(n, m, transport, provisions, commandes,
                             f"PROPOSITION (itération {iteration})")
        print(f"\n  Coût total : {cout_total}")

        # Normalisation
        base, transport = bases.normaliser_base(n, m, couts, transport)

        # Potentiels
        ui, vj = potentiels.calculer_potentiels(n, m, couts, base)
        affichage.afficher_potentiels(n, m, ui, vj)
        affichage.afficher_table_potentiels(n, m, couts, ui, vj)

        # Coûts marginaux
        best_i, best_j, best_val = affichage.afficher_table_marginaux(n, m, couts, ui, vj, transport)

        if best_val >= 0:
            print(f"\n  ✓ Solution optimale atteinte ! Coût = {cout_total}")
            break

        print(f"\n  Meilleure arête améliorante : ({best_i+1},{best_j+1}) "
              f"[coût marginal = {best_val}]")

        # Ajout arête
        transport[best_i][best_j] = 0
        base_test = base | {(best_i, best_j)}

        a_cycle, cycle = cycles.detecter_cycle_bfs(n, m, base_test)

        if not a_cycle:
            print("  [Erreur] Pas de cycle formé.")
            break

        cycles.afficher_cycle(cycle, n)

        # Maximisation
        transport, supprimées = cycles.maximiser_sur_cycle(n, m, transport, cycle, (best_i, best_j))

    cout_final = couttotal.calculer_cout(n, m, couts, transport)
    affichage.afficher_proposition(n, m, transport, provisions, commandes, "PROPOSITION OPTIMALE")
    print(f"\n  *** Coût optimal = {cout_final} ***")

    return transport, cout_final
