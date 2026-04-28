import sys
import io
import os

import read
import couttotal
import NordWest
import BalasHammer
import affichage
import marche_pieds


def resoudre_et_capturer(nom_fichier, algo):
    buffer = io.StringIO()
    ancien_stdout = sys.stdout
    sys.stdout = buffer

    try:
        n, m, couts, provisions, commandes = read.read_pb(nom_fichier)

        print(f"{'#' * 70}")
        print(f"  Fichier : {nom_fichier}.txt")
        print(f"  Algorithme : {'Nord-Ouest (NO)' if algo == 'no' else 'Balas-Hammer (BH)'}")
        print(f"{'#' * 70}")

        # Vérification équilibre
        if sum(provisions) != sum(commandes):
            print(f"  [Erreur] Problème déséquilibré : "
                  f"sum(P)={sum(provisions)} ≠ sum(C)={sum(commandes)}")
            return buffer.getvalue()

        affichage.afficher_matrice_couts(n, m, couts, provisions, commandes)

        # Proposition initiale
        if algo == 'no':
            transport_init = NordWest.nord_ouest(n, m, provisions[:], commandes[:])
        else:
            transport_init = BalasHammer.balas_hammer(n, m, couts, provisions[:], commandes[:])

        cout_init = couttotal.calculer_cout(n, m, couts, transport_init)

        nom_algo_display = "NORD-OUEST (NO)" if algo == 'no' else "BALAS-HAMMER (BH)"
        affichage.afficher_proposition(
            n, m, transport_init, provisions, commandes,
            f"PROPOSITION INITIALE — {nom_algo_display}"
        )
        print(f"\n  Coût initial : {cout_init}")

        # Marche-pied avec potentiels
        marche_pieds.marche_pied(
            n, m, couts, provisions, commandes, transport_init, algo.upper()
        )

    except FileNotFoundError:
        print(f"  [Erreur] Fichier '{nom_fichier}.txt' introuvable.")
    except Exception as e:
        print(f"  [Erreur] {e}")
    finally:
        sys.stdout = ancien_stdout

    return buffer.getvalue()


def generer_toutes_les_traces(nb_problemes=12, dossier_sortie="traces"):
    os.makedirs(dossier_sortie, exist_ok=True)

    print(f"Génération des traces — {nb_problemes} problèmes × 2 algorithmes")
    print("=" * 60)

    for num in range(1, nb_problemes + 1):
        nom_fichier = f"probleme{num}"

        for algo in ("no", "bh"):
            nom_sortie = os.path.join(dossier_sortie, f"1-x-trace{num}-{algo}.txt")

            print(f"  [{num:02d}/{nb_problemes}] {nom_fichier}.txt  algo={algo.upper()} ...", end=" ")

            trace = resoudre_et_capturer("problemes/" + nom_fichier, algo)

            with open(nom_sortie, "w", encoding="utf-8") as f:
                f.write(trace)

            print(f"-> {nom_sortie}")

    print("=" * 60)
    print(f"Terminé. {nb_problemes * 2} fichiers générés dans '{dossier_sortie}'.")


if __name__ == "__main__":
    generer_toutes_les_traces(nb_problemes=12, dossier_sortie="traces")
