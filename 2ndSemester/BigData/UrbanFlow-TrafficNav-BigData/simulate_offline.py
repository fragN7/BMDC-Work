#!/usr/bin/env python3

import os
import random
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)

SEED = 918273645
MESH_K = 8       # matches init.mesh.k in the .cfg files
MESH_BETA = 0.08  # matches init.mesh.beta


def build_mesh(n, k, beta, rng):
    """Watts-Strogatz small-world mesh: local ring links (degree k) with a
    beta-fraction of links rewired into long-range shortcuts."""
    half = k // 2
    links = [set() for _ in range(n)]
    for i in range(n):
        for d in range(1, half + 1):
            j = (i + d) % n
            links[i].add(j)
            links[j].add(i)
    for i in range(n):
        for d in range(1, half + 1):
            j = (i + d) % n
            if j in links[i] and rng.random() < beta:
                m = rng.randrange(n)
                tries = 0
                while (m == i or m in links[i]) and tries < 10:
                    m = rng.randrange(n)
                    tries += 1
                if m != i and m not in links[i]:
                    links[i].discard(j)
                    links[j].discard(i)
                    links[i].add(m)
                    links[m].add(i)
    return [list(s) for s in links]


def dump(path, header, rows):
    with open(path, "w") as f:
        f.write(header + "\n")
        for r in rows:
            f.write(" ".join(str(x) for x in r) + "\n")


def loop_distance(a, b, n):
    gap = abs(a - b)
    return min(gap, n - gap)


def scenario1_flow_sensing(n, ticks=45, seed=SEED):
    """Mirrors FlowGossipProtocol.nextCycle() + FlowStatsLogger."""
    rng = random.Random(seed)
    links = build_mesh(n, MESH_K, MESH_BETA, rng)
    reading = [rng.uniform(0.0, 1.0) for _ in range(n)]

    rows = []
    for t in range(ticks + 1):
        lo, hi, mean = min(reading), max(reading), sum(reading) / n
        spread = statistics.pvariance(reading)
        devi = spread ** 0.5
        rows.append((t, lo, hi, n, mean, spread, devi))
        if t == ticks:
            break
        order = list(range(n))
        rng.shuffle(order)
        for i in order:
            deg = len(links[i])
            if deg == 0:
                continue
            partner = links[i][rng.randrange(deg)]
            settled = (reading[i] + reading[partner]) / 2.0
            reading[i] = settled
            reading[partner] = settled
    return rows


def scenario3_disruption(n, rate, ticks=65, seed=SEED):
    """Mirrors DisruptionInjector.execute() run alongside flow sensing."""
    rng = random.Random(seed)
    links = build_mesh(n, MESH_K, MESH_BETA, rng)
    reading = [rng.uniform(0.0, 1.0) for _ in range(n)]

    rows = []
    hits = int(rate * n)
    for t in range(ticks + 1):
        lo, hi, mean = min(reading), max(reading), sum(reading) / n
        spread = statistics.pvariance(reading)
        devi = spread ** 0.5
        rows.append((t, lo, hi, n, mean, spread, devi))
        if t == ticks:
            break
        for _ in range(hits):
            idx = rng.randrange(n)
            reading[idx] = rng.uniform(0.0, 1.0)
        order = list(range(n))
        rng.shuffle(order)
        for i in order:
            deg = len(links[i])
            if deg == 0:
                continue
            partner = links[i][rng.randrange(deg)]
            settled = (reading[i] + reading[partner]) / 2.0
            reading[i] = settled
            reading[partner] = settled
    return rows


