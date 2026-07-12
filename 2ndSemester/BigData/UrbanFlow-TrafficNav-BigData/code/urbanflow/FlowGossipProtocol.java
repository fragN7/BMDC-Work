/*
 * Big Data coursework (EME0650) - Use case #17: Traffic Navigation
 * Package: urbanflow
 *
 * Pillar 1/3 - decentralised flow sensing via epidemic averaging.
 */
package urbanflow;

import peersim.config.FastConfig;
import peersim.core.CommonState;
import peersim.core.Linkable;
import peersim.core.Node;
import peersim.vector.SingleValueHolder;
import peersim.cdsim.CDProtocol;

/**
 * Every junction in the road mesh carries one of these. The value it holds
 * is a locally sensed occupancy reading (fraction of approach-lane capacity
 * in use, 0..1). Once per cycle a junction samples a single neighbour from
 * its mesh view and the pair settle on their arithmetic mean -- a push-pull
 * epidemic average. Iterated across the whole mesh this drives every
 * junction's reading towards one shared number: the true, city-wide average
 * occupancy, discovered with no central traffic desk and no message beyond a
 * single neighbour contact per junction per round.
 *
 * The spread between the lowest and highest readings anywhere in the mesh is
 * the diagnostic to watch: it should collapse geometrically, cycle after
 * cycle, regardless of how many junctions the mesh contains.
 */
public class FlowGossipProtocol extends SingleValueHolder implements CDProtocol {

    public FlowGossipProtocol(String prefix) {
        super(prefix);
    }

    @Override
    public void nextCycle(Node owner, int pid) {
        int meshId = FastConfig.getLinkable(pid);
        Linkable mesh = (Linkable) owner.getProtocol(meshId);
        int reach = mesh.degree();
        if (reach == 0) {
            return;
        }

        Node partner = mesh.getNeighbor(CommonState.r.nextInt(reach));
        if (!partner.isUp()) {
            return; // partner currently disrupted (see DisruptionInjector)
        }

        FlowGossipProtocol partnerState = (FlowGossipProtocol) partner.getProtocol(pid);
        double settled = (this.value + partnerState.value) / 2.0;
        this.value = settled;
        partnerState.value = settled;
    }
}
