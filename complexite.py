import NordWest
import BalasHammer
import marche_pieds

import sys
import os
import time
import random

def generer_probleme_aleatoire(n):
    couts = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    temp = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    provisions = [sum(temp[i]) for i in range(n)]
    commandes = [sum(temp[i][j] for i in range(n)) for j in range(n)]
    return couts, provisions, commandes


def mesurer_complexite():
    valeurs_n = [10, 40, 100, 400]  # Réduit pour la démonstration (ajouter 1000, 4000, 10000 si besoin)
    nb_repetitions = 100

    resultats = {
        'n': [], 'theta_NO': [], 'theta_BH': [], 't_NO': [], 't_BH': []
    }

    print("\n" + "=" * 60)
    print("  ÉTUDE DE COMPLEXITÉ")
    print("=" * 60)

    for n in valeurs_n:
        print(f"\n  n = {n} ({nb_repetitions} répétitions)...")
        theta_NO_list, theta_BH_list = [], []
        t_NO_list, t_BH_list = [], []

        for rep in range(nb_repetitions):
            couts, provisions, commandes = generer_probleme_aleatoire(n)

            # Nord-Ouest
            t0 = time.process_time()
            # Rediriger la sortie pour éviter l'affichage
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            transport_NO = NordWest.nord_ouest(n, n, provisions, commandes)
            sys.stdout.close()
            sys.stdout = old_stdout
            theta_NO_list.append(time.process_time() - t0)

            # Balas-Hammer
            t0 = time.process_time()
            sys.stdout = open(os.devnull, 'w')
            transport_BH = BalasHammer.balas_hammer(n, n, couts, provisions, commandes)
            sys.stdout.close()
            sys.stdout = old_stdout
            theta_BH_list.append(time.process_time() - t0)

            # Marche-pied depuis NO
            t0 = time.process_time()
            sys.stdout = open(os.devnull, 'w')
            try:
                marche_pieds.marche_pied(n, n, couts, provisions, commandes, transport_NO)
            except Exception:
                pass
            sys.stdout.close()
            sys.stdout = old_stdout
            t_NO_list.append(time.process_time() - t0)

            # Marche-pied depuis BH
            t0 = time.process_time()
            sys.stdout = open(os.devnull, 'w')
            try:
                marche_pieds.marche_pied(n, n, couts, provisions, commandes, transport_BH)
            except Exception:
                pass
            sys.stdout.close()
            sys.stdout = old_stdout
            t_BH_list.append(time.process_time() - t0)

        resultats['n'].append(n)
        resultats['theta_NO'].append(theta_NO_list)
        resultats['theta_BH'].append(theta_BH_list)
        resultats['t_NO'].append(t_NO_list)
        resultats['t_BH'].append(t_BH_list)

        print(f"    θ_NO max = {max(theta_NO_list):.4f}s  "
              f"θ_BH max = {max(theta_BH_list):.4f}s  "
              f"t_NO max = {max(t_NO_list):.4f}s  "
              f"t_BH max = {max(t_BH_list):.4f}s")

    return resultats