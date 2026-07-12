import random
# pyright: basic
def cine_joaca(runda):
    if runda % 2 == 1:
        return 1
    else:
        return 2

def rezolva_centipede(L, R):
    n = len(L)  # numarul de runde
    
    valoare_subjoc = [None] * (n + 2)

    valoare_subjoc[n + 1] = (L[n-1], R[n-1])
    
    decizie = [None] * (n + 1)
    
    for i in range(n, 0, -1):
        payoff_stop = (L[i-1], R[i-1])
        payoff_continue = valoare_subjoc[i+1]
        jucator = cine_joaca(i)
        
        if jucator == 1:
            if payoff_stop[0] >= payoff_continue[0]:
                decizie[i] = "Stop"
                valoare_subjoc[i] = payoff_stop
            else:
                decizie[i] = "Continue"
                valoare_subjoc[i] = payoff_continue
        else:
            if payoff_stop[1] >= payoff_continue[1]:
                decizie[i] = "Stop"
                valoare_subjoc[i] = payoff_stop
            else:
                decizie[i] = "Continue"
                valoare_subjoc[i] = payoff_continue
    
    return decizie, valoare_subjoc

def simuleaza_joc(decizie, L, R):
    n = len(L)
    
    for i in range(1, n + 1):
        if decizie[i] == "Stop":
            return i, cine_joaca(i), L[i-1], R[i-1]
    return n, cine_joaca(n), L[n-1], R[n-1]

def afiseaza_rezultat(runda, jucator, payoff_p1, payoff_p2, decizie, n):
    print(f"\nJocul se opreste in runda {runda}")
    print(f"Oprit de: P{jucator}")
    print(f"Payoff final: P1 = {payoff_p1}, P2 = {payoff_p2}")
    
    print("\nDeciziile pentru fiecare runda (backward induction):")
    for i in range(1, n + 1):
        j = cine_joaca(i)
        print(f"  Runda {i:2d} (P{j}): {decizie[i]}")


def citeste_manual(n):
    L = []
    R = []
    print("\nIntrodu payoff-urile pentru fiecare runda.")
    print("Format pe fiecare linie: L R (separate prin spatiu)")
    for i in range(1, n + 1):
        while True:
            s = input(f"Runda {i}: ").split()
            if len(s) != 2:
                print("Introdu 2 numere.")
                continue
            try:
                L.append(int(s[0]))
                R.append(int(s[1]))
                break
            except ValueError:
                print("Numere invalide.")
    return L, R


def genereaza_aleator(n, minim=0, maxim=20):
    L = [random.randint(minim, maxim) for _ in range(n)]
    R = [random.randint(minim, maxim) for _ in range(n)]
    return L, R

def afiseaza_joc(L, R):
    n = len(L)
    print("\nPayoff-uri pe runde:")
    for i in range(1, n + 1):
        j = cine_joaca(i)
        print(f"  Runda {i:2d} (P{j}): Stop -> ({L[i-1]}, {R[i-1]})")

def main():
    print("Problema 4 - Jocul centipede (backward induction)")
    
    try:
        n = int(input("Numar de runde n (par, minim 2): "))
    except ValueError:
        print("n invalid.")
        return
    
    if n < 2 or n % 2 != 0:
        print("n trebuie sa fie par si >= 2.")
        return
    
    raspuns = input("Introduci manual payoff-urile? (d/n): ").strip().lower()
    if raspuns in ("d", "da", "y", "yes"):
        L, R = citeste_manual(n)
    else:
        L, R = genereaza_aleator(n)
    
    afiseaza_joc(L, R)
    
    decizie, _ = rezolva_centipede(L, R)
    runda, jucator, payoff_p1, payoff_p2 = simuleaza_joc(decizie, L, R)
    
    afiseaza_rezultat(runda, jucator, payoff_p1, payoff_p2, decizie, n)


if __name__ == "__main__":
    main()