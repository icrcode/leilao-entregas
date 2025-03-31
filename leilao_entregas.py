import heapq
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

class DeliveryOptimizer:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.deliveries = []
        self.best_profit = 0
        self.best_path = []
        self.capital_coordinates = {
            "AC": (-68.667, -9.667), "AL": (-35.716, -9.667), "AM": (-60.025, -3.133), "AP": (-51.066, 0.034),
            "BA": (-38.516, -12.970), "CE": (-38.543, -3.717), "DF": (-47.882, -15.793), "ES": (-40.347, -20.315),
            "GO": (-49.253, -16.679), "MA": (-44.307, -2.530), "MG": (-43.938, -19.922), "MS": (-54.646, -20.448),
            "MT": (-56.096, -15.601), "PA": (-48.502, -1.455), "PB": (-34.870, -7.115), "PE": (-34.882, -8.054),
            "PI": (-42.802, -5.089), "PR": (-49.273, -25.428), "RJ": (-43.209, -22.906), "RN": (-35.209, -5.795),
            "RO": (-63.903, -8.761), "RR": (-60.671, 2.822), "RS": (-51.230, -30.033), "SC": (-48.548, -27.596),
            "SE": (-37.073, -10.947), "SP": (-46.633, -23.550), "TO": (-48.335, -10.184)
        }
    
    def ler_conexoes(self, arquivo):
        """Lê as conexões do arquivo e constrói o grafo"""
        with open(arquivo, 'r') as f:
            for linha in f:
                origem, destino, tempo = linha.strip().split(',')
                self.graph[origem][destino] = int(tempo)
                self.graph[destino][origem] = int(tempo)
    
    def ler_entregas(self, arquivo):
        """Lê a lista de entregas do arquivo"""
        with open(arquivo, 'r') as f:
            for linha in f:
                tempo, destino, bonus = linha.strip().split(',')
                self.deliveries.append((int(tempo), destino, int(bonus)))
    
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
    
    def calcular_melhor_rota(self):
        """Calcula a melhor sequência de entregas para maximizar o lucro"""
        inicio = "DF"
        melhor_lucro = 0
        melhor_sequencia = []
        tempo_inicio = time.perf_counter()
        
        for entrega in sorted(self.deliveries, key=lambda x: -x[2]):  # Ordena por bônus
            _, destino, bonus = entrega
            percurso, custo = self.dijkstra(inicio, destino)
            if custo < float('inf'):
                melhor_lucro += bonus
                melhor_sequencia.append((inicio, destino, custo, bonus))
                inicio = destino
        
        tempo_total = (time.perf_counter() - tempo_inicio) * 1000
        
        print("\nProgramação Dinâmica:")
        for origem, destino, custo, bonus in melhor_sequencia:
            print(f"{origem} -> {destino} | Tempo: {custo} min | Bônus: {bonus}")
        print(f"Lucro total: {melhor_lucro}")
        print(f"Tempo de execução: {tempo_total:.4f} ms")
    
    def visualize_graph(self):
        """Visualiza o grafo de conexões baseado no mapa do Brasil"""
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
                    plt.plot(x_values, y_values, 'gold', alpha=0.6, linewidth=2)
                    mid_x = (x_values[0] + x_values[1]) / 2
                    mid_y = (y_values[0] + y_values[1]) / 2
                    plt.text(mid_x, mid_y, str(weight), color='black', fontsize=12, fontweight='bold', bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'))
        
        for node, (x, y) in positions.items():
            plt.scatter(x, y, s=400, marker='s', color='royalblue', edgecolors='black', linewidth=1.5, alpha=0.9)
            plt.text(x, y, node, ha='center', va='center', fontsize=12, fontweight='bold', color='white', bbox=dict(facecolor='black', alpha=0.7, edgecolor='none'))
        
        plt.title("Grafo de Conexões das Capitais Brasileiras", fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel("Longitude", fontsize=12)
        plt.ylabel("Latitude", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.show()

if __name__ == "__main__":
    optimizer = DeliveryOptimizer()
    optimizer.ler_conexoes('conexoes_brasil.txt')
    optimizer.ler_entregas('entregas.txt')
    optimizer.visualize_graph()
    optimizer.calcular_melhor_rota()