def scenario2_adaptive_routing(n, ticks=45, seed=SEED, capacity=120, cap=0.75,
                                 shift=4, probe_count=4, hop_budget=14,
                                 journey_span=25, avoidance_weight=2.5):
    """Mirrors JunctionLoadProtocol.nextCycle() + TripAgentDispatcher.execute()."""
    rng = random.Random(seed)
    links = build_mesh(n, MESH_K, MESH_BETA, rng)
    queued = [rng.randint(12, 114) for _ in range(n)]
    open_ = [True] * n  # no disruptions in this scenario
    dispatch_rate = max(25, n // 48)  # proportionally scaled trip-arrival rate

    def load(i):
        return queued[i] / capacity

    mesh_rows = []
    trip_rows = []
    on_road = []  # [at, goal, hopsUsed, diverted]

    dispatched = arrived = stranded = diverted = hops_on_arrival = 0

    for t in range(ticks + 1):
        open_count = sum(open_)
        fleet = sum(queued)
        loads = [load(i) for i in range(n) if open_[i]]
        mean_load = sum(loads) / open_count if open_count else 0.0
        peak_load = max(loads) if loads else 0.0
        lockups = sum(1 for x in loads if x > 1.0)
        over_cap = sum(1 for x in loads if x > cap)
        over_cap_share = over_cap / open_count if open_count else 0.0
        mesh_rows.append((t, open_count, fleet, mean_load, peak_load, lockups, over_cap_share))

        divert_share = (diverted / arrived) if arrived else 0.0
        avg_hops = (hops_on_arrival / arrived) if arrived else 0.0
        trip_rows.append((t, dispatched, arrived, stranded, diverted, divert_share, avg_hops))

        if t == ticks:
            break

        # --- JunctionLoadProtocol.nextCycle(): infrastructure-side diffusion ---
        order = list(range(n))
        rng.shuffle(order)
        for i in order:
            if not open_[i] or load(i) <= cap:
                continue
            deg = len(links[i])
            if deg == 0:
                continue
            partner = links[i][rng.randrange(deg)]
            if not open_[partner] or partner == i:
                continue
            if load(partner) >= load(i):
                continue
            room = capacity - queued[partner]
            over = queued[i] - int(cap * capacity)
            moved = min(shift, room, max(over, 0))
            if moved > 0:
                queued[i] -= moved
                queued[partner] += moved

        # --- TripAgentDispatcher.execute(): dispatch + advance trips ---
        for _ in range(dispatch_rate):
            o = rng.randrange(n)
            span = 1 + rng.randrange(journey_span)
            if rng.random() < 0.5:
                span = -span
            g = (o + span) % n
            if o == g or not open_[o]:
                continue
            queued[o] += 1
            on_road.append([o, g, 0, False])
            dispatched += 1

        still_on_road = []
        for trip in on_road:
            at, goal, hops, div = trip
            if at == goal:
                continue
            if not open_[at]:
                hops += 1
                if hops >= hop_budget:
                    queued[at] = max(0, queued[at] - 1)
                    stranded += 1
                else:
                    still_on_road.append([at, goal, hops, div])
                continue

            deg = len(links[at])
            if deg == 0:
                hops += 1
                if hops >= hop_budget:
                    queued[at] = max(0, queued[at] - 1)
                    stranded += 1
                else:
                    still_on_road.append([at, goal, hops, div])
                continue

            pick = None
            pick_score = float("inf")
            shortest_dist = None
            shortest_pick = None
            for _ in range(min(probe_count, deg)):
                cand = links[at][rng.randrange(deg)]
                if not open_[cand]:
                    continue
                dist = loop_distance(cand, goal, n)
                score = dist + avoidance_weight * load(cand)
                if shortest_dist is None or dist < shortest_dist:
                    shortest_dist = dist
                    shortest_pick = cand
                if score < pick_score:
                    pick_score = score
                    pick = cand

            if pick is None:
                hops += 1
            else:
                if pick != shortest_pick:
                    div = True
                queued[at] = max(0, queued[at] - 1)
                queued[pick] += 1
                at = pick
                hops += 1

            if at == goal:
                queued[at] = max(0, queued[at] - 1)
                arrived += 1
                hops_on_arrival += hops
                if div:
                    diverted += 1
            elif hops >= hop_budget:
                queued[at] = max(0, queued[at] - 1)
                stranded += 1
            else:
                still_on_road.append([at, goal, hops, div])
        on_road = still_on_road

    return mesh_rows, trip_rows


if __name__ == "__main__":
    print("Scenario 1 - flow sensing")
    for n in (1200, 12000, 120000):
        rows = scenario1_flow_sensing(n)
        dump(os.path.join(RESULTS, f"flowsense_{n}.dat"),
             "tick lo hi live mean spread devi", rows)
        print(f"  mesh size {n}: final devi={rows[-1][-1]:.6f}")

    print("Scenario 2 - adaptive rerouting")
    for n in (1200, 12000, 120000):
        mrows, trows = scenario2_adaptive_routing(n)
        dump(os.path.join(RESULTS, f"meshload_{n}.dat"),
             "tick openCount fleetSize meanLoad peakLoad lockups overCapShare", mrows)
        dump(os.path.join(RESULTS, f"tripflow_{n}.dat"),
             "tick dispatched arrived stranded diverted divertShare avgHops", trows)
        print(f"  mesh size {n}: overCapShare {mrows[0][6]:.4f} -> {mrows[-1][6]:.4f} "
              f"| arrived={trows[-1][2]} divertShare={trows[-1][5]:.4f} avgHops={trows[-1][6]:.2f}")

    print("Scenario 3 - disruption resilience")
    for r in (0.01, 0.02, 0.05, 0.10, 0.20):
        rows = scenario3_disruption(12000, r)
        dump(os.path.join(RESULTS, f"disruption_{r:.2f}.dat"),
             "tick lo hi live mean spread devi", rows)
        print(f"  rate={r}: settled devi={rows[-1][-1]:.4f}")

    print("Done. Results written to", RESULTS)
