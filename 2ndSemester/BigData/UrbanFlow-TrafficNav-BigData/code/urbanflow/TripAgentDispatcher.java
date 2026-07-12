/*
 * Big Data coursework (EME0650) - Use case #17: Traffic Navigation
 * Package: urbanflow
 *
 * Pillar 3/3 - trip agents: the mobile entity type layered on the mesh.
 */
package urbanflow;

import peersim.config.Configuration;
import peersim.config.FastConfig;
import peersim.core.CommonState;
import peersim.core.Control;
import peersim.core.Linkable;
import peersim.core.Network;
import peersim.core.Node;

/**
 * {@link JunctionLoadProtocol} models the fixed infrastructure; this class
 * supplies the second entity type the brief asks for: individual vehicles.
 * PeerSim's engine is built around a fixed roster of long-lived nodes, so a
 * trip is not a Node in its own right but a short-lived record that this
 * Control creates, advances and discards -- much as a real navigation app
 * treats a car as a transient trip consuming a crowd-sourced congestion
 * signal, not as a permanent participant of the road mesh.
 *
 * A node's index doubles as its rough position along the city's ring
 * boulevard (the mesh is wired as a Watts-Strogatz small world, so most
 * links are short and local with a handful of long motorway-style
 * shortcuts). Each cycle a batch of trips is spawned between an origin and a
 * destination within {@code journeySpan} positions of it -- a realistic,
 * in-city journey rather than a cross-town one. Every active trip then takes
 * one hop: it samples {@code probeCount} random neighbours of its current
 * junction and moves to whichever one best trades off closing the distance
 * to its destination against sitting in a queue -- a decision made purely
 * from locally visible information, exactly as a satnav app reroutes a
 * driver without knowing the state of the whole city.
 */
public class TripAgentDispatcher implements Control {

    private static final String PAR_PROT = "protocol";
    private static final String PAR_RATE = "dispatchRate";
    private static final String PAR_HOPBUDGET = "hopBudget";
    private static final String PAR_PROBES = "probeCount";
    private static final String PAR_SPAN = "journeySpan";
    private static final String PAR_AVOID = "avoidanceWeight";

    private final int pid;
    private final int dispatchRate;
    private final int hopBudget;
    private final int probeCount;
    private final int journeySpan;
    private final double avoidanceWeight;

    private static final class Trip {
        int at;
        int goal;
        int hopsUsed;
        boolean diverted; // took a path other than the plain shortest one
    }

    private final java.util.List<Trip> onTheRoad = new java.util.ArrayList<>();

    // cumulative counters, surfaced by TripStatsLogger
    static long dispatched = 0;
    static long arrived = 0;
    static long stranded = 0;   // exceeded hopBudget without arriving
    static long diverted = 0;
    static long hopsOnArrival = 0;

    public TripAgentDispatcher(String prefix) {
        pid = Configuration.getPid(prefix + "." + PAR_PROT);
        dispatchRate = Configuration.getInt(prefix + "." + PAR_RATE, 250);
        hopBudget = Configuration.getInt(prefix + "." + PAR_HOPBUDGET, 14);
        probeCount = Configuration.getInt(prefix + "." + PAR_PROBES, 4);
        journeySpan = Configuration.getInt(prefix + "." + PAR_SPAN, 25);
        avoidanceWeight = Configuration.getDouble(prefix + "." + PAR_AVOID, 2.5);
    }

    private int loopDistance(int a, int b, int n) {
        int gap = Math.abs(a - b);
        return Math.min(gap, n - gap);
    }

    @Override
    public boolean execute() {
        int n = Network.size();
        if (n == 0) {
            return false;
        }

        // 1) dispatch new trips: origin plus a destination within journeySpan
        for (int s = 0; s < dispatchRate; s++) {
            int origin = CommonState.r.nextInt(n);
            int span = 1 + CommonState.r.nextInt(journeySpan);
            if (CommonState.r.nextBoolean()) {
                span = -span;
            }
            int goal = ((origin + span) % n + n) % n;
            if (origin == goal) {
                continue;
            }
            Node originNode = Network.get(origin);
            if (!originNode.isUp()) {
                continue;
            }
            JunctionLoadProtocol jp = (JunctionLoadProtocol) originNode.getProtocol(pid);
            if (!jp.open) {
                continue;
            }
            jp.queued++;
            Trip t = new Trip();
            t.at = origin;
            t.goal = goal;
            t.hopsUsed = 0;
            t.diverted = false;
            onTheRoad.add(t);
            dispatched++;
        }

        // 2) advance every trip currently on the road by one hop
        java.util.Iterator<Trip> it = onTheRoad.iterator();
        while (it.hasNext()) {
            Trip t = it.next();
            if (t.at == t.goal) {
                it.remove();
                continue;
            }

            Node here = Network.get(t.at);
            JunctionLoadProtocol hereState = (JunctionLoadProtocol) here.getProtocol(pid);

            if (!here.isUp() || !hereState.open) {
                t.hopsUsed++;
                if (t.hopsUsed >= hopBudget) {
                    hereState.queued = Math.max(0, hereState.queued - 1);
                    stranded++;
                    it.remove();
                }
                continue;
            }

            int meshId = FastConfig.getLinkable(pid);
            Linkable mesh = (Linkable) here.getProtocol(meshId);
            int reach = mesh.degree();
            if (reach == 0) {
                t.hopsUsed++;
                if (t.hopsUsed >= hopBudget) {
                    hereState.queued = Math.max(0, hereState.queued - 1);
                    stranded++;
                    it.remove();
                }
                continue;
            }

            Node pick = null;
            JunctionLoadProtocol pickState = null;
            double pickScore = Double.MAX_VALUE;
            int shortestDist = Integer.MAX_VALUE;
            Node shortestPick = null;
            for (int k = 0; k < Math.min(probeCount, reach); k++) {
                Node cand = mesh.getNeighbor(CommonState.r.nextInt(reach));
                if (!cand.isUp()) {
                    continue;
                }
                JunctionLoadProtocol candState = (JunctionLoadProtocol) cand.getProtocol(pid);
                if (!candState.open) {
                    continue;
                }
                int dist = loopDistance(cand.getIndex(), t.goal, n);
                double score = dist + avoidanceWeight * candState.load();
                if (dist < shortestDist) {
                    shortestDist = dist;
                    shortestPick = cand;
                }
                if (score < pickScore) {
                    pickScore = score;
                    pick = cand;
                    pickState = candState;
                }
            }

            if (pick == null) {
                t.hopsUsed++;
            } else {
                if (pick != shortestPick) {
                    t.diverted = true;
                }
                hereState.queued = Math.max(0, hereState.queued - 1);
                pickState.queued++;
                t.at = pick.getIndex();
                t.hopsUsed++;
            }

            if (t.at == t.goal) {
                JunctionLoadProtocol goalState = (JunctionLoadProtocol) Network.get(t.at).getProtocol(pid);
                goalState.queued = Math.max(0, goalState.queued - 1);
                arrived++;
                hopsOnArrival += t.hopsUsed;
                if (t.diverted) {
                    diverted++;
                }
                it.remove();
            } else if (t.hopsUsed >= hopBudget) {
                JunctionLoadProtocol stuckState = (JunctionLoadProtocol) Network.get(t.at).getProtocol(pid);
                stuckState.queued = Math.max(0, stuckState.queued - 1);
                stranded++;
                it.remove();
            }
        }

        return false;
    }
}
