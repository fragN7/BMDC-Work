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
 * Seeds every junction's physical state for the adaptive-rerouting scenario:
 * an independent random vehicle queue in [{@code lo}, {@code hi}], all
 * junctions open. Drawing the initial queue from a wide range deliberately
 * creates a rush-hour-like starting point, with a meaningful share of
 * junctions already over the congestion cap, for rerouting to relieve.
 */
public class JunctionSeedInit implements Control {

    private static final String PAR_PROT = "protocol";
    private static final String PAR_LO = "lo";
    private static final String PAR_HI = "hi";

    private final int pid;
    private final int lo;
    private final int hi;

    public JunctionSeedInit(String prefix) {
        pid = Configuration.getPid(prefix + "." + PAR_PROT);
        lo = Configuration.getInt(prefix + "." + PAR_LO, 1);
        hi = Configuration.getInt(prefix + "." + PAR_HI, 60);
    }

    @Override
    public boolean execute() {
        for (int i = 0; i < Network.size(); i++) {
            JunctionLoadProtocol j = (JunctionLoadProtocol) Network.get(i).getProtocol(pid);
            j.queued = lo + CommonState.r.nextInt(hi - lo + 1);
            j.open = true;
            j.setValue(j.load());
        }
        return false;
    }
}
