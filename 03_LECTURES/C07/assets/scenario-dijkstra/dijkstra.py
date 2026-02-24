from heapq import heappop, heappush

def dijkstra(graph, source):
    distances = {v: float("inf") for v in graph}
    predecessors = {v: None for v in graph}
    distances[source] = 0

    pq = [(0, source)]

    while pq:
        dist_u, u = heappop(pq)

        if dist_u != distances[u]:
            continue

        for v, w in graph[u].items():
            nd = dist_u + w
            if nd < distances[v]:
                distances[v] = nd
                predecessors[v] = u
                heappush(pq, (nd, v))

    return distances, predecessors

def main():
    graph = {
        "A": {"B": 4, "C": 2},
        "B": {"D": 2, "E": 3, "A": 4},
        "C": {"D": 3, "E": 1, "A": 2},
        "D": {"C": 3, "B": 2},
        "E": {"B": 3, "C": 1},
    }
    source = "C"

    distances, _ = dijkstra(graph, source)
    print("Shortest distances from", source)
    for v in sorted(distances.keys()):
        print(v, ":", distances[v])

if __name__ == "__main__":
    main()
