# Module 1: Graph Builder

## Purpose
This module focuses on constructing a graph data structure that represents relationships between entities such as cities and roads.

The output of this module will be reused by later modules, so the design emphasizes:
- Clean interfaces
- Correct structure
- Proper error handling

At this stage, the module is limited to **graph creation and representation only**.

---

## Graph Concept
A graph is a non-linear data structure composed of:
- **Nodes (vertices):** represent entities such as cities or locations
- **Edges:** represent connections between nodes
- **Weights:** numerical values associated with edges (e.g., distance or cost)

Graphs are commonly used in:
- Map and navigation systems
- Transportation networks
- Relationship modeling

---

## Graphs in a Map Context
When modeling a map:
- Nodes represent locations, intersections, or points of interest
- Edges represent roads or paths connecting locations
- Weights represent distance, travel time, or other costs

Although real GPS systems may use different graph types, this project models the map using a **weighted, directed graph**, allowing for one-way roads and asymmetric travel costs.

---

## Graph Class Design

### Internal Data Structure
The graph is implemented using a dictionary-based adjacency list.

Conceptually:
- Each node is a key in the dictionary
- The value stores that node’s neighboring nodes and their edge weights

This representation supports efficient insertion, deletion, and traversal.

---

## Core Graph Methods

### Add Node
Registers a new node in the graph.

**Logic:**
- Check if the node already exists
- If it does not exist, add it to the dictionary
- Initialize its neighbors as an empty collection

---

### Add Edge (u, v)
Creates a directed connection from node `u` to node `v`.

**Logic:**
- Access node `u` in the dictionary
- Add `v` to `u`’s list of neighbors
- Assign a weight to the edge

---

### Remove Edge (u, v)
Removes the connection between two nodes.

**Logic:**
- Locate `u`’s neighbor collection
- Remove `v` if it exists

---

### Remove Node
Deletes a node entirely from the graph.

**Logic:**
- Remove the node’s key from the dictionary
- Iterate through all remaining nodes
- Remove the deleted node from their neighbor lists

---

## Adjacency List Output

### `to_adjacency_list()`
Exports the graph in a structured adjacency-list format for display or reuse.

**Design approach:**
- Create a new output container to avoid modifying the original graph
- Iterate through all nodes
- Transform neighbor collections into a printable format
- Map each node to its formatted neighbors
- Return the completed structure

This ensures a clean, readable representation of the graph’s connections.

---

## Parsing Structured Input Files
The graph is built by parsing a structured `.txt` input file.

### Parsing Logic
- Open the file using `open()`
- Read the file line by line
- Strip whitespace and skip empty lines
- Identify sections (e.g., nodes and edges)
- Validate input format and data types
- Convert valid entries into graph operations

The parser acts as a bridge between raw text data and graph construction.

---

## Error Handling
The system includes validation and error handling to:
- Detect malformed input
- Prevent invalid nodes or edges
- Avoid runtime crashes
- Provide meaningful error messages

---

## Interface and Design Principles
- **Encapsulation:** Graph internals are hidden behind class methods
- **Clear interfaces:** Future modules interact only through defined functions
- **Stable data types:** Nodes, edges, and weights use consistent data structures
- **Return values:** Methods return well-defined outputs or updated structures
