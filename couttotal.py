
def calculer_cout(n, m, couts, transport):
    total = 0
    for i in range(n):
        for j in range(m):
            total += couts[i][j] * transport[i][j]
    return total