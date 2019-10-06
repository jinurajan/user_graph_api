"""
I am writing algorithm using Dijkstra's algorithm.
Idea is to run this on adding any user association to compute
the shortest distance between same user node with every other node
and store it in cache. This can be done as a background task and could be used
from a separate datastore / Cache for those specific tasks / API calls

Assumption: There is no negative cycle

Distance to a vertex if there is no path to that returns None
"""

# example_node_representation is given below

nodes = {
    "A": [{"name": "B", "weight": 5}, {"name": "C", "weight": 4}],
    "B": [{"name": "C", "weight": 3}, {"name": "D", "weight": 2}],
    "C": [],
    "D": [{"name": "B", "weight": 1}, {"name": "C", "weight": 5}],
    "E": [{"name": "D", "weight": 3}]
}


class MinPriorityQueue(object): 
    def __init__(self):
        self.queue = []

    def __str__(self): 
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self): 
        return len(self.queue) == 0

    def insert(self, data):
        self.queue.append(data)

    def delete(self): 
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i] < self.queue[min]:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            exit()


# memoization: Below hash contains distance to all nodes from every other nodes

DISTANCE_VERTEX_ALL = {}


def find_shortest_path(source, destination):
    minimum_priority_queue = MinPriorityQueue()
    distance_vertex = {each: None for each in nodes}
    visited = set()
    minimum_priority_queue.insert((0, source))
    distance_vertex[source] = 0

    if DISTANCE_VERTEX_ALL.get(source):
        return DISTANCE_VERTEX_ALL[source][destination]

    while not minimum_priority_queue.isEmpty():
        vertex = minimum_priority_queue.delete()
        v = vertex[1]
        if v in visited:
            continue
        visited.add(v)
        for i in range(len(nodes[v])):
            e = nodes[v][i]["name"]
            w = nodes[v][i]["weight"]
            if (distance_vertex[e] is None) or (distance_vertex[v] + w < distance_vertex[e]):
                distance_vertex[e] = distance_vertex[v] + w
                minimum_priority_queue.insert((distance_vertex[e], e))
    DISTANCE_VERTEX_ALL[source] = distance_vertex
    return distance_vertex.get(destination)


if __name__ == "__main__":
    print("Shortest Path between {} and {} is: {}".format(
        "A", "C", find_shortest_path("A", "C")))
    print("Shortest Path between {} and {} is: {}".format(
        "A", "B", find_shortest_path("A", "B")))
    print("Shortest Path between {} and {} is: {}".format(
        "A", "E", find_shortest_path("A", "E")))

    print("Shortest Path between {} and {} is: {}".format(
        "B", "C", find_shortest_path("B", "C")))
    print("Shortest Path between {} and {} is: {}".format(
        "B", "D", find_shortest_path("B", "D")))

    print("Shortest Path between {} and {} is: {}".format(
        "D", "B", find_shortest_path("D", "B")))
