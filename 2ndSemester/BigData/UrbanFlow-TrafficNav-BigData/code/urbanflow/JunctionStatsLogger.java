/*
 * Big Data coursework (EME0650) - Use case #17: Traffic Navigation
 * Package: urbanflow
 */
package urbanflow;

import peersim.config.Configuration;
import peersim.core.CommonState;
import peersim.core.Control;
import peersim.core.Network;

/**
 * Prints one line per cycle summarising the effect of decentralised
 * rerouting on the junction mesh:
 *
 * <pre>meshlog| tick openCount fleetSize meanLoad peakLoad lockups overCapShare</pre>
 *
 * <ul>
 * <li><b>openCount</b>    - junctions not currently disrupted</li>
 * <li><b>fleetSize</b>    - vehicles queued network-wide</li>
 * <li><b>meanLoad</b>     - mean occupancy of open junctions</li>
 * <li><b>peakLoad</b>     - highest occupancy anywhere (watch for &gt; 1.0)</li>
 * <li><b>lockups</b>      - junctions past 100% capacity (queue overflow)</li>
 * <li><b>overCapShare</b> - fraction of open junctions past the rerouting cap</li>
 * </ul>
 */
public class JunctionStatsLogger implements Control {

    private static final String PAR_PROT = "protocol";
    private static final String PAR_CAP = "cap";

    private final String tag;
    private final int pid;
    private final double cap;

    public JunctionStatsLogger(String tag) {
        this.tag = tag;
        pid = Configuration.getPid(tag + "." + PAR_PROT);
        cap = Configuration.getDouble(tag + "." + PAR_CAP, 0.75);
    }

    @Override
    public boolean execute() {
        long tick = CommonState.getTime();
        int n = Network.size();
        int openCount = 0;
        int lockups = 0;
        int overCap = 0;
        long fleetSize = 0;
        double loadSum = 0.0;
        double peakLoad = 0.0;

        for (int i = 0; i < n; i++) {
            JunctionLoadProtocol j = (JunctionLoadProtocol) Network.get(i).getProtocol(pid);
            fleetSize += j.queued;
            if (j.open) {
                openCount++;
                double load = j.load();
                loadSum += load;
                if (load > peakLoad) {
                    peakLoad = load;
                }
                if (load > 1.0) {
                    lockups++;
                }
                if (load > cap) {
                    overCap++;
                }
            }
        }

        double meanLoad = openCount == 0 ? 0.0 : loadSum / openCount;
        double overCapShare = openCount == 0 ? 0.0 : (double) overCap / openCount;

        System.out.println(tag + "| " + tick
                + " " + openCount
                + " " + fleetSize
                + " " + meanLoad
                + " " + peakLoad
                + " " + lockups
                + " " + overCapShare);
        return false;
    }
}
