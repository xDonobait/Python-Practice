import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pendiente"
    COMPLETED = "completada"


class Task:
    def __init__(self, id: int, description: str, created_at: str = None):
        self.id = id
        self.description = description
        self.status = TaskStatus.PENDING
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = None

    def complete(self):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status.value,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(data['id'], data['description'], data['created_at'])
        if data['status'] == TaskStatus.COMPLETED.value:
            task.status = TaskStatus.COMPLETED
            task.completed_at = data.get('completed_at')
        return task

    def __str__(self) -> str:
        status_icon = "✓" if self.status == TaskStatus.COMPLETED else "○"
        return f"[{self.id:2d}] {status_icon} {self.description}"


class TodoManager:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
                print(f"✓ Cargadas {len(self.tasks)} tareas desde {self.filename}")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠ Error al cargar tareas: {e}")
                print("Iniciando con lista vacía")
        else:
            print("📝 Archivo de tareas no encontrado. Iniciando con lista vacía.")

    def save_tasks(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f,
                          ensure_ascii=False, indent=2)
            print(f"✓ Tareas guardadas en {self.filename}")
        except Exception as e:
            print(f"⚠ Error al guardar tareas: {e}")

    def add_task(self, description: str) -> Task:
        if not description.strip():
            raise ValueError("La descripción de la tarea no puede estar vacía")

        task = Task(self.next_id, description.strip())
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def complete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.complete()
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False

    def list_tasks(self, status_filter: Optional[TaskStatus] = None) -> List[Task]:
        if status_filter:
            return [task for task in self.tasks if task.status == status_filter]
        return self.tasks

    def search_tasks(self, query: str) -> List[Task]:
        query = query.lower()
        return [task for task in self.tasks
                if query in task.description.lower()]

    def get_stats(self) -> Dict:
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.status == TaskStatus.COMPLETED)
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': completion_rate
        }


