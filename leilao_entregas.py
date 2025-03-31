import heapq
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Coordenadas aproximadas das capitais brasileiras
capital_coords = {
    "AC": (-70.55, -9.97), "AL": (-35.73, -9.67), "AM": (-60.02, -3.1), "AP": (-51.07, 0.03), "BA": (-38.5, -12.97),
    "CE": (-38.52, -3.72), "DF": (-47.93, -15.78), "ES": (-40.29, -20.32), "GO": (-49.25, -16.68), "MA": (-44.30, -2.53),
    "MG": (-44.38, -19.92), "MS": (-54.62, -20.45), "MT": (-56.1, -15.6), "PA": (-48.50, -1.45), "PB": (-34.88, -7.12),
    "PE": (-34.88, -8.05), "PI": (-42.80, -5.09), "PR": (-49.27, -25.42), "RJ": (-43.17, -22.90), "RN": (-35.22, -5.81),
    "RO": (-63.9, -8.77), "RR": (-60.67, 2.82), "RS": (-51.23, -30.03), "SC": (-48.55, -27.59), "SE": (-37.07, -10.91),
    "SP": (-46.63, -23.55), "TO": (-48.33, -10.25)
}

class DeliveryOptimizer:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.deliveries = []
        self.best_profit = 0
        self.best_path = []
    
    def ler_conexoes(self, arquivo):
        with open(arquivo, 'r') as f:
            for linha in f:
                origem, destino, tempo = linha.strip().split(',')
                self.graph[origem][destino] = int(tempo)
                self.graph[destino][origem] = int(tempo)
    
    def ler_entregas(self, arquivo):
        with open(arquivo, 'r') as f:
            for linha in f:
                horario, destino, bonus = linha.strip().split(',')
                self.deliveries.append((int(horario), destino, int(bonus)))
        self.deliveries.sort(key=lambda x: x[0])
    
    def dijkstra(self, start, end):
        heap = [(0, start)]
        visited = set()
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        previous = {node: None for node in self.graph}
        
        while heap:
            current_dist, current_node = heapq.heappop(heap)
            
            if current_node == end:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = previous[current_node]
                return current_dist, path[::-1]
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            for neighbor, weight in self.graph[current_node].items():
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(heap, (distance, neighbor))
        
        return float('inf'), []
    
    def visualize_graph(self):
        plt.figure(figsize=(10, 8))
        
        for node in self.graph:
            x, y = capital_coords[node]
            plt.scatter(x, y, color='blue' if node != 'A' else 'red', s=100)
            plt.text(x, y, node, fontsize=10, ha='right', color='black')
        
        for node in self.graph:
            for neighbor in self.graph[node]:
                x1, y1 = capital_coords[node]
                x2, y2 = capital_coords[neighbor]
                plt.plot([x1, x2], [y1, y2], 'k-', alpha=0.5)
        
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Mapa de Conexões entre Capitais")
        plt.grid(True)
        plt.show()

# Exemplo de uso
if __name__ == "__main__":
    optimizer = DeliveryOptimizer()
    optimizer.ler_conexoes('conexoes_brasil.txt')
    optimizer.ler_entregas('entregas.txt')
    optimizer.visualize_graph()
