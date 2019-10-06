"""
TODO: This should not be done with so many API calls. This has to be performed as a background task
Whenever an association/ de-association is happening run dijkstra's algorithm on that node and update distance to every other node.
Since there can be millions of users there is no need to update distance for all other vertices instead run a BFS 
and find out the possible connections list and create distance metrix for each of those nodes and save it in a 
datastore like redis where reading is really cheap. For background tasks use celery or kafka as distributed queue.
Below code is an example of how this can be done

"""

import requests
from conf.settings import Config

HOST = "127.0.0.1"


def get_following_users(email):
    url = "http://{}:{}/users/{}/following_users".format(
        HOST, Config.port, email)
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception("API call Failed")
        return resp.json()["following_users"]
    except Exception as e:
        raise e


def get_all_users():
    url = "http://{}:{}/users".format(
        HOST, Config.port)
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception("API call Failed")
        return resp.json()
    except Exception as e:
        raise e


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


nodes = {user["email"]: user for user in get_all_users()}


# memoization: Below hash will contain distance to all nodes from every other nodes

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
        following_users = get_following_users(v)
        for i in range(len(following_users)):
            e = following_users[i]
            w = 1  # in this case all edge weights are equal
            if (distance_vertex[e] is None) or (distance_vertex[v] + w < distance_vertex[e]):
                distance_vertex[e] = distance_vertex[v] + w
                minimum_priority_queue.insert((distance_vertex[e], e))
    DISTANCE_VERTEX_ALL[source] = distance_vertex
    return distance_vertex.get(destination)

if __name__ == "__main__":
    print("Shortest path between {} and {} is: {}".format(
        "jimxugle@gmail.com",
        "mahbub@live.com",
        find_shortest_path("jimxugle@gmail.com", "mahbub@live.com")))
    print("Shortest path between {} and {} is: {}".format(
        "jimxugle@gmail.com",
        "isorashi@me.com",
        find_shortest_path("jimxugle@gmail.com", "isorashi@me.com")))
    print("Shortest path between {} and {} is: {}".format(
        "jimxugle@gmail.com",
        "jbryan@yahoo.com",
        find_shortest_path("jimxugle@gmail.com", "jbryan@yahoo.com")))
