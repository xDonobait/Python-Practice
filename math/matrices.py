import os
from typing import List, Tuple, Optional


class Matrix:
    def __init__(self, data: List[List[float]]):
        """Inicializa una matriz"""
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    def __str__(self) -> str:
        """Representación en string de la matriz"""
        if not self.data:
            return "[]"

        # Encontrar el ancho máximo para alinear
        max_width = max(len(f"{val:.4g}") for row in self.data for val in row)

        result = []
        for row in self.data:
            formatted_row = "  ".join(f"{val:>{max_width}.4g}" for val in row)
            result.append(f"[ {formatted_row} ]")

        return "\n".join(result)

    def copy(self) -> 'Matrix':
        """Crea una copia de la matriz"""
        return Matrix([row[:] for row in self.data])

    @staticmethod
    def identity(n: int) -> 'Matrix':
        """Crea una matriz identidad de tamaño n x n"""
        data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        return Matrix(data)

    @staticmethod
    def zeros(rows: int, cols: int) -> 'Matrix':
        """Crea una matriz de ceros"""
        data = [[0.0 for _ in range(cols)] for _ in range(rows)]
        return Matrix(data)

    def add(self, other: 'Matrix') -> 'Matrix':
        """Suma dos matrices"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Las matrices deben tener las mismas dimensiones")

        result = [[self.data[i][j] + other.data[i][j]
                   for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def subtract(self, other: 'Matrix') -> 'Matrix':
        """Resta dos matrices"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Las matrices deben tener las mismas dimensiones")

        result = [[self.data[i][j] - other.data[i][j]
                   for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def multiply(self, other: 'Matrix') -> 'Matrix':
        """Multiplica dos matrices"""
        if self.cols != other.rows:
            raise ValueError(f"No se pueden multiplicar: {self.rows}x{self.cols} * {other.rows}x{other.cols}")

        result = [[sum(self.data[i][k] * other.data[k][j]
                       for k in range(self.cols))
                   for j in range(other.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def scalar_multiply(self, scalar: float) -> 'Matrix':
        """Multiplica la matriz por un escalar"""
        result = [[self.data[i][j] * scalar
                   for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def transpose(self) -> 'Matrix':
        """Transpone la matriz"""
        result = [[self.data[i][j]
                   for i in range(self.rows)]
                  for j in range(self.cols)]
        return Matrix(result)

    def determinant(self) -> float:
        """Calcula el determinante de la matriz"""
        if self.rows != self.cols:
            raise ValueError("La matriz debe ser cuadrada")

        if self.rows == 1:
            return self.data[0][0]

        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

        det = 0
        for j in range(self.cols):
            minor = self.get_minor(0, j)
            cofactor = ((-1) ** j) * self.data[0][j] * minor.determinant()
            det += cofactor

        return det

    def get_minor(self, row: int, col: int) -> 'Matrix':
        """Obtiene la matriz menor eliminando una fila y columna"""
        minor_data = []
        for i in range(self.rows):
            if i == row:
                continue
            minor_row = []
            for j in range(self.cols):
                if j == col:
                    continue
                minor_row.append(self.data[i][j])
            minor_data.append(minor_row)
        return Matrix(minor_data)

    def inverse(self) -> 'Matrix':
        """Calcula la inversa de la matriz usando Gauss-Jordan"""
        if self.rows != self.cols:
            raise ValueError("La matriz debe ser cuadrada")

        det = self.determinant()
        if abs(det) < 1e-10:
            raise ValueError("La matriz es singular (determinante = 0)")

        n = self.rows
        # Crear matriz aumentada [A|I]
        augmented = [self.data[i][:] + Matrix.identity(n).data[i]
                     for i in range(n)]

        # Eliminación de Gauss-Jordan
        for i in range(n):
            # Buscar el pivote
            max_row = i
            for k in range(i + 1, n):
                if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                    max_row = k
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]

            # Hacer el pivote = 1
            pivot = augmented[i][i]
            if abs(pivot) < 1e-10:
                raise ValueError("La matriz es singular")

            for j in range(2 * n):
                augmented[i][j] /= pivot

            # Eliminar la columna
            for k in range(n):
                if k != i:
                    factor = augmented[k][i]
                    for j in range(2 * n):
                        augmented[k][j] -= factor * augmented[i][j]

        # Extraer la matriz inversa
        inverse_data = [[augmented[i][j] for j in range(n, 2 * n)]
                        for i in range(n)]
        return Matrix(inverse_data)

    def rank(self) -> int:
        """Calcula el rango de la matriz"""
        # Crear una copia para no modificar la original
        temp = [row[:] for row in self.data]
        rank = min(self.rows, self.cols)

        for row in range(rank):
            # Si el elemento diagonal es 0, buscar un elemento no cero
            if abs(temp[row][row]) < 1e-10:
                reduce = True
                for i in range(row + 1, self.rows):
                    if abs(temp[i][row]) > 1e-10:
                        temp[row], temp[i] = temp[i], temp[row]
                        reduce = False
                        break

                if reduce:
                    rank -= 1
                    for i in range(self.rows):
                        temp[i][row] = temp[i][rank]
                    row -= 1
                    continue

            # Reducir las filas siguientes
            for i in range(row + 1, self.rows):
                factor = temp[i][row] / temp[row][row]
                for j in range(row, self.cols):
                    temp[i][j] -= factor * temp[row][j]

        return rank

    def trace(self) -> float:
        """Calcula la traza de la matriz (suma de la diagonal)"""
        if self.rows != self.cols:
            raise ValueError("La matriz debe ser cuadrada")
        return sum(self.data[i][i] for i in range(self.rows))

    def power(self, n: int) -> 'Matrix':
        """Eleva la matriz a la potencia n"""
        if self.rows != self.cols:
            raise ValueError("La matriz debe ser cuadrada")

        if n == 0:
            return Matrix.identity(self.rows)

        if n < 0:
            return self.inverse().power(-n)

        result = Matrix.identity(self.rows)
        base = self.copy()

        while n > 0:
            if n % 2 == 1:
                result = result.multiply(base)
            base = base.multiply(base)
            n //= 2

        return result


def clear_screen():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')


def read_matrix(name: str = "matriz") -> Matrix:
    """Lee una matriz del usuario"""
    print(f"\n📝 Ingresa la {name}:")

    try:
        rows = int(input("  Número de filas: "))
        cols = int(input("  Número de columnas: "))

        if rows <= 0 or cols <= 0:
            raise ValueError("Las dimensiones deben ser positivas")

        print(f"\n  Ingresa los elementos fila por fila (separados por espacios):")
        data = []
        for i in range(rows):
            while True:
                try:
                    row_input = input(f"    Fila {i + 1}: ")
                    row = [float(x) for x in row_input.split()]
                    if len(row) != cols:
                        print(f"    ❌ Error: Se esperaban {cols} elementos")
                        continue
                    data.append(row)
                    break
                except ValueError:
                    print("    ❌ Error: Ingresa números válidos")

        return Matrix(data)

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        return None


def print_header():
    """Imprime el encabezado"""
    print("\n" + "=" * 70)
    print("                   CALCULADORA DE MATRICES")
    print("=" * 70)


def print_menu():
    """Imprime el menú principal"""
    print("\n📋 OPERACIONES DISPONIBLES:")
    print("\n  Operaciones con dos matrices:")
    print("    1. Sumar matrices")
    print("    2. Restar matrices")
    print("    3. Multiplicar matrices")

    print("\n  Operaciones con una matriz:")
    print("    4. Multiplicar por escalar")
    print("    5. Transponer matriz")
    print("    6. Calcular determinante")
    print("    7. Calcular inversa")
    print("    8. Calcular rango")
    print("    9. Calcular traza")
    print("    10. Elevar a potencia")

    print("\n  Matrices especiales:")
    print("    11. Generar matriz identidad")
    print("    12. Generar matriz de ceros")

    print("\n    0. Salir")


def main():
    while True:
        clear_screen()
        print_header()
        print_menu()

        try:
            choice = input("\n➤ Selecciona una opción: ")

            if choice == "0":
                print("\n¡Hasta luego! 👋\n")
                break

            elif choice == "1":  # Sumar
                A = read_matrix("primera matriz (A)")
                if A is None:
                    continue
                B = read_matrix("segunda matriz (B)")
                if B is None:
                    continue

                result = A.add(B)
                print("\n✅ RESULTADO (A + B):")
                print(result)

            elif choice == "2":  # Restar
                A = read_matrix("primera matriz (A)")
                if A is None:
                    continue
                B = read_matrix("segunda matriz (B)")
                if B is None:
                    continue

                result = A.subtract(B)
                print("\n✅ RESULTADO (A - B):")
                print(result)

            elif choice == "3":  # Multiplicar
                A = read_matrix("primera matriz (A)")
                if A is None:
                    continue
                B = read_matrix("segunda matriz (B)")
                if B is None:
                    continue

                result = A.multiply(B)
                print("\n✅ RESULTADO (A × B):")
                print(result)

            elif choice == "4":  # Escalar
                A = read_matrix()
                if A is None:
                    continue
                scalar = float(input("\n  Ingresa el escalar: "))

                result = A.scalar_multiply(scalar)
                print(f"\n✅ RESULTADO ({scalar} × A):")
                print(result)

            elif choice == "5":  # Transponer
                A = read_matrix()
                if A is None:
                    continue

                result = A.transpose()
                print("\n✅ MATRIZ TRANSPUESTA (Aᵀ):")
                print(result)

            elif choice == "6":  # Determinante
                A = read_matrix()
                if A is None:
                    continue

                det = A.determinant()
                print(f"\n✅ DETERMINANTE: {det:.6g}")

            elif choice == "7":  # Inversa
                A = read_matrix()
                if A is None:
                    continue

                inverse = A.inverse()
                print("\n✅ MATRIZ INVERSA (A⁻¹):")
                print(inverse)

                # Verificación
                verification = A.multiply(inverse)
                print("\n🔍 Verificación (A × A⁻¹ ≈ I):")
                print(verification)

            elif choice == "8":  # Rango
                A = read_matrix()
                if A is None:
                    continue

                rank = A.rank()
                print(f"\n✅ RANGO: {rank}")

            elif choice == "9":  # Traza
                A = read_matrix()
                if A is None:
                    continue

                trace = A.trace()
                print(f"\n✅ TRAZA: {trace:.6g}")

            elif choice == "10":  # Potencia
                A = read_matrix()
                if A is None:
                    continue
                n = int(input("\n  Ingresa la potencia (puede ser negativa): "))

                result = A.power(n)
                print(f"\n✅ RESULTADO (A^{n}):")
                print(result)

            elif choice == "11":  # Identidad
                n = int(input("\n  Tamaño de la matriz identidad: "))
                result = Matrix.identity(n)
                print(f"\n✅ MATRIZ IDENTIDAD ({n}×{n}):")
                print(result)

            elif choice == "12":  # Ceros
                rows = int(input("\n  Número de filas: "))
                cols = int(input("  Número de columnas: "))
                result = Matrix.zeros(rows, cols)
                print(f"\n✅ MATRIZ DE CEROS ({rows}×{cols}):")
                print(result)

            else:
                print("\n❌ Opción inválida")

        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")

        input("\n Presiona Enter para continuar...")


if __name__ == "__main__":
    main()