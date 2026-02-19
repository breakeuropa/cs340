# graph_schedule2.py  (Module 3 - Jo Style, Schedule Queue START)
# Implements:
#   - 
# Usage:
#   python3 graph_schdule2.py schedule3.txt 

import sys

#Update 2: BST for history thumbs up
class TreeNode:
    def __init__(self, city, time):
        self.left = None
        self.right = None
        self.city = city
        self.time = time

    def insert(root, time):
        if root is None:
            return TreeNode(time)
        if root.time == time:
            return root
        if root.time < time:
            root.right = insert(root.right, time)
        else:
            root.left = insert(root.left, time)
        return root

        


# ----------------------------
# Queue 
# ----------------------------
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, city, time):
        delivery = f"{city} at {time}"
        self.queue.append(delivery)
        return f"Scheduled: {delivery}"
    
    def dequeue(self):
        if not self.queue:
            return None
        return self.queue.pop(0)
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def print_queue(self):
        for item in self.queue:
            print(f"{item}")

# ----------------------------
# Min-Heap (for Dijkstra)
# ----------------------------
class MinHeap:
    def __init__(self):
        self.data = []

    def is_empty(self):
        return len(self.data) == 0

    def push(self, item):
        # item must be (cost, node)
        self.data.append(item)
        self._bubble_up(len(self.data) - 1)

    def pop(self):
        if self.is_empty():
            return None

        self._swap(0, len(self.data) - 1)
        item = self.data.pop()
        self._bubble_down(0)
        return item

    def _bubble_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.data[index][0] < self.data[parent][0]:
            self._swap(index, parent)
            self._bubble_up(parent)

    def _bubble_down(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < len(self.data) and self.data[left][0] < self.data[smallest][0]:
            smallest = left
        if right < len(self.data) and self.data[right][0] < self.data[smallest][0]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._bubble_down(smallest)

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]


# ----------------------------
# HashMap w/ chaining (FIXED)
# traffic_delta key format: "CityA|CityB"
# value: cumulative delta (+/-)
# ----------------------------
class HashMap:
    def __init__(self, size: int):
        self._size = size
        self._list = [[] for _ in range(size)]

    def hash_function(self, key: str) -> int:
        value = 0
        for char in key:
            value = (value * 31 + ord(char)) % self._size
        return value

    def set_value(self, key: str, value: int) -> None:
        index = self.hash_function(key)
        bucket = self._list[index]

        # Update existing
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Insert new
        bucket.append((key, value))

    def remove_value(self, key: str) -> None:
        index = self.hash_function(key)
        bucket = self._list[index]
        bucket[:] = [(k, v) for (k, v) in bucket if k != key]

    def get_value(self, key: str) -> int:
        index = self.hash_function(key)
        bucket = self._list[index]
        for (k, v) in bucket:
            if k == key:
                return v
        # For traffic deltas, default should be 0 (no traffic change)
        return 0


def edge_key(u: str, v: str) -> str:
    return f"{u}|{v}"


