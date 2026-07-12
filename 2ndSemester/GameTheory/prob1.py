import itertools
import random


def get_int(prompt, min_val=None, max_val=None):
    """Read an integer from the keyboard, re-prompting until it is valid
    and within [min_val, max_val] (either bound may be None)."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
        except ValueError:
            print("  -> Please enter a whole number.")
            continue
        if min_val is not None and val < min_val:
            print(f"  -> Value must be >= {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"  -> Value must be <= {max_val}.")
            continue
        return val


def read_players_and_strategies():
    n = get_int("Number of players (1-10): ", 1, 10)
    strategies = []
    for i in range(n):
        s = get_int(f"Number of strategies for player {i + 1}: ", 1, None)
        strategies.append(s)
    return n, strategies


def read_payoffs(n, strategies, profiles):
    payoffs = {p: {} for p in range(n)}

    choice = input(
        "Introduce payoffs manually or by randomization? (M = manual / R = random): "
    ).strip().upper()
    while choice not in ("M", "R"):
        choice = input("Please answer M or R: ").strip().upper()

    if choice == "R":
        low = get_int("Lower bound for random payoffs: ")
        high = get_int("Upper bound for random payoffs: ", low, None)
        for profile in profiles:
            for p in range(n):
                payoffs[p][profile] = random.randint(low, high)
        print("Random payoffs generated.")
    else:
        print("Enter the payoff of each player for every strategy profile.")
        for profile in profiles:
            label = ", ".join(
                f"P{i + 1}=s{profile[i] + 1}" for i in range(n)
            )
            print(f"Profile ({label}):")
            for p in range(n):
                val = get_int(f"  payoff to player {p + 1}: ")
                payoffs[p][profile] = val

    return payoffs


def print_payoff_table(n, strategies, profiles, payoffs):
    print("\n--- Payoff table ---")
    for profile in profiles:
        label = ", ".join(f"s{profile[i] + 1}" for i in range(n))
        vals = tuple(payoffs[p][profile] for p in range(n))
        print(f"  ({label}) -> {vals}")


def find_pure_nash_equilibria(n, strategies, profiles, payoffs):
    ne_list = []
    for profile in profiles:
        is_ne = True
        for p in range(n):
            current = payoffs[p][profile]
            for alt in range(strategies[p]):
                if alt == profile[p]:
                    continue
                alt_profile = list(profile)
                alt_profile[p] = alt
                alt_profile = tuple(alt_profile)
                if payoffs[p][alt_profile] > current:
                    is_ne = False
                    break
            if not is_ne:
                break
        if is_ne:
            ne_list.append(profile)
    return ne_list


def main():
    print("=== Pure Nash Equilibrium finder (n-player normal-form game) ===")
    n, strategies = read_players_and_strategies()
    profiles = list(itertools.product(*[range(s) for s in strategies]))
    payoffs = read_payoffs(n, strategies, profiles)
    print_payoff_table(n, strategies, profiles, payoffs)

    ne_list = find_pure_nash_equilibria(n, strategies, profiles, payoffs)

    print("\n--- Result ---")
    if not ne_list:
        print("No pure Nash Equilibrium exists in this game.")
    else:
        print(f"{len(ne_list)} pure Nash Equilibrium/Equilibria found:")
        for ne in ne_list:
            vals = tuple(payoffs[p][ne] for p in range(n))
            label = ", ".join(f"Player {i + 1} -> strategy {ne[i] + 1}" for i in range(n))
            print(f"  ({label})   payoffs = {vals}")


if __name__ == "__main__":
    main()
