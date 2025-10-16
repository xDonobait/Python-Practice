import time
import os
import random
from typing import List, Callable


class SortVisualizer:
    def __init__(self, size: int = 20, delay: float = 0.1):
        self.size = size
        self.delay = delay
        self.comparisons = 0
        self.swaps = 0

    def clear_screen(self):
        """Limpia la pantalla según el sistema operativo"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def visualize(self, arr: List[int], highlight: List[int] = None, sorted_indices: List[int] = None):
        """Visualiza el arreglo con barras ASCII"""
        self.clear_screen()
        if highlight is None:
            highlight = []
        if sorted_indices is None:
            sorted_indices = []

        max_val = max(arr)
        height = 20

        print(f"\n{'=' * 60}")
        print(f"Comparaciones: {self.comparisons} | Intercambios: {self.swaps}")
        print(f"{'=' * 60}\n")

        # Dibujar las barras de arriba hacia abajo
        for level in range(height, 0, -1):
            line = ""
            for i, val in enumerate(arr):
                bar_height = int((val / max_val) * height)

                if i in sorted_indices:
                    char = "█" if bar_height >= level else " "
                    line += f"\033[92m{char}\033[0m "  # Verde para ordenados
                elif i in highlight:
                    char = "█" if bar_height >= level else " "
                    line += f"\033[93m{char}\033[0m "  # Amarillo para comparados
                else:
                    char = "█" if bar_height >= level else " "
                    line += f"\033[94m{char}\033[0m "  # Azul para no procesados
            print(line)

        # Números en la base
        print("\n" + " ".join(f"{val:2}" for val in arr))
        time.sleep(self.delay)

    def bubble_sort(self, arr: List[int]):
        """Bubble Sort con visualización"""
        n = len(arr)
        sorted_indices = []

        for i in range(n):
            swapped = False
            for j in range(n - i - 1):
                self.comparisons += 1
                self.visualize(arr, [j, j + 1], sorted_indices)

                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swaps += 1
                    swapped = True

            sorted_indices.append(n - i - 1)
            if not swapped:
                break

        self.visualize(arr, [], list(range(n)))

    def selection_sort(self, arr: List[int]):
        """Selection Sort con visualización"""
        n = len(arr)
        sorted_indices = []

        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.comparisons += 1
                self.visualize(arr, [min_idx, j], sorted_indices)

                if arr[j] < arr[min_idx]:
                    min_idx = j

            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                self.swaps += 1

            sorted_indices.append(i)
            self.visualize(arr, [], sorted_indices)

        self.visualize(arr, [], list(range(n)))

    def insertion_sort(self, arr: List[int]):
        """Insertion Sort con visualización"""
        n = len(arr)
        sorted_indices = [0]

        for i in range(1, n):
            key = arr[i]
            j = i - 1

            while j >= 0:
                self.comparisons += 1
                self.visualize(arr, [j, j + 1], sorted_indices)

                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    self.swaps += 1
                    j -= 1
                else:
                    break

            arr[j + 1] = key
            sorted_indices.append(i)

        self.visualize(arr, [], list(range(n)))

    def quick_sort(self, arr: List[int], low: int = 0, high: int = None, sorted_indices: List[int] = None):
        """Quick Sort con visualización"""
        if high is None:
            high = len(arr) - 1
        if sorted_indices is None:
            sorted_indices = []

        if low < high:
            pi = self.partition(arr, low, high, sorted_indices)
            sorted_indices.append(pi)

            self.quick_sort(arr, low, pi - 1, sorted_indices)
            self.quick_sort(arr, pi + 1, high, sorted_indices)
        elif low == high:
            sorted_indices.append(low)

        if low == 0 and high == len(arr) - 1:
            self.visualize(arr, [], list(range(len(arr))))

    def partition(self, arr: List[int], low: int, high: int, sorted_indices: List[int]) -> int:
        """Partición para Quick Sort"""
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            self.comparisons += 1
            self.visualize(arr, [j, high], sorted_indices)

            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.swaps += 1

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.swaps += 1
        self.visualize(arr, [i + 1], sorted_indices)

        return i + 1

    def merge_sort(self, arr: List[int], left: int = 0, right: int = None, sorted_indices: List[int] = None):
        """Merge Sort con visualización"""
        if right is None:
            right = len(arr) - 1
        if sorted_indices is None:
            sorted_indices = []

        if left < right:
            mid = (left + right) // 2

            self.merge_sort(arr, left, mid, sorted_indices)
            self.merge_sort(arr, mid + 1, right, sorted_indices)
            self.merge(arr, left, mid, right, sorted_indices)

        if left == 0 and right == len(arr) - 1:
            self.visualize(arr, [], list(range(len(arr))))

    def merge(self, arr: List[int], left: int, mid: int, right: int, sorted_indices: List[int]):
        """Mezcla para Merge Sort"""
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(L) and j < len(R):
            self.comparisons += 1
            self.visualize(arr, [k], sorted_indices)

            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            self.swaps += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            self.swaps += 1
            self.visualize(arr, [k - 1], sorted_indices)

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            self.swaps += 1
            self.visualize(arr, [k - 1], sorted_indices)

    def reset_stats(self):
        """Reinicia las estadísticas"""
        self.comparisons = 0
        self.swaps = 0


def main():
    algorithms = {
        '1': ('Bubble Sort', 'bubble_sort'),
        '2': ('Selection Sort', 'selection_sort'),
        '3': ('Insertion Sort', 'insertion_sort'),
        '4': ('Quick Sort', 'quick_sort'),
        '5': ('Merge Sort', 'merge_sort'),
    }

    print("\n" + "=" * 60)
    print("   VISUALIZADOR DE ALGORITMOS DE ORDENAMIENTO")
    print("=" * 60)

    print("\nSelecciona un algoritmo:")
    for key, (name, _) in algorithms.items():
        print(f"  {key}. {name}")
    print("  6. Salir")

    choice = input("\nOpción: ")

    if choice == '6':
        print("\n¡Hasta luego!\n")
        return

    if choice not in algorithms:
        print("\n❌ Opción inválida")
        return

    try:
        size = int(input("Tamaño del arreglo (10-30, default 20): ") or "20")
        size = max(10, min(30, size))
    except ValueError:
        size = 20

    try:
        speed = float(input("Velocidad (0.01-1.0 segundos, default 0.1): ") or "0.1")
        speed = max(0.01, min(1.0, speed))
    except ValueError:
        speed = 0.1

    # Generar arreglo aleatorio
    arr = random.sample(range(1, size * 3), size)

    # Crear visualizador y ejecutar algoritmo
    visualizer = SortVisualizer(size, speed)
    algo_name, algo_method = algorithms[choice]

    print(f"\n🚀 Ejecutando {algo_name}...\n")
    time.sleep(1)

    visualizer.visualize(arr)
    time.sleep(1)

    getattr(visualizer, algo_method)(arr.copy())

    print(f"\n{'=' * 60}")
    print(f"✅ {algo_name} completado!")
    print(f"   Comparaciones totales: {visualizer.comparisons}")
    print(f"   Intercambios totales: {visualizer.swaps}")
    print(f"{'=' * 60}\n")

    input("Presiona Enter para continuar...")


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            break1