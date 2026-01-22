srcfile = "input1.txt"
class Graph:

    _nodes: dict

    def __init__(self):
        
        self._nodes: dict = {}

    def add_node(self, node: str) -> None:

        if not node in self._nodes.keys():
            self._nodes.setdefault(node, {})

    def add_edge(self, node_src: str, node_dst: str, cost: int) -> None:

        if node_src == node_dst:
            return

        if not node_src in self._nodes.keys():
            self.add_node(node_src)

        if not node_dst in self._nodes.keys():
            self.add_node(node_dst)

        self._nodes[node_src][node_dst] = cost

    def remove_node(self, node: str) -> None:

        if not node in self._nodes.keys():
            return
        
        for key in self._nodes.keys():
            if node in self._nodes[key]:
                self._nodes[key].pop(node)
        
        self._nodes.pop(node)

    def remove_edge(self, src_node: str, node: str):

        if not src_node in self._nodes.keys():
            return
        
        if not node in self._nodes[src_node].keys():
            return
        
        self._nodes[src_node].pop(node)

    def _adjacency_list(self):

        for nodeKeys in self._nodes.keys():
            txt: str = f"{nodeKeys}: "
            nodedict: dict = self._nodes[nodeKeys]

            for pair in nodedict.items():
                txt += f"{pair[0]}({pair[1]}) "
            
            print(f"{txt}")

    def update_cost(self, src_node: str, dst_node: str, cost: int) -> None:
        self.add_edge(src_node, dst_node, cost)

    def get_adjacent_nodes(self, node: str) -> dict:
        if not node in self._nodes:
            return {}
        return self._nodes[node]
    
    def get_cost(self, src_node: str, dst_node: str) -> int:
        
        if not src_node in self._nodes:
            return -1
        
        # If dst_node in the src_node dict, then dst_node must be stored in the _nodes dict.
        # Which means, we are eliminating the cond: if not dst_node in self._nodes
        if not dst_node in self._nodes[src_node]:
            return -1
        
        return self._nodes[src_node][dst_node]


def load_file(srcfile: str) -> Graph:
    new_graph = Graph()

    with open(srcfile, "r") as file:
        for line in file:
        
            if line.startswith('CITIES'):
                for line in file: 
                    
                    if line.startswith('ROADS'):
                        return 
                    
                    print(f"{line}", end=" ")
                    
    return new_graph

if __name__ == "__main__":
    print("Hello world")

    area = Graph()

    # Update 2; added remove_edge:

    area.add_node("City1")
    area.add_node("City2")
    area.add_node("City3")

    area.add_edge("City1", "City2", 4)
    area.add_edge("City2", "City3", 8)

    print(f"{area._nodes}")

    print(f"\nBefore removing City2 from City1:")
    area._adjacency_list()

    area.remove_edge("City1", "City2")
    area.update_cost("City2", "City3", 40)


    print(f"\nAfter removing City2 from City1:")
    area._adjacency_list()

    print(f"{area.get_cost('City3', 'City1')}")

    area.remove_node("City2")

    print(f"\nAfter removing City2")
    area._adjacency_list()

    load_file(srcfile)