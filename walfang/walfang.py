#!/usr/bin/env python
import sys
import math
import random

def uniform(groesse, wert = 0):
    lst = []
    for y in range(0, groesse):
        xlst = []
        for x in range(0, groesse):
            xlst.append(wert)
        lst.append(xlst)

    return lst

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def sonar(wal, schiff, groesse):
    dst = dist(wal, schiff)
    d = []
    for y in range(0, groesse):
        d.append([])
        for x in range(0, groesse):
            d[y].append(1 if dst == dist(schiff, [x, y]) else 0)

    return d

def normal(mat):
    sum = 0
    for line in mat:
        for e in line:
            sum += e
    for y in range(0, len(mat)):
        for x in range(0, len(mat[y])):
            mat[y][x] /= sum
    return mat

def mult(a, b):
    for y in range(len(a)):
        for x in range(len(a[y])):
            a[y][x] *= b[y][x]
    return a

def bayesupdate(mat, wal, schiff):
    groesse = len(mat)
    d = sonar(wal, schiff, groesse)
    mat = mult(mat, d)
    mat = normal(mat)
    return mat

def walposition(mat):
    pos = None
    for y in range(len(mat)):
        for x in range(len(mat[y])):
            if mat[y][x] != 0:
                if pos == None:
                    pos = [x, y]
                else:
                    return None
    return pos

def entropie(mat):
    sum = 0
    for y in range(len(mat)):
        for x in range(len(mat[y])):
            if mat[y][x] != 0:
                sum += mat[y][x] + math.log(mat[y][x])
    return -sum

def bewegungen(pos, groesse):
    bew = [pos]
    if pos[0] - 1 >= 0:
        bew.append([pos[0] - 1, pos[1]])
    if pos[0] + 1 < groesse:
        bew.append([pos[0] + 1, pos[1]])
    if pos[1] - 1 >= 0:
        bew.append([pos[0], pos[1] - 1])
    if pos[1] + 1 < groesse:
        bew.append([pos[0], pos[1] + 1])

    if pos[0] - 1 >= 0 and pos[1] - 1 >= 0:
        bew.append([pos[0] - 1, pos[1] - 1])
    if pos[0] - 1 >= 0 and pos[1] + 1 < groesse:
        bew.append([pos[0] - 1, pos[1] + 1])
    if pos[0] + 1 < groesse and pos[1] + 1 < groesse:
        bew.append([pos[0] + 1, pos[1] + 1])
    if pos[0] + 1 < groesse and pos[1] - 1 >= 0:
        bew.append([pos[0] + 1, pos[1] - 1])
    return bew

def unschaerfe(mat):
    a = uniform(len(mat))
    for y in range(len(mat)):
        for x in range(len(mat[y])):
            for pos in bewegungen([x, y], len(mat)):
                a[pos[1]][pos[0]] += mat[y][x]
    return normal(a)


def printmat(mat):
    for line in reversed(mat):
        for e in line:
            print("{:04f}".format(e), end = " ")
        print("")
    print("")

groesse = 10
schiff = [5, 5]
wal = [random.randint(0, groesse - 1), random.randint(0, groesse - 1)]
print("Initial:")
mat = uniform(groesse, 1 / (groesse * groesse))
printmat(mat)

mat = bayesupdate(mat, wal, schiff)

schritt = 0
while 1:
    schritt += 1
    print("Schritt {:d}:".format(schritt))
    print("Schiffsposition: {:04f}, {:04f}".format(schiff[0], schiff[1]))
    print("Walposition: {:04f}, {:04f}".format(wal[0], wal[1]))
    printmat(mat)
    walpos = walposition(mat)
    if walpos != None:
        print("Wal gefunden: {:04f}, {:04f}".format(walpos[0], walpos[1]))
        break;
    elif schritt >= 100:
        print("Abbruch.")
        break;

    wal = random.choice(bewegungen(wal, groesse))
    mat = unschaerfe(mat)

    mine = 900000
    minmat = []
    minpos = schiff
    for tb in bewegungen(schiff, groesse):
        tmat = bayesupdate(mat, wal, tb)
        te = entropie(tmat)
        if(te < mine):
            mine = te
            minpos = tb
            minmat = tmat

    mat = tmat
    schiff = minpos
