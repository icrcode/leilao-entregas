import heapq
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

class DeliveryOptimizer:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.capital_coordinates = {
            "AC": (-68.667, -9.667), "AL": (-35.716, -9.667), "AM": (-60.025, -3.133), "AP": (-51.066, 0.034),
            "BA": (-38.516, -12.970), "CE": (-38.543, -3.717), "DF": (-47.882, -15.793), "ES": (-40.347, -20.315),
            "GO": (-49.253, -16.679), "MA": (-44.307, -2.530), "MG": (-43.938, -19.922), "MS": (-54.646, -20.448),
            "MT": (-56.096, -15.601), "PA": (-48.502, -1.455), "PB": (-34.870, -7.115), "PE": (-34.882, -8.054),
            "PI": (-42.802, -5.089), "PR": (-49.273, -25.428), "RJ": (-43.209, -22.906), "RN": (-35.209, -5.795),
            "RO": (-63.903, -8.761), "RR": (-60.671, 2.822), "RS": (-51.230, -30.033), "SC": (-48.548, -27.596),
            "SE": (-37.073, -10.947), "SP": (-46.633, -23.550), "TO": (-48.335, -10.184)
        }
        self.best_route = []
    
    def ler_conexoes(self, arquivo):
        """Lê as conexões do arquivo e constrói o grafo"""
        with open(arquivo, 'r') as f:
            for linha in f:
                origem, destino, distancia = linha.strip().split(',')
                self.graph[origem][destino] = int(distancia)
                self.graph[destino][origem] = int(distancia)

    def dijkstra(self, origem, destino):
        """Calcula o menor caminho entre duas capitais"""
        fila = [(0, origem)]
        custos = {cidade: float('inf') for cidade in self.graph}
        custos[origem] = 0
        caminho = {}
        
        while fila:
            custo_atual, cidade_atual = heapq.heappop(fila)
            if cidade_atual == destino:
                break
            for vizinho, custo in self.graph[cidade_atual].items():
                novo_custo = custo_atual + custo
                if novo_custo < custos[vizinho]:
                    custos[vizinho] = novo_custo
                    heapq.heappush(fila, (novo_custo, vizinho))
                    caminho[vizinho] = cidade_atual
        
        percurso = []
        cidade = destino
        while cidade in caminho:
            percurso.append(cidade)
            cidade = caminho[cidade]
        percurso.append(origem)
        percurso.reverse()
        return percurso, custos[destino]
    
    def visualize_graph(self, rota=None):
        """Visualiza o grafo e destaca a menor rota se fornecida"""
        plt.figure(figsize=(12, 14))
        
        active_capitals = set(self.graph.keys())
        positions = {cap: self.capital_coordinates[cap] for cap in active_capitals if cap in self.capital_coordinates}
        
        for node in self.graph:
            if node not in positions:
                continue
            for neighbor, weight in self.graph[node].items():
                if neighbor in positions:
                    x_values = [positions[node][0], positions[neighbor][0]]
                    y_values = [positions[node][1], positions[neighbor][1]]
                    color = 'red' if rota and (node, neighbor) in rota or (neighbor, node) in rota else 'gold'
                    linewidth = 4 if color == 'red' else 2
                    plt.plot(x_values, y_values, color, alpha=0.6, linewidth=linewidth)
                    mid_x = (x_values[0] + x_values[1]) / 2
                    mid_y = (y_values[0] + y_values[1]) / 2
                    plt.text(mid_x, mid_y, f"{weight} km", color='black', fontsize=12, fontweight='bold')
        
        for node, (x, y) in positions.items():
            plt.scatter(x, y, s=400, marker='s', color='royalblue', edgecolors='black', linewidth=1.5, alpha=0.9)
            plt.text(x, y, node, ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        plt.title("Grafo de Conexões das Capitais Brasileiras (Distância em KM)", fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel("Longitude", fontsize=12)
        plt.ylabel("Latitude", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.show()

if __name__ == "__main__":
    optimizer = DeliveryOptimizer()
    optimizer.ler_conexoes('conexoes_brasil.txt')
    
    origem = input("Digite a cidade de origem (sigla): ").strip().upper()
    destino = input("Digite a cidade de destino (sigla): ").strip().upper()

    if origem not in optimizer.graph or destino not in optimizer.graph:
        print("Cidade inválida. Certifique-se de usar a sigla correta.")
    else:
        caminho, distancia_total = optimizer.dijkstra(origem, destino)
        print("\nMelhor Rota Encontrada:")
        print(" -> ".join(caminho))
        print(f"Distância total: {distancia_total} km")
        
        rota_destacada = [(caminho[i], caminho[i + 1]) for i in range(len(caminho) - 1)]
        optimizer.visualize_graph(rota=rota_destacada)