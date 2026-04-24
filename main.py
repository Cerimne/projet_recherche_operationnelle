# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def read_pb(name):
    with open("problemes/"+name+".txt", 'r') as f:
        size = f.readline()
        nbRow, nbColumn = size.split()
        cost= []
        provision = []
        for i in range(int(nbRow)):
            l=f.readline().split()
            provision.append(l[-1])
            cost.append(list(map(int,l[0:int(nbColumn)])))
        commandes=f.readline().split()
    return cost, list(map(int,provision)), list(map(int,commandes))
print(read_pb("test"))