#!/usr/bin/env bash
# =====================================================================
#  Big Data coursework (EME0650) - Use case #17: Traffic Navigation
#  Builds the urbanflow package and runs the three scenarios, capturing
#  one results file per run under results/. Requires a JDK (javac) on
#  PATH - tested with JDK 17 and 21.
#
#  Usage:
#    ./execute_experiments.sh              # all three scenarios
#    JAVA_HOME=/path/to/jdk ./execute_experiments.sh
# =====================================================================
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

JAVAC_BIN="${JAVAC_BIN:-javac}"
JAVA_BIN="${JAVA_BIN:-java}"

TP="thirdparty"
CP="workspace:${TP}/peersim-1.0.5.jar:${TP}/jep-2.3.0.jar:${TP}/djep-1.0.0.jar"

mkdir -p workspace results

echo ">> [1/4] compiling code/urbanflow ..."
"$JAVAC_BIN" -cp "$CP" -d workspace code/urbanflow/*.java

# capture <tag>| rows from a peersim run into results/<file>
capture() {
  local tag="$1" cfgfile="$2" outfile="$3"; shift 3
  "$JAVA_BIN" -Xmx2g -cp "$CP" peersim.Simulator "$cfgfile" "$@" 2>/dev/null \
    | grep "^${tag}| " | sed "s/^${tag}| //" >> "$outfile"
}

echo ">> [2/4] scenario 1 - flow sensing across mesh sizes ..."
for N in 1200 12000 120000; do
  f="results/flowsense_${N}.dat"
  echo "tick lo hi live mean spread devi" > "$f"
  capture log scenarios/scenario1-flow-sensing.cfg "$f" network.size=$N
done

echo ">> [3/4] scenario 2 - adaptive rerouting across mesh sizes ..."
for N in 1200 12000 120000; do
  fm="results/meshload_${N}.dat"
  ft="results/tripflow_${N}.dat"
  echo "tick openCount fleetSize meanLoad peakLoad lockups overCapShare" > "$fm"
  capture meshlog scenarios/scenario2-adaptive-routing.cfg "$fm" network.size=$N
  echo "tick dispatched arrived stranded diverted divertShare avgHops" > "$ft"
  capture triplog scenarios/scenario2-adaptive-routing.cfg "$ft" network.size=$N
done

echo ">> [4/4] scenario 3 - disruption resilience across disruption rates ..."
for R in 0.01 0.02 0.05 0.10 0.20; do
  f="results/disruption_${R}.dat"
  echo "tick lo hi live mean spread devi" > "$f"
  capture log scenarios/scenario3-disruption-resilience.cfg "$f" control.disrupt.disruptionRate=$R
done

echo ">> done. Rendering charts ..."
python3 plots.py
echo ">> charts written to plots/."
