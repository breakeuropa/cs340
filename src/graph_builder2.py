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

    # def remove_node(self):
    #     pass

    # def remove_edge(self):
    #     pass

    def _adjacency_list(self):

        for nodeKeys in self._nodes.keys():
            txt: str = f"{nodeKeys}: "
            nodedict: dict = self._nodes[nodeKeys]

            for pair in nodedict.items():
                txt += f"{pair[0]}({pair[1]}) "
            
            print(f"{txt}")

if __name__ == "__main__":
    print("Hello world")

    area = Graph()

    area.add_node("City1")
    area.add_node("City2")
    area.add_node("City3")
    area.add_node("City4")

    area.add_edge("City1", "City2", 4)
    area.add_edge("City1", "City4", 10)
    area.add_edge("City3", "City1", 5)
    area.add_edge("City2", "City3", 2)

    print(f"{area._nodes}")

    area._adjacency_list()