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
 * Injects road disruptions into the flow-sensing scenario. Each cycle a
 * fraction {@code rate} of junctions suffers a sudden event -- an accident,
 * emergency roadworks, a stalled vehicle -- and its locally sensed reading
 * is overwritten with a fresh, un-aggregated draw from [{@code lo},
 * {@code hi}], exactly as a real sensor would report a brand-new spike.
 * This keeps feeding raw noise into the mesh and tests whether flow sensing
 * still tracks the true city-wide average under constant, realistic
 * disruption.
 */
public class DisruptionInjector implements Control {

    private static final String PAR_PROT = "protocol";
    private static final String PAR_RATE = "disruptionRate";
    private static final String PAR_LO = "lo";
    private static final String PAR_HI = "hi";

    private final int pid;
    private final double rate;
    private final double lo;
    private final double hi;

    public DisruptionInjector(String prefix) {
        pid = Configuration.getPid(prefix + "." + PAR_PROT);
        rate = Configuration.getDouble(prefix + "." + PAR_RATE, 0.05);
        hi = Configuration.getDouble(prefix + "." + PAR_HI, 1.0);
        lo = Configuration.getDouble(prefix + "." + PAR_LO, 0.0);
    }

    @Override
    public boolean execute() {
        int hits = (int) (rate * Network.size());
        for (int k = 0; k < hits; k++) {
            int idx = CommonState.r.nextInt(Network.size());
            SingleValue v = (SingleValue) Network.get(idx).getProtocol(pid);
            v.setValue(lo + CommonState.r.nextDouble() * (hi - lo));
        }
        return false;
    }
}
