#!/usr/bin/env python
import math

def normmat(mat):
    sum = 0
    for line in mat:
        for e in line:
            sum += e
    for y in range(0, len(mat)):
        for x in range(0, len(mat[y])):
            mat[y][x] /= sum
    return mat

def printmat(mat):
    for line in mat:
        for e in line:
            print("{:04f}".format(e), end = " ")
        print("")
    print("")

def printvec(vec):
    for e in vec:
        print("{:04f}".format(e), end = " ")
    print("")

U = [[1, 0],
     [0, 1]]

p_a_s = [[0.25, 0.25],
         [0.25, 0.25]]

p_s = [0.5, 0.5]

p_a = []
for a in range(len(U[0])):
    p_a.append(1 / len(U[0]))

beta = 80

step = 0
while True:
    for a in range(len(U[0])):
        for s in range(len(U)):
            p_a_s[s][a] = p_a[a] * math.exp(beta * U[s][a])

    p_a_s = normmat(p_a_s)

    for a in range(len(U[0])):
        p_a[a] = 0
        for s in range(len(U)):
            p_a[a] += p_a_s[s][a] * p_s[s]

    step += 1
    print("Schritt {:d}:".format(step))
    printmat(p_a_s)
    if step >= 20:
        print("Abbruch.")
        break
