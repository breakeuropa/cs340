import sys

# Jo Update 1: Minimal Heap

class MinHeap:
    def __init__(self):
        self.data = []

    def is_empty(self):
        return len(self.data) == 0
    
    #push item into heap array
    def push(self, item):
        self.data.append(item)
        self._bubble_up(len(self.data) - 1)

    #remove from array
    def pop(self):
        if self.is_empty():
            return None
        
        #swap root with the last item
        self._swap(0, len(self.data) - 1)
        #remove the smallest
        item = self.data.pop()
        #fix the heap order
        self._bubble_down(0)
        return item
    
# GeeksForGeeks: Min Heap Representation as an Array
# The root element is stored at Arr[0].
# For any i-th node (at Arr[i]):
#       Parent Node → Arr[(i - 1) / 2]
#       Left Child → Arr[(2 * i) + 1]
#       Right Child → Arr[(2 * i) + 2]

    def _bubble_up(self, index):
        parent = (index - 1) // 2 #formula for finding the parent, // is for integer division (no remainder)
        #if we're not at the root node AND the current cost is < the parent cost
        if index > 0 and self.data[index][0] < self.data[parent][0]:
            #then swap the child (currrent) and parent
            self._swap(index, parent)
            #fix the heap
            self._bubble_up(parent)

    def _bubble_down(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index #assuming the current node is the smallest

        #if left exists and is less than the current smallest
        if left < len(self.data) and self.data[left][0] < self.data[smallest][0]:
            smallest = left

        #if right is smaller
        if right < len(self.data) and self.data[right][0] < self.data[smallest][0]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._bubble_down(smallest)

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

# Update 2: Hashmaps w/ chaining 
# Update 3: +remove_value()

# (2/4/26 - 6:53am): If prof asked us to turn this into an undirected graph, we might need to change
# the graph class a bit. Possible solution: For example, instead of having each city containing its
# own dictionary, we will remove this and the main list will probably be a tuple or something

class HashMap:

    # We want to initalize the size so % operator won't be a problem.
    def __init__(self, size):
        self._size: int = size
        self._list: list = [[] for _ in range(size)]

    def hash_function(self, key: str) -> int:
        value: int = 0
        for char in key:
            value = (value * 31 + ord(char)) % self._size
        return value

# Jo Update 3 or 4 idk: if not key in bucket: doesnt account for tuples so set and remove values are updated to account for that :)
    def set_value(self, key: str, value: int) -> None:
        index: int = self.hash_function(key)
        bucket: list = self._list[index]
        
        key_exists = any(k == key for k, v in bucket)

        if not key_exists:
            bucket.append((key, value))
            return
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                break
            
    def remove_value(self, key: str) -> None:
        index: int = self.hash_function(key)
        bucket: list = self._list[index]
        
        #remove the tuple with matching key
        bucket[:] = [(k, v) for k, v in bucket if k != key]

    def get_value(self, key: str) -> int:
        index: int = self.hash_function(key)
        bucket: list = self._list[index]

        for i, (k, v) in enumerate(bucket):
            if key == k:
                return v
        return -1


class Graph:

    #create "_nodes" attribute which is a dictionary
    _nodes: dict

    #initialize empty dictionary
    def __init__(self):
        self._nodes: dict = {}

    #Add city to the graph  
    def add_node(self, node: str) -> None:
        #Check if city is already in graph
        if not node in self._nodes.keys():
            #add with empty list
            self._nodes.setdefault(node, {})

    #Add road between two cities
    def add_edge(self, node_src: str, node_dst: str, cost: int) -> None:
        #Check if both cities are in the graph
        if node_src == node_dst:
            return
        #Check if source (first) city is in list
        if not node_src in self._nodes.keys():
            self.add_node(node_src)
        #Check if destination (second) city is in list
        if not node_dst in self._nodes.keys():
            self.add_node(node_dst)

        #Calculate cost based on source and destination
        self._nodes[node_src][node_dst] = cost

    #Remove city from graph
    def remove_node(self, node: str) -> None:
        #Check if city exists
        if not node in self._nodes.keys():
            return
        #Cycle through each instance of the city and "delete" it from the list
        for key in self._nodes.keys():
            if node in self._nodes[key]:
                self._nodes[key].pop(node)
        #remove the city
        self._nodes.pop(node)

    #Remove road from graph
    def remove_edge(self, src_node: str, node: str):
        #Check if road exists
        if not src_node in self._nodes.keys():
            return
        #Check if road connects to city
        if not node in self._nodes[src_node].keys():
            return
        #Remove road
        self._nodes[src_node].pop(node)

    #Convert to Adjacendy List
    def _adjacency_list(self):
        #Print the Graph
        for nodeKeys in self._nodes.keys():
            txt: str = f"{nodeKeys}: "
            nodedict: dict = self._nodes[nodeKeys]
            count: int = 0
            size: int = len(nodedict)
            #Format output
            for pair in nodedict.items():
                count+=1
                txt+= f"{pair[0]}({pair[1]})"
                txt = (txt + ", ") if (count < size) else (txt + " ")
            print(f"{txt}")
           
    #Return adjacent nodes      
    def get_adjacent_nodes(self, node: str) -> dict:
        if not node in self._nodes:
            return {}
        return self._nodes[node]
   
   #Return cost
    def get_cost(self, src_node: str, dst_node: str) -> int:
        if not src_node in self._nodes:
            return -1
        if not dst_node in self._nodes[src_node]:
            return -1
        return self._nodes[src_node][dst_node]
   
   #Change cost between cities
    def set_cost(self, src_node: str, dst_node: str, cost: int) -> None:
        #Check if cities and roads exist
        if not src_node in self._nodes.keys():
            raise ValueError(f"{src_node} is not created.")
        if not dst_node in self._nodes:
            raise ValueError(f"{dst_node} is not created.")
        if not dst_node in self._nodes[src_node]:
            raise ValueError(f"{dst_node} is not adjacent to {src_node}.")
        #Calculate cost
        self._nodes[src_node][dst_node] = cost

    def has_edge(self, src_node: str, dst_node: str) -> bool:
        return dst_node in self._nodes[src_node]
    
    def contains(self, node: str) -> bool:
        return node in self._nodes

def load_cities_file(srcfile: str) -> Graph:
    new_graph = Graph()

    try:
        file = open(srcfile, "r")
    except:
        raise FileNotFoundError(f"File {srcfile} isn't found.")
   
    keys = {"ROADS", "CITIES"}
    selected_key: str = "None"
   
    for line in file:
        txt: str = line.rstrip()
       
        if txt in keys:
            selected_key = txt
           
        if selected_key == "CITIES" and txt != selected_key:
            new_graph.add_node(txt)
       
        elif selected_key == "ROADS" and txt != selected_key:
           
            values: list = txt.split(' ')
            src_node: str = values[0]
            dst_node: str = values[1]
           
            try: cost: int = int(values[2])
            except: cost = 999 # Default cost if it is not properly defined.
           
            new_graph.add_edge(src_node, dst_node, cost)
           
    return new_graph

def load_query_file(srcfile: str, data: Graph) -> None:

    try:
        file = open(srcfile, "r")
    except:
        raise FileNotFoundError(f"File {srcfile} isn't found.")
    
    for line in file:
        values: list = line.rstrip().split(' ')

        if values[0] == "TRAFFIC_REPORT":
            
            src_node: str = values[1]
            dst_node: str = values[2]
            try: cost: int = int(values[3])
            except: cost = 999

            # Handle traffic reports
            if not data.has_edge(src_node, dst_node):
                # If edge doesn't exist, create it with the cost change
                # If cost is negative, set to 0
                cost = max(0, cost)
                data.add_edge(src_node, dst_node, cost)
            else:
                # Update existing edge
                edge_cost: int = data.get_cost(src_node, dst_node)
                new_cost = max(0, edge_cost + cost)  # Ensure cost doesn't go negative
                data.set_cost(src_node, dst_node, new_cost)

        elif values[0] == "QUERY" and values[1] == "SHORTEST_PATH":
            start = values[2]
            end = values[3]
            path, cost = dijkstra(data, start, end)

            if path is None or cost == float('inf'):
                print(f"SHORTEST_PATH {start} {end}: No path available")
            else:
                path_str = " -> ".join(path)
                print(f"SHORTEST_PATH {start} {end}: {path_str} (cost: {int(cost)})")

        elif values[0] == "QUERY" and values[1] == "K_PATHS":
            start = values[2]
            end = values[3]
            k = int(values[4])
            
            paths = k_shortest_paths(data, start, end, k)
            
            if not paths:
                print(f"K_PATHS {start} {end}: No paths available")
            else:
                print(f"K_PATHS {start} {end}:")
                for idx, (path, cost) in enumerate(paths, 1):
                    path_str = " -> ".join(path)
                    print(f"{idx}) {path_str} ({int(cost)})")

#Jo Update 2: Dijkstra
def dijkstra(graph: Graph, start: str, end: str):
    dist = {node: float('inf') for node in graph._nodes}
    dist[start] = 0 #beginning node set to 0 so we always start here :)

    prev = {} #parent table, how we will rebuild the path

    heap = MinHeap()
    heap.push((0, start)) #add the beginning to the heap: (cost so far, city)

    #stops if we find the shortest path or all reachabe nodes are visited
    while not heap.is_empty():
        #pop the cheapest unvisited node so far
        current_cost, current_node = heap.pop()

        #if current distance(cost) is not the latest shortest one, skip it
        if current_cost > dist[current_node]:
            continue

        #if we're at the end, dont keep going, we found the shortest path
        if current_node == end:
            break

        #explore neighbors of current vertex
        for neighbor, weight in graph.get_adjacent_nodes(current_node).items():
            new_cost = current_cost + weight

            #if we found a shorter path, update it
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                prev[neighbor] = current_node
                heap.push((new_cost, neighbor))
        
    #if the graph is disconnected or unreachable
    if start != end and end not in prev:
        return None, float('inf')
        
    path = [] #list of cities
    node = end
    while node != start:
        path.append(node)
        node = prev[node]
    path.append(start)
    path.reverse()

    return path, dist[end]

#The function below is for the kpath implementation
def k_shortest_paths(graph: Graph, start: str, end: str, k: int):
    """Find k shortest paths using iterative Dijkstra approach"""
    all_paths = []
    
    # Create a modified graph for each iteration
    temp_graph_edges = {}  # Store removed edges
    
    for i in range(k):
        # Find shortest path in current graph state
        path, cost = dijkstra(graph, start, end)
        
        if path is None or cost == float('inf'):
            break  # No more paths available
        
        all_paths.append((path, cost))
        
        # If we found k paths, stop
        if len(all_paths) >= k:
            break
        
        # Remove edges from this path to find alternative routes
        # Store them so we can restore later if needed
        for j in range(len(path) - 1):
            src = path[j]
            dst = path[j + 1]
            
            if graph.has_edge(src, dst):
                # Store the edge for potential restoration
                edge_key = (src, dst)
                if edge_key not in temp_graph_edges:
                    temp_graph_edges[edge_key] = graph.get_cost(src, dst)
                
                # Temporarily remove the edge
                graph.remove_edge(src, dst)
    
    # Restore all removed edges
    for (src, dst), cost in temp_graph_edges.items():
        graph.add_edge(src, dst, cost)
    
    return all_paths

def main(argv: list) -> None:

    if len(argv) != 3:
        print(f"Invalid. Command usage: python {argv[0]} <city file> <query file>")
        return
   
    city_graph: Graph = load_cities_file(argv[1])
    load_query_file(argv[2], city_graph)

# Update 5; argument pass
if __name__ == "__main__":
    main(sys.argv)