# ----------------------------
# Graph (team dict-of-dicts style)
# _nodes[src][dst] = base_cost
# ----------------------------
class Graph:
    def __init__(self):
        self._nodes = {}

    def add_node(self, node: str) -> None:
        if node not in self._nodes:
            self._nodes.setdefault(node, {})

    def add_edge(self, node_src: str, node_dst: str, cost: int) -> None:
        if node_src == node_dst:
            return
        if node_src not in self._nodes:
            self.add_node(node_src)
        if node_dst not in self._nodes:
            self.add_node(node_dst)
        self._nodes[node_src][node_dst] = cost

    def remove_node(self, node: str) -> None:
        if node not in self._nodes:
            return
        for key in list(self._nodes.keys()):
            if node in self._nodes[key]:
                self._nodes[key].pop(node)
        self._nodes.pop(node)

    def remove_edge(self, src_node: str, dst_node: str) -> None:
        if src_node not in self._nodes:
            return
        if dst_node not in self._nodes[src_node]:
            return
        self._nodes[src_node].pop(dst_node)

    def get_adjacent_nodes(self, node: str) -> dict:
        return self._nodes.get(node, {})

    def get_cost(self, src_node: str, dst_node: str) -> int:
        if src_node not in self._nodes:
            return -1
        if dst_node not in self._nodes[src_node]:
            return -1
        return self._nodes[src_node][dst_node]

    def set_cost(self, src_node: str, dst_node: str, cost: int) -> None:
        if src_node not in self._nodes:
            raise ValueError(f"{src_node} is not created.")
        if dst_node not in self._nodes:
            raise ValueError(f"{dst_node} is not created.")
        if dst_node not in self._nodes[src_node]:
            raise ValueError(f"{dst_node} is not adjacent to {src_node}.")
        self._nodes[src_node][dst_node] = cost

    def has_edge(self, src_node: str, dst_node: str) -> bool:
        return src_node in self._nodes and dst_node in self._nodes[src_node]

    def contains(self, node: str) -> bool:
        return node in self._nodes

    def to_adjacency_list(self) -> str:
        lines = []
        for src in self._nodes.keys():
            nodedict = self._nodes[src]
            parts = [f"{dst}({cost})" for dst, cost in nodedict.items()]
            lines.append(f"{src}: " + ", ".join(parts) if parts else f"{src}:")
        return "\n".join(lines)


# ----------------------------
# Module 1 file parser
# ----------------------------
def load_cities_file(srcfile: str) -> Graph:
    new_graph = Graph()

    try:
        with open(srcfile, "r") as file:
            keys = {"ROADS", "CITIES"}
            selected_key = None

            for line in file:
                txt = line.strip()
                if not txt:
                    continue

                if txt in keys:
                    selected_key = txt
                    continue

                if selected_key == "CITIES":
                    new_graph.add_node(txt)

                elif selected_key == "ROADS":
                    values = txt.split()  # safe for multiple spaces
                    if len(values) != 3:
                        # skip malformed line
                        continue
                    src_node, dst_node, w_str = values
                    try:
                        cost = int(w_str)
                    except ValueError:
                        # skip bad weight
                        continue
                    new_graph.add_edge(src_node, dst_node, cost)

    except FileNotFoundError:
        raise FileNotFoundError(f"File {srcfile} isn't found.")

    return new_graph


# ----------------------------
# Dijkstra using base graph + traffic deltas (HashMap)
# effective_weight = base + delta
# ----------------------------
def dijkstra(graph: Graph, traffic: HashMap, start: str, end: str):
    if not graph.contains(start) or not graph.contains(end):
        return None, float("inf")

    dist = {node: float("inf") for node in graph._nodes}
    dist[start] = 0
    prev = {}

    heap = MinHeap()
    heap.push((0, start))

    while not heap.is_empty():
        popped = heap.pop()
        if popped is None:
            break

        current_cost, u = popped

        if current_cost != dist[u]:
            continue

        if u == end:
            break

        for v, base_w in graph.get_adjacent_nodes(u).items():
            delta = traffic.get_value(edge_key(u, v))
            w = base_w + delta

            if w < 0:
                w = 0

            new_cost = current_cost + w
            if new_cost < dist[v]:
                dist[v] = new_cost
                prev[v] = u
                heap.push((new_cost, v))

    if start != end and end not in prev:
        return None, float("inf")

    # rebuild path
    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()

    return path, dist[end]

def k_shortest_paths(graph: Graph, traffic: HashMap, start: str, end: str, k: int):
    """Find k shortest paths using iterative Dijkstra approach"""
    all_paths = []
    
    temp_graph_edges = {}  
    
    for i in range(k):
        # Find shortest path in current graph state
        path, cost = dijkstra(graph, traffic, start, end)
        
        if path is None or cost == float('inf'):
            break  # No more paths available
        
        all_paths.append((path, cost))
        
        if len(all_paths) >= k:
            break
        
        for j in range(len(path) - 1):
            src = path[j]
            dst = path[j + 1]
            
            if graph.has_edge(src, dst):
                edge_key = (src, dst)
                if edge_key not in temp_graph_edges:
                    temp_graph_edges[edge_key] = graph.get_cost(src, dst)
                
                graph.remove_edge(src, dst)
    
    for (src, dst), cost in temp_graph_edges.items():
        graph.add_edge(src, dst, cost)
    
    return all_paths

