# graph_query2.py  (Module 2: Traffic & Priority Query System - SHORTEST_PATH only)
# Usage: python3 graph_query2.py input1.txt commands2.txt

import sys
import heapq


class Graph:
    def __init__(self):
        # city -> list of (to_city, base_weight)
        self.graph = {}

    def add_node(self, city: str) -> None:
        if city not in self.graph:
            self.graph[city] = []

    def add_edge(self, from_city: str, to_city: str, weight: int) -> None:
        # Ensure nodes exist
        if from_city not in self.graph:
            self.add_node(from_city)
        if to_city not in self.graph:
            self.add_node(to_city)

        # Replace edge if it already exists (prevents duplicates)
        for i, (to, w) in enumerate(self.graph[from_city]):
            if to == to_city:
                self.graph[from_city][i] = (to_city, weight)
                return

        self.graph[from_city].append((to_city, weight))

    def neighbors(self, city: str):
        return self.graph.get(city, [])


def load_base_graph(filename: str) -> Graph:
    """
    Parses Module 1 input file format:

    CITIES
    City1
    City2
    ...
    ROADS
    City1 City2 5
    City2 City3 3
    ...
    """
    g = Graph()
    mode = None  # "cities" or "roads"

    with open(filename, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            if line == "CITIES":
                mode = "cities"
                continue
            if line == "ROADS":
                mode = "roads"
                continue

            if mode == "cities":
                g.add_node(line)

            elif mode == "roads":
                parts = line.split()
                if len(parts) != 3:
                    print(f"Warning: skipping bad road line: {line}")
                    continue
                u, v, w_str = parts
                try:
                    w = int(w_str)
                except ValueError:
                    print(f"Warning: skipping road with invalid weight: {line}")
                    continue
                g.add_edge(u, v, w)

            else:
                # Ignore any lines before CITIES/ROADS header
                continue

    return g


def dijkstra_shortest_path(graph: Graph, traffic_delta: dict, start: str, end: str):
    """
    traffic_delta[(u, v)] = delta to add to base weight (from TRAFFIC_REPORT lines)
    effective_weight = base_weight + delta
    """
    if start not in graph.graph or end not in graph.graph:
        return None, float("inf")

    dist = {node: float("inf") for node in graph.graph}
    prev = {}

    dist[start] = 0
    heap = [(0, start)]  # (cost, node)

    while heap:
        cur_cost, u = heapq.heappop(heap)

        # Skip stale heap entries
        if cur_cost != dist[u]:
            continue

        if u == end:
            break

        for v, base_w in graph.neighbors(u):
            delta = traffic_delta.get((u, v), 0)
            w = base_w + delta

            # Dijkstra assumes non-negative edge weights.
            # If traffic makes it negative, clamp to 0.
            if w < 0:
                w = 0

            new_cost = cur_cost + w
            if new_cost < dist[v]:
                dist[v] = new_cost
                prev[v] = u
                heapq.heappush(heap, (new_cost, v))

    # Unreachable
    if start != end and end not in prev:
        return None, float("inf")

    # Reconstruct path
    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()

    return path, dist[end]


def run_commands(commands_file: str, graph: Graph) -> None:
    """
    Processes commands2.txt lines of the form:
      TRAFFIC_REPORT City1 City2 +3
      QUERY SHORTEST_PATH City1 City4
    Ignores K_PATHS for now (per request).
    """
    traffic_delta = {}  # (u, v) -> cumulative delta

    with open(commands_file, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            parts = line.split()

            # TRAFFIC_REPORT <FROM> <TO> <DELTA>
            if parts[0] == "TRAFFIC_REPORT":
                if len(parts) != 4:
                    print(f"Warning: bad TRAFFIC_REPORT line: {line}")
                    continue
                u, v, d_str = parts[1], parts[2], parts[3]
                try:
                    delta = int(d_str)  # works for +3 and -2
                except ValueError:
                    print(f"Warning: bad delta in TRAFFIC_REPORT: {line}")
                    continue

                traffic_delta[(u, v)] = traffic_delta.get((u, v), 0) + delta

            # QUERY SHORTEST_PATH <FROM> <TO>
            elif parts[0] == "QUERY" and len(parts) >= 2 and parts[1] == "SHORTEST_PATH":
                if len(parts) != 4:
                    print(f"Warning: bad SHORTEST_PATH query: {line}")
                    continue

                start, end = parts[2], parts[3]
                path, cost = dijkstra_shortest_path(graph, traffic_delta, start, end)

                if path is None or cost == float("inf"):
                    print(f"SHORTEST_PATH {start} {end}: NO PATH")
                else:
                    path_str = " -> ".join(path)
                    print(f"SHORTEST_PATH {start} {end}: {path_str} (cost: {int(cost)})")

            else:
                # Ignore unsupported commands for now (e.g., K_PATHS)
                continue


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 graph_query2.py input1.txt commands2.txt")
        raise SystemExit(2)

    graph_file = sys.argv[1]
    commands_file = sys.argv[2]

    base_graph = load_base_graph(graph_file)
    run_commands(commands_file, base_graph)


if __name__ == "__main__":
    main()
