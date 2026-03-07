# Transport Network System

**CS Project – Group 2**

---

# Team Members and Roles

**Sajeda Abuisad**

* Designed the overall module outline of the system
* Added shortcut and helper functions
* Assisted with debugging across modules
* Helped coordinate the structure and integration of the modules

**Alex Agbleade**

* Wrote and refined multiple parts of the code
* Assisted with debugging and improving program stability
* Helped clean and organize the final implementation

**Jo Schmidt**

* Initiated the team collaboration and created the shared project code
* Maintained the team To-Do list and tracked project progress
* Designed several core classes and functions including the MinHeap and Queue
* Contributed to Dijkstra's algorithm implementation and HashMap functions
* Performed initial testing for file loading functions

**Kaden Walls**

* Organized the GitHub repository structure
* Assisted with class design and system integration
* Helped debug the project and improve code readability

---

# Project Overview

The Ministry of Transport provided a dataset containing cities, road networks, traffic updates, and delivery request streams.

The goal of the project was to develop a **Transport Network System** capable of modeling a transportation map, handling real-time traffic updates, computing optimal routes, and managing delivery scheduling operations.

The system processes input data, builds a transportation graph, responds to route queries, and schedules deliveries efficiently using multiple data structures and algorithms.

---

# System Requirements

The system supports the following operations:

* Add new cities and roads to the transportation map
* Update and retrieve road distances or travel costs
* Process dynamic traffic reports that affect road conditions
* Find the shortest path between cities
* Schedule deliveries and maintain delivery history
* Undo scheduling and record operations when needed

---

# Contribution Breakdown

Each team member contributed to the development and debugging of the system. Responsibilities were divided across modules and shared when integration was required.

**Sajeda Abuisad**
Focused on outlining the system architecture and supporting module integration. Implemented helper functions and contributed to debugging across multiple modules.

**Alex Agbleade**
Completed file parsing and implemented multiple helper functions,  and graph construction functions, and developed the command-line interface with error handling. Contributed to output formatting and cross-module integration.

**Jo Schmidt**
Led the initial development setup and created foundational data structures and functions. Developed key classes including the MinHeap and Queue, contributed to the Dijkstra shortest path implementation, and implemented HashMap utility functions. Also maintained project coordination through task lists.

**Kaden Walls**
Created the Graph data structure, revised other classes such as the MinHeap & Queue. Designed the parsing system framework for road builder & query.

---

# Design Summary

The system architecture is composed of six main components that work together to process transportation data and delivery operations.

### 1. Input Files

The system receives several input files that contain commands, queries, traffic reports, city data, road data, delivery schedules, and history records.

### 2. Input Parser

The parser reads command line arguments and determines which operations should be executed. It prepares the data to be processed by the system modules.

### 3. Graph Builder (Module 1)

This module constructs a **directed weighted graph** representing the transportation network.
Cities are modeled as nodes, and roads are represented as edges with associated costs.
The graph is stored using an adjacency list to allow efficient traversal.

### 4. Traffic and Query Engine (Module 2)

This module handles route queries and traffic updates.

Key data structures and algorithms include:

* **Dijkstra’s Algorithm** for computing shortest paths
* **MinHeap / Priority Queue** to efficiently select the next closest node
* **HashMap** to dynamically update road costs when traffic changes occur

The graph created in Module 1 is reused here to process queries.

### 5. Delivery Scheduler (Module 3)

This module manages delivery tasks and records delivery history.

Several data structures are used:

* **Queue** for scheduling delivery tasks (FIFO order)
* **Sorted List** for maintaining delivery history ordered by time
* **Stack** to support undo operations (LIFO order)

The undo stack allows the system to reverse recent scheduling or recording actions.

### 6. Output Formatter

The final component formats system results for display.
Outputs are printed to the terminal with clear formatting using arrows (`->`), parentheses `()`, and spacing for readability.

---

# Lessons Learned

**Jo Schmidt**
Clear communication within a team is essential for project success. Maintaining task lists and sharing updates helped coordinate development effectively.

**Sajeda Abuisad**
Creating a project outline before development helped organize the system design. Incrementally building modules and performing unit testing before moving forward significantly improved debugging and maintenance.

**Alex Agbleade**
Working in a cooperative and supportive team environment made the development process more efficient and enjoyable.

**Kaden Walls**
Team members should remain responsive and proactive when collaborating. Code updates and changes should be clearly communicated to ensure smooth integration.
