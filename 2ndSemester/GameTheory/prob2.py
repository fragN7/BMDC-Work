

import random


def get_float(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("  -> Please enter a number.")


def read_matrix(label):
    print(f"Payoff matrix for {label} (row = own strategy, column = opponent strategy).")
    m = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(2):
        for j in range(2):
            m[i][j] = get_float(f"  {label} payoff at (S{i + 1}, S{j + 1}): ")
    return m


def read_payoffs():
    choice = input(
        "Introduce payoffs manually or by randomization? (M = manual / R = random): "
    ).strip().upper()
    while choice not in ("M", "R"):
        choice = input("Please answer M or R: ").strip().upper()

    if choice == "R":
        low = get_float("Lower bound for random payoffs: ")
        high = get_float("Upper bound for random payoffs: ")
        A = [[round(random.uniform(low, high), 2) for _ in range(2)] for _ in range(2)]
        B = [[round(random.uniform(low, high), 2) for _ in range(2)] for _ in range(2)]
        print("Random payoff matrices generated.")
    else:
        A = read_matrix("Player 1")
        B = read_matrix("Player 2")

    return A, B


def print_matrices(A, B):
    print("\nPlayer 1 payoff matrix A:")
    for row in A:
        print(f"  {row}")
    print("Player 2 payoff matrix B:")
    for row in B:
        print(f"  {row}")


def find_completely_mixed_ne(A, B):
    """Returns (p, q) or None if no completely mixed NE exists."""
    a11, a12 = A[0]
    a21, a22 = A[1]
    b11, b12 = B[0]
    b21, b22 = B[1]

    denom_p = b11 - b12 - b21 + b22
    denom_q = a11 - a12 - a21 + a22

    if denom_p == 0 or denom_q == 0:
        return None

    p = (b22 - b21) / denom_p
    q = (a22 - a12) / denom_q

    if 0 < p < 1 and 0 < q < 1:
        return (p, q)
    return None


def main():
    print("=== Completely mixed Nash Equilibrium finder (2 players, 2 strategies) ===")
    A, B = read_payoffs()
    print_matrices(A, B)

    result = find_completely_mixed_ne(A, B)

    print("\n--- Result ---")
    if result is None:
        print("No completely mixed Nash Equilibrium exists for this game.")
    else:
        p, q = result
        print("Completely mixed Nash Equilibrium found:")
        print(f"  Player 1 mixes: (S1 w.p. {p:.4f}, S2 w.p. {1 - p:.4f})")
        print(f"  Player 2 mixes: (S1 w.p. {q:.4f}, S2 w.p. {1 - q:.4f})")


if __name__ == "__main__":
    main()
