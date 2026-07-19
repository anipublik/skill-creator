#!/usr/bin/env python3
"""
validate_graph.py

Validates a JSON graph spec against the checks GRAPH.md Phase 3 and 5 require:
  - exactly one declared entry node
  - every node reachable from the entry node
  - every node can reach at least one terminal node (no dead-end sinks)
  - every cycle has a max_iterations budget on at least one edge in the cycle

Input: a JSON file shaped like:

{
  "entry": "plan",
  "nodes": ["plan", "execute", "evaluate", "escalate", "done"],
  "edges": [
    {"from": "plan", "to": "execute"},
    {"from": "execute", "to": "evaluate"},
    {"from": "evaluate", "to": "done", "condition": "success"},
    {"from": "evaluate", "to": "plan", "condition": "retry", "cycle": true, "max_iterations": 5},
    {"from": "evaluate", "to": "escalate", "condition": "exhausted"}
  ],
  "terminal_nodes": ["done", "escalate"]
}

Usage:
  python3 validate_graph.py path/to/graph.json

Exit code 0 if the spec passes all checks, 1 if any check fails, with
findings printed to stdout either way. This script only checks topology.
It does not and cannot validate that your routing conditions or node
contracts are semantically correct - do that by hand, per GRAPH.md Phase 5.
"""

import sys
import json
from collections import defaultdict


def load_spec(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: no file found at '{path}'.")
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: '{path}' is not valid JSON ({e.msg} at line {e.lineno}, column {e.colno}).")
        sys.exit(2)


def build_adjacency(edges):
    adj = defaultdict(list)
    for e in edges:
        adj[e["from"]].append(e)
    return adj


def find_reachable(entry, adj):
    seen = set()
    stack = [entry]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        for e in adj.get(n, []):
            if e["to"] not in seen:
                stack.append(e["to"])
    return seen


def find_reverse_reachable(terminal_nodes, edges):
    rev_adj = defaultdict(list)
    for e in edges:
        rev_adj[e["to"]].append(e["from"])
    seen = set()
    stack = list(terminal_nodes)
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        for src in rev_adj.get(n, []):
            if src not in seen:
                stack.append(src)
    return seen


def find_cycles(nodes, adj):
    """Returns a list of cycles, each a list of edges forming the actual
    cycle, via DFS back-edge detection. When a back edge to node v is found,
    the true cycle is only the suffix of the current DFS path starting at v
    - not the full path from the DFS root - so a budgeted edge earlier in
    the path (outside the real cycle) can't be mistaken for covering it.
    Not exhaustive for every cycle in densely connected graphs, but catches
    every node that participates in at least one cycle, which is what the
    budget check needs."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}
    cycles = []

    def dfs(u, stack_nodes, stack_edges):
        color[u] = GRAY
        stack_nodes.append(u)
        for e in adj.get(u, []):
            v = e["to"]
            if v not in color:
                continue
            if color[v] == GRAY:
                idx = stack_nodes.index(v)
                cycles.append(stack_edges[idx:] + [e])
            elif color[v] == WHITE:
                dfs(v, stack_nodes, stack_edges + [e])
        color[u] = BLACK
        stack_nodes.pop()

    for n in nodes:
        if color.get(n) == WHITE:
            dfs(n, [], [])
    return cycles


def validate(spec):
    findings = []
    ok = True

    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    entry = spec.get("entry")
    terminal_nodes = spec.get("terminal_nodes", [])

    # Every edge must be shaped like an edge before anything else touches it.
    malformed = [e for e in edges if "from" not in e or "to" not in e]
    if malformed:
        findings.append(f"FAIL: {len(malformed)} edge(s) missing a required "
                         f"'from' or 'to' field: {malformed}")
        return False, findings

    if not entry:
        findings.append("FAIL: no entry node declared.")
        ok = False
    elif entry not in nodes:
        findings.append(f"FAIL: entry node '{entry}' is not in the node list.")
        ok = False

    if not terminal_nodes:
        findings.append("FAIL: no terminal nodes declared. A graph with no terminal "
                         "node can never be said to have finished a run.")
        ok = False

    adj = build_adjacency(edges)

    # Every edge must reference declared nodes - a typo'd node name in an
    # edge should never silently vanish and get reported as a pass.
    node_set = set(nodes)
    phantom_refs = []
    for e in edges:
        if e["from"] not in node_set:
            phantom_refs.append(f"edge {e['from']!r} -> {e['to']!r}: "
                                 f"'from' node {e['from']!r} is not in the declared node list")
        if e["to"] not in node_set:
            phantom_refs.append(f"edge {e['from']!r} -> {e['to']!r}: "
                                 f"'to' node {e['to']!r} is not in the declared node list")
    if phantom_refs:
        findings.append(f"FAIL: {len(phantom_refs)} edge(s) reference undeclared nodes:")
        for p in phantom_refs:
            findings.append(f"   {p}")
        ok = False
    else:
        findings.append("PASS: every edge references a declared node.")

    # Reachability from entry
    if entry:
        reachable = find_reachable(entry, adj)
        unreachable = set(nodes) - reachable
        if unreachable:
            findings.append(f"FAIL: nodes unreachable from entry: {sorted(unreachable)}")
            ok = False
        else:
            findings.append("PASS: every node is reachable from the entry node.")

    # Every node can reach a terminal node (no dead-end sinks)
    if terminal_nodes:
        can_reach_terminal = find_reverse_reachable(terminal_nodes, edges)
        dead_ends = set(nodes) - can_reach_terminal - set(terminal_nodes)
        if dead_ends:
            findings.append(f"FAIL: nodes that can never reach a terminal node "
                             f"(dead-end sinks with no exit path): {sorted(dead_ends)}")
            ok = False
        else:
            findings.append("PASS: every node can reach a terminal node.")

    # Cycle budget check
    cycles = find_cycles(nodes, adj)
    if not cycles:
        findings.append("INFO: no cycles detected. Skip cycle budget checks.")
    else:
        budgeted = []
        unbudgeted = []
        for cyc in cycles:
            path = " -> ".join(e["from"] for e in cyc) + f" -> {cyc[-1]['to']}"
            has_budget = any(e.get("cycle") and "max_iterations" in e for e in cyc)
            (budgeted if has_budget else unbudgeted).append(path)

        findings.append(f"INFO: {len(cycles)} cycle(s) detected total "
                         f"({len(budgeted)} budgeted, {len(unbudgeted)} unbudgeted).")
        for p in budgeted:
            findings.append(f"   OK (budgeted): {p}")

        if unbudgeted:
            findings.append(f"FAIL: {len(unbudgeted)} cycle(s) with no max_iterations "
                             f"budget on any edge in the cycle:")
            for p in unbudgeted:
                findings.append(f"   {p}")
            findings.append("   Every cycle-back edge needs 'cycle: true' and "
                             "'max_iterations: N'. See GRAPH.md Phase 3, cycle budgets.")
            ok = False
        else:
            findings.append(f"PASS: all {len(cycles)} detected cycle(s) have an "
                             f"iteration budget on at least one edge.")

    return ok, findings


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate_graph.py path/to/graph.json")
        sys.exit(2)

    spec = load_spec(sys.argv[1])
    ok, findings = validate(spec)

    print(f"Validating: {sys.argv[1]}\n")
    for line in findings:
        print(line)
    print()
    print("RESULT: PASS" if ok else "RESULT: FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
