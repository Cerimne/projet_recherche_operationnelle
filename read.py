def read_pb(name):
    with open(name + ".txt", "r") as f:
        size = f.readline().split()

        nbRow = int(size[0])
        nbColumn = int(size[1])

        cost = []
        provision = []

        for i in range(nbRow):
            l = f.readline().split()
            provision.append(int(l[-1]))
            cost.append(list(map(int, l[:nbColumn])))

        commandes = list(map(int, f.readline().split()))

    return nbRow, nbColumn, cost, provision, commandes