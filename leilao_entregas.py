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
    
    def ler_conexoes(self, arquivo):
        """Lê as conexões do arquivo e constrói o grafo"""
        with open(arquivo, 'r') as f:
            for linha in f:
                origem, destino, tempo = linha.strip().split(',')
                self.graph[origem][destino] = int(tempo)
                self.graph[destino][origem] = int(tempo)
    
    def ler_entregas(self, arquivo):
        """Lê as entregas do arquivo e ordena por horário"""
        with open(arquivo, 'r') as f:
            for linha in f:
                horario, destino, bonus = linha.strip().split(',')
                self.deliveries.append((int(horario), destino, int(bonus)))
        # Ordena as entregas por horário
        self.deliveries.sort(key=lambda x: x[0])
    
    def dijkstra(self, start, end):
        """Calcula o caminho mais curto entre dois pontos usando Dijkstra"""
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
    
    def calculate_possible_deliveries(self):
        """Calcula todas as combinações possíveis de entregas"""
        n = len(self.deliveries)
        max_profit = 0
        best_combination = []
        
        # Gera todas as combinações possíveis usando bitmask
        for mask in range(1, 1 << n):
            current_profit = 0
            current_time = 0
            current_position = 'A'
            combination = []
            valid = True
            
            for i in range(n):
                if mask & (1 << i):
                    delivery = self.deliveries[i]
                    horario, destino, bonus = delivery
                    
                    # Calcula o tempo para ir da posição atual ao destino
                    time_to_dest, _ = self.dijkstra(current_position, destino)
                    
                    # Verifica se é possível chegar a tempo
                    if current_time + time_to_dest > horario:
                        valid = False
                        break
                    
                    # Atualiza tempo e posição
                    time_back, _ = self.dijkstra(destino, 'A')
                    current_time += time_to_dest + time_back
                    current_position = 'A'
                    current_profit += bonus
                    combination.append(delivery)
            
            if valid and current_profit > max_profit:
                max_profit = current_profit
                best_combination = combination
        
        self.best_profit = max_profit
        self.best_path = best_combination
        return best_combination, max_profit
    
    def optimized_delivery_selection(self):
        """Versão otimizada usando programação dinâmica"""
        n = len(self.deliveries)
        dp = [0] * (n + 1)
        last_delivery_time = [0] * (n + 1)
        
        for i in range(1, n + 1):
            horario, destino, bonus = self.deliveries[i-1]
            
            # Tempo para ir de A ao destino e voltar
            time_to_dest, _ = self.dijkstra('A', destino)
            total_time = time_to_dest * 2
            
            # Verifica entregas anteriores que não conflitam
            best_previous = 0
            best_time = 0
            for j in range(i):
                if last_delivery_time[j] <= horario - total_time:
                    if dp[j] > best_previous:
                        best_previous = dp[j]
                        best_time = last_delivery_time[j] + total_time
            
            # Escolhe a melhor opção
            if best_previous + bonus > dp[i-1]:
                dp[i] = best_previous + bonus
                last_delivery_time[i] = best_time
            else:
                dp[i] = dp[i-1]
                last_delivery_time[i] = last_delivery_time[i-1]
        
        # Reconstruir a sequência
        sequence = []
        current_profit = dp[n]
        remaining_time = last_delivery_time[n]
        
        for i in range(n, 0, -1):
            if dp[i] != dp[i-1]:
                sequence.append(self.deliveries[i-1])
                _, destino, _ = self.deliveries[i-1]
                time_to_dest, _ = self.dijkstra('A', destino)
                remaining_time -= time_to_dest * 2
        
        sequence.reverse()
        return sequence, current_profit
    
    def visualize_graph(self):
        """Visualiza o grafo de conexões"""
        plt.figure(figsize=(10, 6))
        pos = {}
        nodes = list(self.graph.keys())
        
        # Posicionamento circular para os nós
        for i, node in enumerate(nodes):
            angle = 2 * i * 3.1416 / len(nodes)
            pos[node] = (np.cos(angle), np.sin(angle))
        
        # Desenha as arestas
        for node in self.graph:
            for neighbor, weight in self.graph[node].items():
                plt.plot([pos[node][0], pos[neighbor][0]], 
                         [pos[node][1], pos[neighbor][1]], 
                         'k-', alpha=0.3)
                mid_x = (pos[node][0] + pos[neighbor][0]) / 2
                mid_y = (pos[node][1] + pos[neighbor][1]) / 2
                plt.text(mid_x, mid_y, str(weight), color='red')
        
        # Desenha os nós
        for node in pos:
            plt.plot(pos[node][0], pos[node][1], 'o', markersize=20, 
                    color='skyblue' if node != 'A' else 'lightgreen')
            plt.text(pos[node][0], pos[node][1], node, 
                     ha='center', va='center', fontsize=12)
        
        plt.title("Grafo de Conexões entre Destinos")
        plt.axis('off')
        plt.show()

# Função para medir desempenho
def benchmark(optimizer):
    methods = {
        "Combinação Completa": optimizer.calculate_possible_deliveries,
        "Programação Dinâmica": optimizer.optimized_delivery_selection
    }
    
    results = {}
    times = {}
    
    for name, method in methods.items():
        start_time = time.perf_counter()
        sequence, profit = method()
        elapsed = (time.perf_counter() - start_time) * 1000
        
        results[name] = profit
        times[name] = elapsed
        
        print(f"\n{name}:")
        print(f"Sequência: {sequence}")
        print(f"Lucro: {profit}")
        print(f"Tempo: {elapsed:.6f} ms")
    
    # Plot resultados
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.bar(results.keys(), results.values(), color=['red', 'orange'])
    plt.title('Comparação de Lucro')
    plt.ylabel('Lucro Total')
    
    plt.subplot(1, 2, 2)
    plt.bar(times.keys(), times.values(), color=['red', 'orange'])
    plt.title('Comparação de Tempo de Execução')
    plt.ylabel('Tempo (ms)')
    
    plt.tight_layout()
    plt.show()

# Exemplo de uso
if __name__ == "__main__":
    optimizer = DeliveryOptimizer()
    
    # Carrega os dados
    optimizer.ler_conexoes('conexoes.txt')
    optimizer.ler_entregas('entregas.txt')
    
    # Visualiza o grafo
    optimizer.visualize_graph()
    
    # Executa e compara os algoritmos
    benchmark(optimizer)