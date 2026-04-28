import read
import couttotal
import NordWest
import BalasHammer
import affichage
import marche_pieds
import complexite
import generer_traces



def menu_choix_algo():
    print("\n  Choisissez l'algorithme pour la proposition initiale :")
    print("  1. Nord-Ouest (NO)")
    print("  2. Balas-Hammer (BH)")
    return input("  Votre choix : ").strip()


def resoudre_probleme(nom_fichier, num=None):
    print(f"\n{'#' * 70}")
    print(f"  Fichier : {nom_fichier}")
    print(f"{'#' * 70}")

    #Gestion erreurs
    try:
        n, m, couts, provisions, commandes = read.read_pb(nom_fichier)
    except FileNotFoundError:
        print(f"Erreur fichier '{nom_fichier}' introuvable.")
        return
    except Exception as e:
        print(f"Erreur, impossible de lire le fichier : {e}")
        return

    # Vérification équilibre
    if sum(provisions) != sum(commandes):
        print(f"Erreur, problème déséquilibré : "
              f"sum(P)={sum(provisions)} est différent de sum(C)={sum(commandes)}")
        return

    affichage.afficher_matrice_couts(n, m, couts, provisions, commandes)

    choix = menu_choix_algo()

    # Choix algorithme
    if choix == '1':
        transport_init = NordWest.nord_ouest(n, m, provisions, commandes)
        nom_algo = "no"
    else:
        transport_init = BalasHammer.balas_hammer(n, m, couts, provisions, commandes)
        nom_algo = "bh"

    cout_init = couttotal.calculer_cout(n, m, couts, transport_init)

    affichage.afficher_proposition(
        n, m, transport_init, provisions, commandes,
        f"PROPOSITION INITIALE ({nom_algo})"
    )

    print(f"\n  Coût initial : {cout_init}")
    



def main():
    print("\n" + "=" * 70)
    print("  Résolution de problèmes de transport")
    print("=" * 70)

    continuer = True
    while continuer:
        print("\n  MENU PRINCIPAL")
        print("  1. Résoudre un problème de transport (fichier .txt)")
        print("  2. Résoudre un problème numéroté (1-12)")
        print("  3. Étude de complexité")
        print("  4. Générer les fichiers sorties des problèmes 1-12")
        print("  5. Quitter")

        choix = input("\n  Votre choix : ").strip()

        if choix == '1':
            nom = input("  Nom du fichier .txt : ").strip()
            nom = "problemes/" + nom
            resoudre_probleme(nom, None)

        elif choix == '2':
            num = input("  Numéro du problème (1-12) : ").strip()
            nom = f"probleme{num}"
            nom = "problemes/" + nom
            resoudre_probleme(nom, num)

        elif choix == '3':
            complexite.mesurer_complexite()

        elif choix == '4':
            generer_traces.generer_toutes_les_traces()

        elif choix == '5':
            continuer = False
            print("\nAu revoir !")

        else:
            print("Choix invalide.")

    return 0


if __name__ == "__main__":
    main()