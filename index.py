import osmnx as ox
import heapq
import folium

def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end: 
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            min_weight = float('inf')
            for key, data in graph[current_node][neighbor].items():
                weight = data.get('length', 1)
                if weight < min_weight:
                    min_weight = weight

            distance = current_distance + min_weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruir o caminho
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous_nodes[node]
    path = path[::-1]

    return path

place_name = "Santa Maria, DF, Brasil"

graph = ox.graph_from_place(place_name, network_type='drive')
start_latlng = (-16.040755, -48.034199) # A coordenada do ponto inicial
end_latlng = (-16.040521, -48.030425) # Aqui é a coordenada do ponto final

try:
    start = ox.distance.nearest_nodes(graph, start_latlng[1], start_latlng[0])
    end = ox.distance.nearest_nodes(graph, end_latlng[1], end_latlng[0])
except ImportError as e:
    print(e)
    raise e

route = dijkstra(graph, start, end)
route_coordinates = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]

print(route_coordinates)

my_map = folium.Map(location=start_latlng, zoom_start=14)
folium.PolyLine(route_coordinates, color='blue', weight=5, opacity=0.7).add_to(my_map)
folium.Marker(location=start_latlng, popup='Start', icon=folium.Icon(color='green')).add_to(my_map)
folium.Marker(location=end_latlng, popup='End', icon=folium.Icon(color='red')).add_to(my_map)

my_map.save("mapa_com_menor_caminho.html")

print("O mapa com a rota foi salvo com sucesso!")