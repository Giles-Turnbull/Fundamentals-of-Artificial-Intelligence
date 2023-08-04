#Github co-pilot was used in this question so some of the vocabulary used in djkstra's algorithm may be generic
#the reference for github co-pilot is https://copilot.github.com/
#this code must be run as a .ipynb file for it to work

%matplotlib inline
import networkx as nx
from matplotlib import pyplot as plt
from collections import defaultdict, deque

#this is a list of tuples that represent the route map given in the question
Routemap = [('St. Louis', 'Miami'), ('St. Louis', 'San Diego'), ('St. Louis', 'Chicago'), ('San Diego', 'Chicago'), 
            ('San Diego', 'San Francisco'), ('San Diego', 'Minneapolis'), ('San Diego', 'Boston'), ('San Diego', 'Portland'), 
            ('San Diego', 'Seattle'), ('Tulsa', 'New York'), ('Tulsa', 'Dallas'), ('Phoenix', 'Cleveland'), ('Phoenix', 'Denver'), 
            ('Phoenix', 'Dallas'), ('Chicago', 'New York'), ('Chicago', 'Los Angeles'), ('Miami', 'New York'), ('Miami', 'Philadelphia'), 
            ('Miami', 'Denver'), ('Boston', 'Atlanta'), ('Dallas', 'Cleveland'), ('Dallas', 'Albuquerque'), ('Philadelphia', 'Atlanta'), ('Denver', 'Minneapolis'), 
            ('Denver', 'Cleveland'), ('Albuquerque', 'Atlanta'), ('Minneapolis', 'Portland'), ('Los Angeles', 'Seattle'), 
            ('San Francisco', 'Portland'), ('San Francisco', 'Seattle'), ('San Francisco', 'Cleveland'), ('Seattle', 'Portland')]

#a graph using networkx using the list
G = nx.Graph()
G.add_edges_from(Routemap)
nx.draw(G, with_labels=True)
plt.show()

###########
# part A
###########

#a depth first search function to find the maximum number of hops between any two cities in the route map
def find_longest_path(graph, start, end):
    visitedNodes, path, longestPath = set(), [], []
    def dfs(city):
        nonlocal longestPath
        visitedNodes.add(city)
        path.append(city)
        #if the city is the end city, check if the path is longer than the longest path
        if city == end:
            if len(longestPath) < len(path): longestPath = list(path)
        else:
            for neighbor in graph[city]:
                if neighbor not in visitedNodes: dfs(neighbor)
        #pop the last node from the path and remove it from the visited nodes        
        path.pop()
        visitedNodes.remove(city)
    dfs(start)
    return longestPath


###########
# part B
###########

#a function for dijkstra's algorithm to find the shortest path between two nodes
def dijkstra(graphRouteMap, start, destination, visitedNodes=[], distances={}, predecessors={}):
    #a few sanity checks
    if (start not in graphRouteMap) or (destination not in graphRouteMap): print("Invalid input")
    
    #check if the start node is the destination node so the function can end
    if (start == destination):
        #build the final path from the predecessors
        previousNode = destination
        Finalpath = []
        while previousNode != None:     #run until the predecessor is empty
            Finalpath.append(previousNode)
            previousNode = predecessors.get(previousNode, None)
        print("the shortest path is: " + str(Finalpath) + " with a cost of: " + str(distances[destination]) + " hops")
    else:
        #if it is the initial run, initialize the cost and mark the current node as visited
        if not visitedNodes: distances[start] = 0
        visitedNodes.append(start)

        #visit the neighbors of the current node
        for neighbor in graphRouteMap[start]:
            #if the node has not been visited
            if neighbor not in visitedNodes:
                new_distance = distances[start] + 1
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = start
        
        unvisited = {}
        for k in graphRouteMap:
            if k not in visitedNodes: unvisited[k] = distances.get(k, float('inf'))
        currentNode = min(unvisited, key=unvisited.get)
        #recursion substitute start for current node
        dijkstra(graphRouteMap, currentNode, destination, visitedNodes, distances, predecessors)

#run the function
dijkstra(G, 'Seattle', 'Atlanta')


    



###########
# part C
###########

#I have rewritten the routemap as an adjacency list so that I can use it in the next part
AdjacencyMap = {'St. Louis': ['Miami', 'San Diego', 'Chicago'], 'Miami': ['St. Louis', 'New York', 'Philadelphia', 'Denver'], 
           'San Diego': ['St. Louis', 'Chicago', 'San Francisco', 'Minneapolis', 'Boston', 'Portland', 'Seattle'], 
           'Chicago': ['St. Louis', 'San Diego', 'New York', 'Los Angeles'], 
           'San Francisco': ['San Diego', 'Portland', 'Seattle', 'Cleveland'], 
           'Minneapolis': ['San Diego', 'Denver', 'Portland'], 'Boston': ['San Diego', 'Atlanta'], 
           'Portland': ['San Diego', 'Minneapolis', 'San Francisco', 'Seattle'], 
           'Seattle': ['San Diego', 'Los Angeles', 'San Francisco', 'Portland'], 
           'Tulsa': ['New York', 'Dallas'], 'New York': ['Tulsa', 'Chicago', 'Miami'], 
           'Dallas': ['Tulsa', 'Phoenix', 'Cleveland', 'Albuquerque'], 
           'Phoenix': ['Cleveland', 'Denver', 'Dallas'], 'Cleveland': ['Phoenix', 'Dallas', 'Denver', 'San Francisco'], 
           'Denver': ['Phoenix', 'Miami', 'Minneapolis', 'Cleveland'], 
           'Los Angeles': ['Chicago', 'Seattle'], 'Philadelphia': ['Miami', 'Atlanta'], 
           'Atlanta': ['Boston', 'Philadelphia', 'Albuquerque'], 'Albuquerque': ['Dallas', 'Atlanta']}

#function using deque and bfs to find the optimal city
def find_optimal_city(routemap):
    #initialize variables
    graph = routemap
    cities, min_avg_hops, optimal_city = list(graph.keys()), float('inf'), None

    #loop through the cities
    for city in cities:
        visited = [False] * len(cities)
        queue = deque()
        queue.append(city)
        visited[cities.index(city)] = True
        total_hops, count = 0, 0

        #run until the queue is empty
        while queue:
            curr_city = queue.popleft()
            for adj_city in graph[curr_city]:
                if not visited[cities.index(adj_city)]:
                    queue.append(adj_city)
                    visited[cities.index(adj_city)] = True
                    total_hops += 1
                    count += 1

        avg_hops = total_hops / count if count > 0 else 0
        #this finds the minimum average hops

        #change the optimal city if the average hops is less than the minimum average hops
        if  min_avg_hops > avg_hops:
            min_avg_hops, optimal_city = avg_hops, city
    #return the optimal city
    return optimal_city

# run the function
optimal_city = find_optimal_city(AdjacencyMap)
print("the optimal city to live in is: " + optimal_city)