# ----------------------------
# commands2.txt parser
# ----------------------------
def load_query_file(srcfile: str, data: Graph) -> None:
    try:
        with open(srcfile, "r") as file:
            # Traffic map: edge -> delta
            traffic = HashMap(2003)  # prime-ish size helps reduce collisions

            for line in file:
                values = line.strip().split()  # safe split
                if not values:
                    continue

                # TRAFFIC_REPORT City1 City2 +3
                if values[0] == "TRAFFIC_REPORT":
                    if len(values) != 4:
                        continue
                    src_node = values[1]
                    dst_node = values[2]

                    try:
                        delta = int(values[3])  # +3 or -2
                    except ValueError:
                        continue

                    k = edge_key(src_node, dst_node)
                    current = traffic.get_value(k)
                    traffic.set_value(k, current + delta)

                # QUERY SHORTEST_PATH City1 City4
                elif values[0] == "QUERY" and len(values) >= 2 and values[1] == "SHORTEST_PATH":
                    if len(values) != 4:
                        continue
                    start = values[2]
                    end = values[3]

                    path, cost = dijkstra(data, traffic, start, end)

                    if path is None or cost == float("inf"):
                        print(f"SHORTEST_PATH {start} {end}: NO PATH")
                    else:
                        path_str = " -> ".join(path)
                        print(f"SHORTEST_PATH {start} {end}: {path_str} (cost: {int(cost)})")
                
                elif values[0] == "QUERY" and values[1] == "K_PATHS":
                    start = values[2]
                    end = values[3]
                    
                    try: k = int(values[4])
                    except ValueError: continue
                    
                    paths = k_shortest_paths(data, traffic, start, end, k)
                    
                    if not paths:
                        print(f"K_PATHS {start} {end}: No paths available")
                    else:
                        print(f"K_PATHS {start} {end}:")
                        for idx, (path, cost) in enumerate(paths, 1):
                            path_str = " -> ".join(path)
                            print(f"{idx}) {path_str} ({int(cost)})")

    except FileNotFoundError:
        raise FileNotFoundError(f"File {srcfile} isn't found.")

#Jo Update 1.2 Queue File Loader
def load_schedule_file(srcfile: str) -> None:
    try:
        with open(srcfile, "r") as file:
            delivery = Queue()
            print("Made Queue")

            for line in file:
                values = line.strip().split()  # safe split
                #print(f"values: {values}")
                if not values:
                    print("Line emoty")
                    continue
                
                # SCHEDULE DELIVERY City25->City0 at 09:00
                if values[0] == "SCHEDULE" and values[1] == "DELIVERY":
                    
                    if len(values) != 5:
                        continue
 
                    city: str = values[2]
                    time: str = values[4]

                    #print(f"city: {city} time: {time}")

                    print(f"{delivery.enqueue(city, time)}")
                
                if values[0] == "RECORD_HISTORY":
                    print("Dequeuing!")
                    print(f"{delivery.dequeue()}")
                    print("Current Queue: ")
                    delivery.print_queue()
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File {srcfile} isn't found.")

# def main():
#     print("Starting Main:")
#     q = Queue()
#     print(f"{q.enqueue("City1->City4", "09:00")}")
#     print(f"{q.enqueue("City1->City4", "09:10")}")
#     print(f"Current Queue: ")
#     q.print_queue()
#     print(f"Removed: {q.dequeue()}")
#     print(f"Current Queue: ")
#     q.print_queue()

# if __name__ == "__main__":
#     main()

def main(argv: list) -> None:
    if len(argv) != 2:
        print(f"Invalid. Command usage: python3 {argv[0]} <schedule file>")
        return
    
    #city_graph = load_cities_file(argv[1])
    #load_query_file(argv[2], city_graph)
    load_schedule_file(argv[1])


if __name__ == "__main__":
   main(sys.argv)