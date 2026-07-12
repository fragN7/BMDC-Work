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

/**
 * Seeds every junction's flow-sensing reading with an independent uniform
 * draw in [{@code lo}, {@code hi}] -- the raw, un-aggregated starting point
 * that gossip must reconcile into one shared city-wide figure.
 */
public class FlowSeedInit implements Control {

    private static final String PAR_PROT = "protocol";
    private static final String PAR_LO = "lo";
    private static final String PAR_HI = "hi";

    private final int pid;
    private final double lo;
    private final double hi;

    public FlowSeedInit(String prefix) {
        pid = Configuration.getPid(prefix + "." + PAR_PROT);
        hi = Configuration.getDouble(prefix + "." + PAR_HI, 1.0);
        lo = Configuration.getDouble(prefix + "." + PAR_LO, 0.0);
    }

    @Override
    public boolean execute() {
        for (int i = 0; i < Network.size(); i++) {
            SingleValue v = (SingleValue) Network.get(i).getProtocol(pid);
            v.setValue(lo + CommonState.r.nextDouble() * (hi - lo));
        }
        return false;
    }
}