class TodoCLI:
    def __init__(self):
        self.manager = TodoManager()

    def show_menu(self):
        stats = self.manager.get_stats()

        print("\n" + "─" * 60)
        print("  📋 GESTOR DE TAREAS")
        if stats['total'] > 0:
            print(f"  {stats['completed']}/{stats['total']} completadas • {stats['pending']} pendientes")
        print("─" * 60)

        menu_items = [
            ("1", "Agregar nueva tarea", "➕"),
            ("2", "Ver todas las tareas", "📝"),
            ("3", "Ver tareas pendientes", "⏳"),
            ("4", "Ver tareas completadas", "✅"),
            ("5", "Marcar como completada", "☑️"),
            ("6", "Eliminar tarea", "🗑️"),
            ("7", "Buscar tareas", "🔍"),
            ("8", "Ver estadísticas", "📊"),
            ("9", "Salir", "🚪")
        ]

        for num, desc, icon in menu_items:
            print(f"  {num}. {icon}  {desc}")

        print("─" * 60)

    def add_task_interactive(self):
        try:
            print("\n➕ AGREGAR NUEVA TAREA")
            print("─" * 25)
            description = input("  📝 Descripción: ").strip()
            if not description:
                print("  ⚠️  La descripción no puede estar vacía")
                return

            task = self.manager.add_task(description)
            print(f"  ✅ Tarea creada exitosamente")
            print(f"  📋 [{task.id}] {task.description}")
        except ValueError as e:
            print(f"  ❌ Error: {e}")

    def list_tasks_formatted(self, tasks: List[Task], title: str):
        print(f"\n{title}")
        print("─" * len(title))

        if not tasks:
            print("  💭 No hay tareas para mostrar")
            return

        for i, task in enumerate(sorted(tasks, key=lambda t: t.id), 1):
            status_icon = "✓" if task.status == TaskStatus.COMPLETED else "○"
            status_color = "✅" if task.status == TaskStatus.COMPLETED else "⏳"

            print(f"  {i:2d}. [{task.id:2d}] {status_icon} {task.description}")

            created = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
            created_str = created.strftime("%d/%m/%Y")

            if task.status == TaskStatus.COMPLETED and task.completed_at:
                completed = datetime.strptime(task.completed_at, "%Y-%m-%d %H:%M:%S")
                completed_str = completed.strftime("%d/%m/%Y")
                print(f"      📅 {created_str} → ✅ {completed_str}")
            else:
                print(f"      📅 {created_str}")
            print()

    def complete_task_interactive(self):
        pending_tasks = self.manager.list_tasks(TaskStatus.PENDING)
        if not pending_tasks:
            print("\n  🎉 ¡No hay tareas pendientes!")
            return

        print("\n☑️  COMPLETAR TAREA")
        print("─" * 20)
        print("  Tareas pendientes:")
        for task in pending_tasks[:5]:
            print(f"    [{task.id}] {task.description}")
        if len(pending_tasks) > 5:
            print(f"    ... y {len(pending_tasks) - 5} más")

        try:
            task_id = int(input("\n  🔢 ID de la tarea: "))
            if self.manager.complete_task(task_id):
                print(f"  ✅ Tarea {task_id} completada")
            else:
                print(f"  ⚠️  Tarea {task_id} no encontrada o ya está completada")
        except ValueError:
            print("  ❌ Por favor, ingresa un número válido")

    def delete_task_interactive(self):
        if not self.manager.tasks:
            print("\n  📭 No hay tareas para eliminar")
            return

        print("\n🗑️  ELIMINAR TAREA")
        print("─" * 18)

        recent_tasks = self.manager.tasks[-5:] if len(self.manager.tasks) > 5 else self.manager.tasks
        for task in recent_tasks:
            status = "✅" if task.status == TaskStatus.COMPLETED else "⏳"
            print(f"    [{task.id}] {status} {task.description}")

        try:
            task_id = int(input("\n  🔢 ID de la tarea: "))
            task = self.manager.get_task(task_id)
            if task:
                print(f"  📋 '{task.description}'")
                confirm = input("  ❓ ¿Confirmar eliminación? (s/N): ")
                if confirm.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                    if self.manager.delete_task(task_id):
                        print(f"  ✅ Tarea eliminada")
                    else:
                        print(f"  ❌ Error al eliminar")
                else:
                    print("  ↩️  Operación cancelada")
            else:
                print(f"  ⚠️  Tarea {task_id} no encontrada")
        except ValueError:
            print("  ❌ Por favor, ingresa un número válido")

    def search_tasks_interactive(self):
        print("\n🔍 BUSCAR TAREAS")
        print("─" * 16)
        query = input("  📝 Texto a buscar: ").strip()
        if not query:
            print("  ⚠️  Debes ingresar un texto para buscar")
            return

        results = self.manager.search_tasks(query)
        if results:
            self.list_tasks_formatted(results, f"🔍 Resultados para '{query}' ({len(results)} encontradas):")
        else:
            print(f"  💭 No se encontraron tareas con '{query}'")

    def show_stats(self):
        stats = self.manager.get_stats()
        print("\n📊 ESTADÍSTICAS")
        print("─" * 30)
        print(f"  📋 Total de tareas:    {stats['total']:3d}")
        print(f"  ✅ Completadas:       {stats['completed']:3d}")
        print(f"  ⏳ Pendientes:        {stats['pending']:3d}")
        print(f"  📈 Progreso:      {stats['completion_rate']:5.1f}%")

        if stats['total'] > 0:
            print("\n  Barra de progreso:")
            completed_bars = int(stats['completion_rate'] / 5)
            remaining_bars = 20 - completed_bars
            progress_bar = "█" * completed_bars + "░" * remaining_bars
            print(f"  [{progress_bar}]")
            print(f"  {stats['completion_rate']:.1f}% completado")

        print("─" * 30)

    def run(self):
        print("🚀 Bienvenido al Gestor de Tareas")
        print("   Una herramienta simple y eficiente")

        while True:
            try:
                self.show_menu()
                choice = input("  👉 Selecciona una opción: ").strip()

                if choice == '1':
                    self.add_task_interactive()
                elif choice == '2':
                    tasks = self.manager.list_tasks()
                    self.list_tasks_formatted(tasks, f"📝 TODAS LAS TAREAS ({len(tasks)} total)")
                elif choice == '3':
                    tasks = self.manager.list_tasks(TaskStatus.PENDING)
                    self.list_tasks_formatted(tasks, f"⏳ TAREAS PENDIENTES ({len(tasks)} pendientes)")
                elif choice == '4':
                    tasks = self.manager.list_tasks(TaskStatus.COMPLETED)
                    self.list_tasks_formatted(tasks, f"✅ TAREAS COMPLETADAS ({len(tasks)} completadas)")
                elif choice == '5':
                    self.complete_task_interactive()
                elif choice == '6':
                    self.delete_task_interactive()
                elif choice == '7':
                    self.search_tasks_interactive()
                elif choice == '8':
                    self.show_stats()
                elif choice == '9':
                    print("\n  👋 ¡Gracias por usar el Gestor de Tareas!")
                    print("  📝 Tus datos están guardados en tasks.json")
                    break
                else:
                    print("  ❌ Opción no válida. Selecciona del 1 al 9.")

                input("\n  📱 Presiona Enter para continuar...")

            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"⚠ Error inesperado: {e}")


if __name__ == "__main__":
    app = TodoCLI()
    app.run()