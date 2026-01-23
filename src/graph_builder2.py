import sys

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
            count: int = 0
            size: int = len(nodedict)
            for pair in nodedict.items():
                count+=1
                txt+= f"{pair[0]}({pair[1]})"
                txt = (txt + ", ") if (count < size) else (txt + " ")
            print(f"{txt}")
           
    def get_adjacent_nodes(self, node: str) -> dict:
        if not node in self._nodes:
            return {}
        return self._nodes[node]
   
    def get_cost(self, src_node: str, dst_node: str) -> int:
        if not src_node in self._nodes:
            return -1
        if not dst_node in self._nodes[src_node]:
            return -1
        return self._nodes[src_node][dst_node]
   
    def set_cost(self, src_node: str, dst_node: str, cost: int) -> None:
        if not src_node in self._nodes.keys():
            raise ValueError(f"{src_node} is not created.")
        if not dst_node in self._nodes:
            raise ValueError(f"{dst_node} is not created.")
        if not dst_node in self._nodes[src_node]:
            raise ValueError(f"{dst_node} is not adjacent to {src_node}.")
        self._nodes[src_node][dst_node] = cost

def load_file(srcfile: str) -> Graph:
    new_graph = Graph()

    try:
        file = open(srcfile, "r")
    except:
        raise FileNotFoundError(f"File {srcfile} isn't found.")
   
    # Update 7; Added parser. We assume that the input file contains the following keywords:
    # "ROADS" and "CITIES"
    # City nodes created are under 'CITIES'
    # Roads (edges) are created under 'ROADS'
   
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

def main(argv: list) -> None:

    if len(argv) != 2:
        print(f"Invalid. Command usage: python {argv[0]} <src file>")
        return
   
    city_graph: Graph = load_file(argv[1])
    city_graph._adjacency_list()

# Update 5; argument pass
if __name__ == "__main__":
    main(sys.argv)