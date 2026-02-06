# Module 2: Traffic & Priority Query System

## Goal
Module 2 simulates **live traffic** and supports routing queries on top of the graph built in Module 1.

Key outcomes:
- Dynamic edge weights (traffic updates) without rebuilding the graph
- `SHORTEST_PATH` using **Dijkstra + heap**
- `K_PATHS` for alternative routes using **iterative Dijkstra**
- Clear CLI output with arrows and cost summaries

---

## What “Priority Query System” Means Here
A normal queue is **FIFO** (first in, first out).  
A **priority queue** always returns the *highest priority* item first.

In routing, “priority” = **lowest total cost so far**.  
So we use a **min-heap** to always expand the next best candidate node during Dijkstra.

---

## 1) Dynamic Traffic Map (Hash Map)
Instead of relying only on static edge weights, we maintain a **Traffic Map** (dictionary).

### Traffic Map Design
- **Key:** a tuple representing the directed edge  
  Example: `("CityA", "CityB")`
- **Value:** the current traffic adjustment or current edge cost (depending on implementation choice)

### Why a Hash Map?
Traffic updates happen in **O(1)** average time.  
This lets us update “live traffic” instantly without rebuilding the graph.

During routing, Dijkstra “asks”:
> What is the current cost to go from A to B?

### Effective Weight (recommended)
Keep base weights in the graph and traffic deltas separate:


---

## 2) Shortest Path (Dijkstra’s Algorithm with a Heap)
Dijkstra is a greedy explorer: it always expands the node with the **lowest known cost** next.

### Min-Heap (Priority Queue)
We store tuples as:

### Core Logic
1. Start at the source with cost `0`
2. Pop the smallest-cost node from the heap
3. For each neighbor:
   - `new_cost = current_cost + get_weight(u, v)`
4. If `new_cost` improves the best known distance:
   - record it (distance + parent)
   - push `(new_cost, neighbor)` back into the heap

### Heap Tip (Python)
In Python `heapq`, always push `(cost, node)` so the heap sorts by **cost** first.

---

## 3) K-Shortest Paths (Alternative Routes)
The professor wants **K routes**, not just the best one.

A full standard solution is **Yen’s Algorithm**, but for this class project a simpler approach is acceptable:

### Iterative Dijkstra Approach
Repeat K times:
1. Find the shortest path
2. “Break” one edge in that path temporarily  
   (set its cost to infinity or apply a huge penalty)
3. Run Dijkstra again to find the next best route
4. Continue until K paths are found or no paths remain

---

## 4) Interface Design (Recommended Methods)
To keep code clean and reusable:

| Method | Purpose |
|------|---------|
| `update_traffic(u, v, delta)` | Update the Traffic Map with new live traffic data |
| `get_weight(u, v)` | Return effective weight (base + traffic delta, default 0 if none) |
| `find_shortest_path(start, end)` | Run Dijkstra using the heap and return (path, cost) |
| `format_route(path, cost)` | Convert `['A','B','C']` → `A -> B -> C (cost: X)` |

---

## 5) CLI Input and Output

### Commands File Format (`commands2.txt`)
Examples:

---

## Summary
Module 2 prepares the graph for weighted routing by adding:
- Real-time traffic updates via a hash map
- Dijkstra shortest path using a heap priority queue
- K alternative routes using iterative Dijkstra
- Clear CLI formatting for paths and costs
# Module 2 push test Thu Feb  5 23:57:23 CST 2026
