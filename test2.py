## create a function that performs a uniform cost search
def UCS(G, StartNode, EndNode):
    # initialize the queues and cost
    searchQueue, visited, path, cost = [], [], [], 0
    # add the start node to the queue
    searchQueue.append(StartNode)
    # loop until the queue is empty
    while searchQueue:
        # pop the first element from the queue
        current = searchQueue.pop(0)
        # check if the current node is the end node, return the path and the cost
        if current == EndNode: return path, cost
        # check if the current node has been visited
        if current not in visited:
            # add the current node to the visited nodes
            visited.append(current)
            path.append(current)

            # loop through the neighbors of the current node
            for neighbor in G[current]:
                # check if the neighbor has been visited
                if neighbor not in visited:
                    # add the neighbor to the queue
                    searchQueue.append(neighbor)
                    # add the cost of the neighbor to the cost
                    cost = cost + G[current][neighbor]['weight']
    # return the path and the cost
    return path, cost