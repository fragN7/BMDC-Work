import random

def simuleaza_o_data(N):
    cadou = random.randint(0, N - 1)
    alegere = random.randint(0, N - 1)
    
    if alegere == cadou:

        usi_posibile = [i for i in range(N) if i != alegere]
        usa_ramasa = random.choice(usi_posibile)
    else:

        usa_ramasa = cadou

    castig_S1 = (alegere == cadou)    
    castig_S2 = (usa_ramasa == cadou)    
    
    return castig_S1, castig_S2

def ruleaza_simulari(N, K):
    wins_S1 = 0
    wins_S2 = 0
    
    for _ in range(K):
        c1, c2 = simuleaza_o_data(N)
        if c1:
            wins_S1 += 1
        if c2:
            wins_S2 += 1
    
    prob_S1 = wins_S1 / K
    prob_S2 = wins_S2 / K
    
    return prob_S1, prob_S2

def probabilitati_teoretice(N):
    prob_S1 = 1 / N
    prob_S2 = (N - 1) / N
    return prob_S1, prob_S2

def afiseaza_rezultate(N, K, prob_S1, prob_S2):
    teo_S1, teo_S2 = probabilitati_teoretice(N)
    print(f"\nN = {N}, K = {K}")
    print(f"  Strategia 1 (ramai):  {prob_S1:.4f}   (teoretic: {teo_S1:.4f})")
    print(f"  Strategia 2 (schimbi): {prob_S2:.4f}   (teoretic: {teo_S2:.4f})")




def main():
    print("Monty Hall - simulare")
    
    try:
        N = int(input("Numar de usi N (minim 3): "))
    except ValueError:
        print("N invalid.")
        return
    
    if N < 3:
        print("N trebuie sa fie minim 3")
        return
    
    valori_K = [10, 100, 1000, 10000]
    
    raspuns = input(f"Folosesc K = {valori_K}? (d/n): ").strip().lower()
    if raspuns not in ("d", "da", "y", "yes"):
        try:
            s = input("Introdu valorile K separate prin spatiu: ").split()
            valori_K = [int(x) for x in s]
        except ValueError:
            print("Valori K invalide.")
            return
    
    for K in valori_K:
        prob_S1, prob_S2 = ruleaza_simulari(N, K)
        afiseaza_rezultate(N, K, prob_S1, prob_S2)


if __name__ == "__main__":
    main()