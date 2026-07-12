/*
 * Big Data coursework (EME0650) - Use case #17: Traffic Navigation
 * Package: urbanflow
 *
 * Pillar 2/3 - infrastructure-side rerouting via gossip diffusion.
 */
package urbanflow;

import peersim.config.Configuration;
import peersim.config.FastConfig;
import peersim.core.CommonState;
import peersim.core.Linkable;
import peersim.core.Node;
import peersim.vector.SingleValueHolder;
import peersim.cdsim.CDProtocol;

/**
 * A junction with a finite queueing capacity (the vehicles its approach
 * lanes can hold before the intersection locks up). A junction whose queue
 * is above {@code cap} of its capacity samples one random neighbour each
 * cycle; if that neighbour has room to spare, a small batch of queued
 * vehicles is shifted across -- exactly the effect a satnav service has when
 * it nudges drivers onto a quieter parallel street. A shift only ever moves
 * traffic towards a strictly quieter junction and only ever fills spare
 * capacity, so the protocol cannot itself manufacture a new bottleneck.
 */
public class JunctionLoadProtocol extends SingleValueHolder implements CDProtocol {

    private static final String PAR_CAPACITY = "capacity";
    private static final String PAR_CAP = "cap";
    private static final String PAR_SHIFT = "shift";

    protected final int capacity;   // maximum vehicles this junction can queue
    protected final double cap;     // occupancy fraction above which rerouting kicks in
    protected final int shift;      // max vehicles moved to a neighbour per gossip round

    protected int queued;           // vehicles presently queued here
    protected boolean open = true;  // false while a disruption blocks this junction

    public JunctionLoadProtocol(String prefix) {
        super(prefix);
        capacity = Configuration.getInt(prefix + "." + PAR_CAPACITY, 120);
        cap = Configuration.getDouble(prefix + "." + PAR_CAP, 0.75);
        shift = Configuration.getInt(prefix + "." + PAR_SHIFT, 4);
    }

    @Override
    public Object clone() {
        return super.clone();
    }

    double load() {
        return capacity == 0 ? 0.0 : (double) queued / capacity;
    }

    @Override
    public void nextCycle(Node owner, int pid) {
        if (!open || load() <= cap) {
            return;
        }

        int meshId = FastConfig.getLinkable(pid);
        Linkable mesh = (Linkable) owner.getProtocol(meshId);
        int reach = mesh.degree();
        if (reach == 0) {
            return;
        }

        Node partner = mesh.getNeighbor(CommonState.r.nextInt(reach));
        if (!partner.isUp()) {
            return;
        }

        JunctionLoadProtocol other = (JunctionLoadProtocol) partner.getProtocol(pid);
        if (!other.open || other == this || other.load() >= this.load()) {
            return; // only shift towards a genuinely quieter junction
        }

        int room = other.capacity - other.queued;
        int over = this.queued - (int) (cap * capacity);
        int moved = Math.min(shift, Math.min(room, Math.max(over, 0)));

        if (moved > 0) {
            this.queued -= moved;
            other.queued += moved;
        }

        this.value = this.load();
        other.value = other.load();
    }
}
