/*
 * Big Data coursework (EME0650) - Use case #17: Traffic Navigation
 * Package: urbanflow
 */
package urbanflow;

import peersim.config.Configuration;
import peersim.core.CommonState;
import peersim.core.Control;
import peersim.core.Network;
import peersim.vector.SingleValue;
import peersim.util.IncrementalStats;

/**
 * Prints one line per cycle summarising how far decentralised flow sensing
 * has converged:
 *
 * <pre>flowlog| tick lo hi live mean spread devi</pre>
 *
 * {@code devi} (standard deviation across all live junctions) is the
 * headline number: it should shrink towards zero as gossip proceeds,
 * showing that every junction now agrees on the true city-wide occupancy.
 */
public class FlowStatsLogger implements Control {

    private static final String PAR_PROT = "protocol";
    private static final String PAR_TARGET = "target";

    private final String tag;
    private final int pid;
    private final double target;

    public FlowStatsLogger(String tag) {
        this.tag = tag;
        pid = Configuration.getPid(tag + "." + PAR_PROT);
        target = Configuration.getDouble(tag + "." + PAR_TARGET, -1);
    }

    @Override
    public boolean execute() {
        long tick = CommonState.getTime();
        IncrementalStats s = new IncrementalStats();
        for (int i = 0; i < Network.size(); i++) {
            if (!Network.get(i).isUp()) {
                continue; // skip junctions currently disrupted
            }
            SingleValue v = (SingleValue) Network.get(i).getProtocol(pid);
            s.add(v.getValue());
        }

        System.out.println(tag + "| " + tick
                + " " + s.getMin()
                + " " + s.getMax()
                + " " + s.getN()
                + " " + s.getAverage()
                + " " + s.getVar()
                + " " + s.getStD());

        return target > 0 && s.getStD() <= target;
    }
}
