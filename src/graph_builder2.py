class Graph:

    _nodes: dict

    def __init__(self):
        
        self._nodes: dict = {}

    def add_node(self, node: str) -> None:

        if not node in self._nodes.keys():
            self._nodes.setdefault(node, {})

    def add_edge(self, node_src: str, node_dst: str, cost: int) -> None:

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


def load_file(srcfile: str) -> Graph:
    new_graph = Graph()

    return new_graph




if __name__ == "__main__":
    print("Hello world")

    area = Graph()

    # Update 1; added add_node, add_edge, adjacency_list

    # area.add_node("City1")
    # area.add_node("City2")
    # area.add_node("City3")
    # area.add_node("City4")

    # area.add_edge("City1", "City2", 4)
    # area.add_edge("City1", "City4", 10)
    # area.add_edge("City3", "City1", 5)
    # area.add_edge("City2", "City3", 2)
    # area.add_edge("City1", "City4", 15)

    # Update 2; added remove_edge:

    # area.add_node("City1")
    # area.add_node("City2")
    # area.add_node("City3")

    # area.add_edge("City1", "City2", 4)
    # area.add_edge("City2", "City3", 8)

    # print(f"{area._nodes}")

    # print(f"\nBefore removing City2 from City1:")
    # area._adjacency_list()

    

    # # area.remove_edge("City1", "City2")
    # area.update_cost("City2", "City3", 40)


    # print(f"\nAfter removing City2 from City1:")
    # area._adjacency_list()

    # Update 3; added remove_node:

    area.add_node("City1")
    area.add_node("City2")
    area.add_node("City3")

    area.add_edge("City1", "City2", 4)
    area.add_edge("City2", "City3", 8)
    area.add_edge("City3", "City2", 2)
    area.add_edge("City3", "City1", 14)

    print(f"\nBefore removing City2")
    area._adjacency_list()

    area.remove_node("City2")

    print(f"\nAfter removing City2")
    area._adjacency_list()