import sys

# Update 2: Hashmaps w/ chaining 

class HashMap:

    def __init__(self, size):
        self._size: int = size
        self._list: list = [[] for _ in range(size)]

    def hash_function(self, key: str) -> int:
        value: int = 0
        for char in key:
            value = (value * 31 + ord(char)) % self._size
        return value

    def set_value(self, key: str, value: int) -> None:
        index: int = self.hash_function(key)
        bucket: list = self._list[index]
        
        if not key in bucket:
            bucket.append((key, value))
            return
        
        for i, (k, v) in enumerate(bucket):
            bucket[i] = (key, value) if k == key else bucket[i]

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

            # Update 1: It seems like some roads from commands2.txt aren't defined in input1.txt
            if not data.has_edge(src_node, dst_node):
                print(f"{dst_node} isn't located in {src_node}, adding to graph obj...")
                data.add_edge(src_node, dst_node, cost)

            else:
                edge_cost: int = data.get_cost(src_node, dst_node)
                print(f"{dst_node} found in {src_node} {edge_cost}")
                data.set_cost(src_node, dst_node, edge_cost + cost)

        elif values[0] == "QUERY" and values[1] == "SHORTEST_PATH":
            pass

        else: # query -> k_paths
            pass

def main(argv: list) -> None:

    if len(argv) != 3:
        print(f"Invalid. Command usage: python {argv[0]} <city file> <query file>")
        return
   
    # city_graph: Graph = load_cities_file(argv[1])
    # load_query_file(argv[2], city_graph)
    # city_graph._adjacency_list()

    hash = HashMap(500)
    # print(f"{hash.hash_function('hello world')}")
    # print(f"{hash.hash_function('Hello world')}")
    # print(f"{hash.hash_function('cat')}")
    # print(f"{hash.hash_function('cta')}")
    # print(f"{hash.hash_function('tac')}")
    # print(f"{hash.hash_function('tca')}")
    # print(f"{hash.hash_function('act')}")
    # print(f"{hash.hash_function('atc')}")

    hash.append("test", 48)
    hash.append("sett", 72)
    hash.append("etst", 499)

    print(f"{hash.get_value('test')}")
    print(f"{hash.get_value('sett')}")
    print(f"{hash.get_value('etst')}")

# Update 5; argument pass
if __name__ == "__main__":
    main(sys.argv)