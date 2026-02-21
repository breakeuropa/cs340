#Loads sys library
import sys
#Class name = graph
class Graph:
    #Constructor
    def __init__(self):
        #dictionary to hold the graph
        self.graph = {}
    #Add a city to the graph
    def add_node(self, city):
        #Check if city is not already in the graph
        if city not in self.graph:
            #If not, add it with an empty list of edges
            self.graph[city] = []
    #Add a road between two cities
    def add_edge(self, from_city, to_city, weight):
        #Check if both cities are in the graph
        if from_city not in self.graph:
            #If not, add it with an empty list of edges
            self.add_node(from_city)
            #self.graph[from_city] = []
        if to_city not in self.graph:
            #If not, add it with an empty list of edges
            self.add_node(to_city)
        #Add the edge
        self.graph[from_city].append((to_city, weight))
    #Remove a city from the graph
    def remove_node(self, city):
        #Check if city is in the graph
        if city in self.graph:
            #Remove all edges to this city
            del self.graph[city]
            #Remove all edges from other cities to this city
            for c in self.graph:
                self.graph[c] = [
                    (to, w) for to, w in self.graph[c] if to != city
                ]
    #Remove a road between two cities
    def remove_edge(self, from_city, to_city):
        #Check if both cities are in the graph
        if from_city in self.graph and to_city in self.graph:
            #Remove the edge
            self.graph[from_city] = [
                (to, w) for to, w in self.graph[from_city] if to != to_city
            ]
    #Convert the graph to an adjacency list
    def to_adjacency_list(self):
        #Print the adjacency list
        for city in self.graph:
            #Get the list of edges for this city
            edges = self.graph[city]
            #Check if there are any edges
            if edges:
                #If there are, create a string representation
                edge_str = ", ".join(f"{to}({w})" for to, w in edges)
                #Print the adjacency list
                print(f"{city}: {edge_str}")
            else:
                print(f"{city}:")

#Main function
def main():
    #Check if the correct number of arguments is provided
    if len(sys.argv) < 2:
        print("Usage: python3 graph_builder3.py input.txt")
        return
    #Get the filename
    filename = sys.argv[1]
    #Create a new graph
    graph = Graph()
    #Open the input file
    with open(filename, "r") as file:
        #Read the lines
        lines = [line.strip() for line in file if line.strip()]
    #Initialize the mode
    mode = None
    #Process each line
    for line in lines:
        if line == "CITIES":
            mode = "cities"
        elif line == "ROADS":
            mode = "roads"
        elif mode == "cities":
            graph.add_node(line)
        elif mode == "roads":
            parts = line.split()
            from_city = parts[0]
            to_city = parts[1]
            weight = int(parts[2])
            graph.add_edge(from_city, to_city, weight)
    #Convert the graph to an adjacency list
    graph.to_adjacency_list()

#Entry point
if __name__ == "__main__":
    main() 