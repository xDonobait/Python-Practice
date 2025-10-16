#!/usr/bin/env python3

import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Any


class MiniDatabase:
    def __init__(self, db_name="minidb.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Conectado a la base de datos: {self.db_name}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("Conexion cerrada")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al ejecutar query: {e}")
            return False

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener datos: {e}")
            return []

    def create_table(self, table_name, columns):
        columns_def = ", ".join([f"{col[0]} {col[1]}" for col in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        if self.execute_query(query):
            print(f"Tabla '{table_name}' creada exitosamente")
            return True
        return False

    def drop_table(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        if self.execute_query(query):
            print(f"Tabla '{table_name}' eliminada")
            return True
        return False

    def list_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = self.fetch_all(query)
        if tables:
            print("\nTablas en la base de datos:")
            print("-" * 40)
            for table in tables:
                print(f"- {table[0]}")
            return [t[0] for t in tables]
        else:
            print("No hay tablas en la base de datos")
            return []

    def describe_table(self, table_name):
        query = f"PRAGMA table_info({table_name})"
        columns = self.fetch_all(query)
        if columns:
            print(f"\nEstructura de la tabla '{table_name}':")
            print("-" * 60)
            print(f"{'ID':<5} {'Nombre':<20} {'Tipo':<15} {'Not Null':<10} {'PK':<5}")
            print("-" * 60)
            for col in columns:
                print(f"{col[0]:<5} {col[1]:<20} {col[2]:<15} {col[3]:<10} {col[5]:<5}")
            return columns
        else:
            print(f"Tabla '{table_name}' no existe")
            return []

    def insert_data(self, table_name, data):
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        if self.execute_query(query, data):
            print(f"Datos insertados en '{table_name}'")
            return True
        return False

    def insert_dict(self, table_name, data_dict):
        columns = ", ".join(data_dict.keys())
        placeholders = ", ".join(["?" for _ in data_dict])
        values = tuple(data_dict.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        if self.execute_query(query, values):
            print(f"Datos insertados en '{table_name}'")
            return True
        return False

    def select_all(self, table_name, limit=None):
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        results = self.fetch_all(query)

        if results:
            columns_info = self.fetch_all(f"PRAGMA table_info({table_name})")
            column_names = [col[1] for col in columns_info]

            print(f"\nDatos de la tabla '{table_name}':")
            print("-" * 80)
            print(" | ".join([f"{name:<15}" for name in column_names]))
            print("-" * 80)
            for row in results:
                print(" | ".join([f"{str(val):<15}" for val in row]))
            print(f"\nTotal: {len(results)} registro(s)")
        else:
            print(f"No hay datos en la tabla '{table_name}'")

        return results

    def update_data(self, table_name, set_clause, where_clause, params):
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        if self.execute_query(query, params):
            print(f"Datos actualizados en '{table_name}'")
            print(f"Filas afectadas: {self.cursor.rowcount}")
            return True
        return False

    def delete_data(self, table_name, where_clause, params=None):
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        if self.execute_query(query, params):
            print(f"Datos eliminados de '{table_name}'")
            print(f"Filas afectadas: {self.cursor.rowcount}")
            return True
        return False

    def custom_query(self, query, params=None):
        query_lower = query.lower().strip()

        if query_lower.startswith("select"):
            results = self.fetch_all(query, params)
            if results:
                print(f"\nResultados ({len(results)} fila(s)):")
                print("-" * 80)
                for row in results:
                    print(row)
                return results
            else:
                print("No se encontraron resultados")
                return []
        else:
            if self.execute_query(query, params):
                print(f"Query ejecutada exitosamente")
                print(f"Filas afectadas: {self.cursor.rowcount}")
                return True
            return False

    def export_to_csv(self, table_name, filename):
        results = self.fetch_all(f"SELECT * FROM {table_name}")
        if not results:
            print(f"No hay datos para exportar en '{table_name}'")
            return False

        columns_info = self.fetch_all(f"PRAGMA table_info({table_name})")
        column_names = [col[1] for col in columns_info]

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(column_names)
                writer.writerows(results)
            print(f"Datos exportados a '{filename}'")
            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False

    def import_from_csv(self, table_name, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)

                for row in reader:
                    self.insert_data(table_name, row)

            print(f"Datos importados desde '{filename}'")
            return True
        except Exception as e:
            print(f"Error al importar: {e}")
            return False

    def export_to_json(self, table_name, filename):
        results = self.fetch_all(f"SELECT * FROM {table_name}")
        if not results:
            print(f"No hay datos para exportar en '{table_name}'")
            return False

        columns_info = self.fetch_all(f"PRAGMA table_info({table_name})")
        column_names = [col[1] for col in columns_info]

        data = []
        for row in results:
            data.append(dict(zip(column_names, row)))

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Datos exportados a '{filename}'")
            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False

    def get_row_count(self, table_name):
        result = self.fetch_all(f"SELECT COUNT(*) FROM {table_name}")
        if result:
            count = result[0][0]
            print(f"Total de registros en '{table_name}': {count}")
            return count
        return 0


def print_menu():
    print("\n" + "=" * 60)
    print("MINI BASE DE DATOS SQL")
    print("=" * 60)
    print("1. Crear tabla")
    print("2. Eliminar tabla")
    print("3. Listar tablas")
    print("4. Ver estructura de tabla")
    print("5. Insertar datos")
    print("6. Ver todos los datos de una tabla")
    print("7. Actualizar datos")
    print("8. Eliminar datos")
    print("9. Ejecutar query SQL personalizada")
    print("10. Contar registros")
    print("11. Exportar tabla a CSV")
    print("12. Importar datos desde CSV")
    print("13. Exportar tabla a JSON")
    print("0. Salir")
    print("=" * 60)


def main():
    db_name = input("Nombre de la base de datos (por defecto: minidb.db): ").strip()
    if not db_name:
        db_name = "minidb.db"

    db = MiniDatabase(db_name)

    while True:
        print_menu()
        choice = input("\nSelecciona una opcion: ").strip()

        if choice == '1':
            print("\n--- CREAR TABLA ---")
            table_name = input("Nombre de la tabla: ").strip()
            num_columns = int(input("Numero de columnas: "))

            columns = []
            print("\nTipos disponibles: INTEGER, TEXT, REAL, BLOB")
            print("Restricciones: PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT valor")

            for i in range(num_columns):
                print(f"\nColumna {i + 1}:")
                col_name = input("  Nombre: ").strip()
                col_type = input("  Tipo: ").strip().upper()
                col_constraints = input("  Restricciones (opcional): ").strip()

                col_def = f"{col_type} {col_constraints}".strip()
                columns.append((col_name, col_def))

            db.create_table(table_name, columns)

        elif choice == '2':
            table_name = input("\nNombre de la tabla a eliminar: ").strip()
            confirm = input(f"Estas seguro de eliminar '{table_name}'? (s/n): ").strip().lower()
            if confirm == 's':
                db.drop_table(table_name)

        elif choice == '3':
            db.list_tables()

        elif choice == '4':
            table_name = input("\nNombre de la tabla: ").strip()
            db.describe_table(table_name)

        elif choice == '5':
            print("\n--- INSERTAR DATOS ---")
            table_name = input("Nombre de la tabla: ").strip()

            columns_info = db.fetch_all(f"PRAGMA table_info({table_name})")
            if not columns_info:
                print(f"Tabla '{table_name}' no existe")
                continue

            print("\nColumnas de la tabla:")
            for col in columns_info:
                print(f"  - {col[1]} ({col[2]})")

            print("\nIngresa los valores:")
            values = []
            for col in columns_info:
                value = input(f"  {col[1]}: ").strip()
                if value.lower() == 'null':
                    values.append(None)
                elif col[2] == 'INTEGER':
                    values.append(int(value) if value else None)
                elif col[2] == 'REAL':
                    values.append(float(value) if value else None)
                else:
                    values.append(value)

            db.insert_data(table_name, values)

        elif choice == '6':
            table_name = input("\nNombre de la tabla: ").strip()
            limit = input("Limite de registros (Enter para todos): ").strip()
            limit = int(limit) if limit else None
            db.select_all(table_name, limit)

        elif choice == '7':
            print("\n--- ACTUALIZAR DATOS ---")
            table_name = input("Nombre de la tabla: ").strip()
            set_clause = input("Clausula SET (ej: nombre = ?, edad = ?): ").strip()
            where_clause = input("Clausula WHERE (ej: id = ?): ").strip()

            print("Ingresa los valores (separados por comas):")
            values_input = input("Valores para SET: ").strip()
            set_values = [v.strip() for v in values_input.split(',')]

            where_input = input("Valores para WHERE: ").strip()
            where_values = [v.strip() for v in where_input.split(',')]

            params = set_values + where_values
            db.update_data(table_name, set_clause, where_clause, params)

        elif choice == '8':
            print("\n--- ELIMINAR DATOS ---")
            table_name = input("Nombre de la tabla: ").strip()
            where_clause = input("Clausula WHERE (ej: id = ?): ").strip()

            values_input = input("Valores para WHERE (separados por comas): ").strip()
            params = [v.strip() for v in values_input.split(',')] if values_input else None

            confirm = input("Estas seguro? (s/n): ").strip().lower()
            if confirm == 's':
                db.delete_data(table_name, where_clause, params)

        elif choice == '9':
            print("\n--- QUERY SQL PERSONALIZADA ---")
            print("Ingresa tu query SQL:")
            query = input().strip()

            params_input = input("Parametros (separados por comas, Enter si no hay): ").strip()
            params = [p.strip() for p in params_input.split(',')] if params_input else None

            db.custom_query(query, params)

        elif choice == '10':
            table_name = input("\nNombre de la tabla: ").strip()
            db.get_row_count(table_name)

        elif choice == '11':
            table_name = input("\nNombre de la tabla: ").strip()
            filename = input("Nombre del archivo CSV: ").strip()
            if not filename.endswith('.csv'):
                filename += '.csv'
            db.export_to_csv(table_name, filename)

        elif choice == '12':
            table_name = input("\nNombre de la tabla: ").strip()
            filename = input("Nombre del archivo CSV: ").strip()
            db.import_from_csv(table_name, filename)

        elif choice == '13':
            table_name = input("\nNombre de la tabla: ").strip()
            filename = input("Nombre del archivo JSON: ").strip()
            if not filename.endswith('.json'):
                filename += '.json'
            db.export_to_json(table_name, filename)

        elif choice == '0':
            db.close()
            print("\nHasta luego!")
            break

        else:
            print("Opcion no valida")

        input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    main()