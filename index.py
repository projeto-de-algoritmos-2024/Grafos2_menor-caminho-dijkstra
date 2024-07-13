import heapq

def dijkstra (graph, start, end):
    queue = [(0, start)]
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous_node = {node: None for node in graph.nodes}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            min_weight = float('infinity')
            for _,_, data in graph.edges(current_node, data=True):
                weight = data.get('lenght', 1)
                if weight < min_weight:
                    min_weight = weight
            
            distance = current_distance + min_weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous_node[node]
    path = path[::-1]

    return path