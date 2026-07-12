"""
Problema 1 - Echilibre Nash pure, joc 2 jucatori, forma normala.
"""

import random
import time


def citeste_int(prompt, minim=1):
    while True:
        try:
            v = int(input(prompt))
            if v < minim:
                print(f"Minim {minim}")
                continue
            return v
        except ValueError:
            print("Nu e valid")


def citeste_payoffs_manual(m, n):
    P1 = [[0.0] * n for _ in range(m)]
    P2 = [[0.0] * n for _ in range(m)]
    print()
    for i in range(m):
        for j in range(n):
            while True:
                s = input(f"P1({i+1},{j+1}) P2({i+1},{j+1}): ").split()
                if len(s) != 2:
                    print("Introdu 2 numere separate prin spatiu")
                    continue
                try:
                    P1[i][j] = float(s[0])
                    P2[i][j] = float(s[1])
                    break
                except ValueError:
                    print("Nu sunt valide")
    return P1, P2


def genereaza_random(m, n, a=-10, b=10):
    P1 = [[random.randint(a, b) for _ in range(n)] for _ in range(m)]
    P2 = [[random.randint(a, b) for _ in range(n)] for _ in range(m)]
    return P1, P2


def afiseaza_matrice(P1, P2):
    m, n = len(P1), len(P1[0])
    print("\nMatricea jocului:")
    header = "     "
    for j in range(n):
        header += f"  C{j+1:<2}     "
    print(header)
    for i in range(m):
        rand = f"R{i+1:<2}  "
        for j in range(n):
            rand += f"({P1[i][j]:>3},{P2[i][j]:>3})  "
        print(rand)


def gaseste_NE(P1, P2):
    m, n = len(P1), len(P1[0])
    max_col = [max(P1[i][j] for i in range(m)) for j in range(n)]
    max_rand = [max(P2[i][j] for j in range(n)) for i in range(m)]
    ne = []
    for i in range(m):
        for j in range(n):
            if P1[i][j] == max_col[j] and P2[i][j] == max_rand[i]:
                ne.append((i, j))
    return ne


def afiseaza_rezultate(ne, P1, P2, durata_ms):
    print()
    if not ne:
        print("Nu exista echilibru Nash pur")
    else:
        print(f"Echilibre Nash pure gasite: {len(ne)}")
        for (i, j) in ne:
            print(f"  (R{i+1}, C{j+1}) -> ({P1[i][j]}, {P2[i][j]})")
    print(f"Timp: {durata_ms:.2f} ms")


def test_predefinit(nume, P1, P2):
    print(f"\n--- {nume} ---")
    afiseaza_matrice(P1, P2)
    t0 = time.perf_counter()
    ne = gaseste_NE(P1, P2)
    dt = (time.perf_counter() - t0) * 1000
    afiseaza_rezultate(ne, P1, P2, dt)


def ruleaza_teste_clasice():
    test_predefinit("Dilema Prizonierului",
                    [[-1, -3], [0, -2]],
                    [[-1, 0], [-3, -2]])
    test_predefinit("Battle of the Sexes",
                    [[2, 0], [0, 1]],
                    [[1, 0], [0, 2]])
    test_predefinit("Matching Pennies",
                    [[1, -1], [-1, 1]],
                    [[-1, 1], [1, -1]])
    test_predefinit("Coordination",
                    [[3, 0], [0, 2]],
                    [[3, 0], [0, 2]])
    test_predefinit("Joc 3x3",
                    [[4, 3, 2], [3, 2, 1], [2, 1, 0]],
                    [[4, 3, 2], [3, 2, 1], [2, 1, 0]])


def test_performanta():
    s = input("Dimensiuni de testat: ").strip()
    if s == "":
        dimensiuni = [10, 50, 100, 500, 1000]
    else:
        try:
            dimensiuni = [int(x) for x in s.split()]
        except ValueError:
            print("Valori invalide.")
            return
    print()
    for dim in dimensiuni:
        P1, P2 = genereaza_random(dim, dim, -100, 100)
        t0 = time.perf_counter()
        ne = gaseste_NE(P1, P2)
        dt = (time.perf_counter() - t0) * 1000
        print(f"  {dim}x{dim}: {len(ne)} NE, {dt:.2f} ms")


def main():
    while True:
        print("\n1. Joc nou (manual sau random)")
        print("2. Teste predefinite")
        print("3. Test performanta")
        print("4. Iesire")
        opt = input("Optiune: ").strip()

        if opt == "1":
            m = citeste_int("Numar strategii P1: ")
            n = citeste_int("Numar strategii P2: ")
            raspuns = input("Introduci manual payoff-urile?: ").strip().lower()
            if raspuns in ("d", "da", "y", "yes"):
                P1, P2 = citeste_payoffs_manual(m, n)
            else:
                P1, P2 = genereaza_random(m, n)
            afiseaza_matrice(P1, P2)
            t0 = time.perf_counter()
            ne = gaseste_NE(P1, P2)
            dt = (time.perf_counter() - t0) * 1000
            afiseaza_rezultate(ne, P1, P2, dt)
        elif opt == "2":
            ruleaza_teste_clasice()
        elif opt == "3":
            test_performanta()
        elif opt == "4":
            break
        else:
            print("Optiune invalida ")


if __name__ == "__main__":
    main()