def bellman_ford(graph, source):
    distances = {v: float("inf") for v in graph}
    predecessors = {v: None for v in graph}
    distances[source] = 0

    vertices = list(graph.keys())

    print("INITIAL distances:", distances)
    print("INITIAL predecessors:", predecessors)
    print()

    for i in range(len(vertices) - 1):
        changed = False
        for u in vertices:
            for v, w in graph[u].items():
                if distances[u] != float("inf") and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    predecessors[v] = u
                    changed = True

        print(f"ITERATION {i + 1} distances:", distances)
        if not changed:
            print("No changes, stopping early.")
            break

    # negative cycle detection
    for u in vertices:
        for v, w in graph[u].items():
            if distances[u] != float("inf") and distances[u] + w < distances[v]:
                return None, None

    return distances, predecessors

def main():
    graph = {
        "A": {"B": 4, "C": 2},
        "B": {"D": 2, "E": 3, "A": 4},
        "C": {"D": 3, "E": 1, "A": 2},
        "D": {"C": 3, "B": 2},
        "E": {"B": 3, "C": 1},
    }
    source = "D"

    distances, predecessors = bellman_ford(graph, source)
    if distances is None:
        print("Negative cycle detected")
        return

    print()
    print("Shortest distances from", source)
    for v in sorted(distances.keys()):
        print(v, ":", distances[v])

if __name__ == "__main__":
    main()
