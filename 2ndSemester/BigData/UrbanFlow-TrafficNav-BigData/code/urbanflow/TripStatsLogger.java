/*
 * Big Data coursework (EME0650) - Use case #17: Traffic Navigation
 * Package: urbanflow
 */
package urbanflow;

import peersim.core.CommonState;
import peersim.core.Control;

/**
 * Prints one line per cycle summarising the trip agents dispatched by
 * {@link TripAgentDispatcher}:
 *
 * <pre>triplog| tick dispatched arrived stranded diverted divertShare avgHops</pre>
 */
public class TripStatsLogger implements Control {

    private final String tag;

    public TripStatsLogger(String tag) {
        this.tag = tag;
    }

    @Override
    public boolean execute() {
        long tick = CommonState.getTime();
        long arrived = TripAgentDispatcher.arrived;
        double divertShare = arrived == 0 ? 0.0 : (double) TripAgentDispatcher.diverted / arrived;
        double avgHops = arrived == 0 ? 0.0 : (double) TripAgentDispatcher.hopsOnArrival / arrived;

        System.out.println(tag + "| " + tick
                + " " + TripAgentDispatcher.dispatched
                + " " + arrived
                + " " + TripAgentDispatcher.stranded
                + " " + TripAgentDispatcher.diverted
                + " " + divertShare
                + " " + avgHops);
        return false;
    }
}
