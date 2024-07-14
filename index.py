import osmnx as ox
import heapq
import folium

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
folium.PolyLine(route_coordinates, color="blue", weight=5, opacity=0.7).add_to(my_map)
folium.Marker(location=start_latlng).add_to(my_map)
folium.Marker(location=end_latlng).add_to(my_map)

my_map.save("mapa_com_menor_caminho.html")

print("O mapa com a rota foi salvo com sucesso!")