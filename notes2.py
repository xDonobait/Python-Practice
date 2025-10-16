#!/usr/bin/env python3

import os
import json
import re
from datetime import datetime
from pathlib import Path
import hashlib


class NotesManager:
    def __init__(self, notes_dir="my_notes"):
        self.notes_dir = Path(notes_dir)
        self.notes_dir.mkdir(exist_ok=True)
        self.index_file = self.notes_dir / "index.json"
        self.notes_index = self._load_index()

    def _load_index(self):
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_index(self):
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.notes_index, f, indent=2, ensure_ascii=False)

    def _generate_id(self, title):
        timestamp = datetime.now().isoformat()
        unique_string = f"{title}_{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:8]

    def create_note(self, title, content, tags=None):
        note_id = self._generate_id(title)
        timestamp = datetime.now().isoformat()

        if tags is None:
            tags = []

        note_data = {
            'id': note_id,
            'title': title,
            'created': timestamp,
            'modified': timestamp,
            'tags': tags,
            'filename': f"{note_id}.md"
        }

        note_path = self.notes_dir / note_data['filename']
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.notes_index[note_id] = note_data
        self._save_index()

        print(f"Nota creada: '{title}' (ID: {note_id})")
        return note_id

    def list_notes(self, sort_by='modified'):
        if not self.notes_index:
            print("No hay notas guardadas")
            return []

        notes_list = list(self.notes_index.values())
        notes_list.sort(key=lambda x: x.get(sort_by, ''), reverse=True)

        print(f"\nNotas guardadas ({len(notes_list)}):")
        print("-" * 80)

        for note in notes_list:
            tags_str = f"[{', '.join(note['tags'])}]" if note['tags'] else ""
            modified = datetime.fromisoformat(note['modified']).strftime('%Y-%m-%d %H:%M')
            print(f"ID: {note['id']} | {note['title']}")
            print(f"   {modified} {tags_str}")
            print()

        return notes_list

    def read_note(self, note_id):
        if note_id not in self.notes_index:
            print(f"Nota con ID '{note_id}' no encontrada")
            return None

        note_data = self.notes_index[note_id]
        note_path = self.notes_dir / note_data['filename']

        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print("\n" + "=" * 80)
        print(f"{note_data['title']}")
        print("=" * 80)
        print(f"ID: {note_data['id']}")
        print(f"Creada: {datetime.fromisoformat(note_data['created']).strftime('%Y-%m-%d %H:%M')}")
        print(f"Modificada: {datetime.fromisoformat(note_data['modified']).strftime('%Y-%m-%d %H:%M')}")
        if note_data['tags']:
            print(f"Etiquetas: {', '.join(note_data['tags'])}")
        print("-" * 80)
        print(content)
        print("=" * 80 + "\n")

        return content

    def edit_note(self, note_id, new_content=None, new_title=None, new_tags=None):
        if note_id not in self.notes_index:
            print(f"Nota con ID '{note_id}' no encontrada")
            return False

        note_data = self.notes_index[note_id]
        note_path = self.notes_dir / note_data['filename']

        if new_content is not None:
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

        if new_title is not None:
            note_data['title'] = new_title

        if new_tags is not None:
            note_data['tags'] = new_tags

        note_data['modified'] = datetime.now().isoformat()
        self._save_index()

        print(f"Nota actualizada: '{note_data['title']}'")
        return True

    def delete_note(self, note_id):
        if note_id not in self.notes_index:
            print(f"Nota con ID '{note_id}' no encontrada")
            return False

        note_data = self.notes_index[note_id]
        note_path = self.notes_dir / note_data['filename']

        if note_path.exists():
            note_path.unlink()

        del self.notes_index[note_id]
        self._save_index()

        print(f"Nota eliminada: '{note_data['title']}'")
        return True

    def search_notes(self, query, search_in=['title', 'content', 'tags']):
        results = []
        query_lower = query.lower()

        for note_id, note_data in self.notes_index.items():
            found = False

            if 'title' in search_in and query_lower in note_data['title'].lower():
                found = True

            if 'tags' in search_in and any(query_lower in tag.lower() for tag in note_data['tags']):
                found = True

            if 'content' in search_in:
                note_path = self.notes_dir / note_data['filename']
                with open(note_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if query_lower in content.lower():
                    found = True

            if found:
                results.append(note_data)

        if results:
            print(f"\nResultados de busqueda para '{query}': {len(results)} notas")
            print("-" * 80)
            for note in results:
                tags_str = f"[{', '.join(note['tags'])}]" if note['tags'] else ""
                print(f"ID: {note['id']} | {note['title']} {tags_str}")
        else:
            print(f"No se encontraron resultados para '{query}'")

        return results

    def get_tags_stats(self):
        tags_count = {}

        for note_data in self.notes_index.values():
            for tag in note_data['tags']:
                tags_count[tag] = tags_count.get(tag, 0) + 1

        if tags_count:
            print("\nEtiquetas utilizadas:")
            print("-" * 40)
            for tag, count in sorted(tags_count.items(), key=lambda x: x[1], reverse=True):
                print(f"{tag}: {count} nota(s)")
        else:
            print("No hay etiquetas registradas")

        return tags_count


def print_menu():
    print("\n" + "=" * 50)
    print("SISTEMA DE NOTAS CON MARKDOWN")
    print("=" * 50)
    print("1. Crear nueva nota")
    print("2. Listar todas las notas")
    print("3. Leer nota")
    print("4. Editar nota")
    print("5. Eliminar nota")
    print("6. Buscar notas")
    print("7. Ver estadisticas de etiquetas")
    print("0. Salir")
    print("=" * 50)


def main():
    manager = NotesManager()

    while True:
        print_menu()
        choice = input("\nSelecciona una opcion: ").strip()

        if choice == '1':
            print("\n--- CREAR NUEVA NOTA ---")
            title = input("Titulo: ").strip()
            if not title:
                print("El titulo no puede estar vacio")
                continue

            print("Contenido (escribe 'END' en una linea nueva para terminar):")
            content_lines = []
            while True:
                line = input()
                if line == 'END':
                    break
                content_lines.append(line)
            content = '\n'.join(content_lines)

            tags_input = input("Etiquetas (separadas por comas): ").strip()
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

            manager.create_note(title, content, tags)

        elif choice == '2':
            manager.list_notes()

        elif choice == '3':
            note_id = input("\nID de la nota: ").strip()
            manager.read_note(note_id)

        elif choice == '4':
            note_id = input("\nID de la nota a editar: ").strip()
            if note_id not in manager.notes_index:
                print(f"Nota con ID '{note_id}' no encontrada")
                continue

            print("\nQue deseas editar?")
            print("1. Contenido")
            print("2. Titulo")
            print("3. Etiquetas")
            print("4. Todo")
            edit_choice = input("Opcion: ").strip()

            new_content = None
            new_title = None
            new_tags = None

            if edit_choice in ['1', '4']:
                print("Nuevo contenido (escribe 'END' en una linea nueva para terminar):")
                content_lines = []
                while True:
                    line = input()
                    if line == 'END':
                        break
                    content_lines.append(line)
                new_content = '\n'.join(content_lines)

            if edit_choice in ['2', '4']:
                new_title = input("Nuevo titulo: ").strip()
                if not new_title:
                    new_title = None

            if edit_choice in ['3', '4']:
                tags_input = input("Nuevas etiquetas (separadas por comas): ").strip()
                new_tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

            manager.edit_note(note_id, new_content, new_title, new_tags)

        elif choice == '5':
            note_id = input("\nID de la nota a eliminar: ").strip()
            confirm = input(f"Estas seguro de eliminar esta nota? (s/n): ").strip().lower()
            if confirm == 's':
                manager.delete_note(note_id)

        elif choice == '6':
            query = input("\nTermino de busqueda: ").strip()
            if query:
                manager.search_notes(query)

        elif choice == '7':
            manager.get_tags_stats()

        elif choice == '0':
            print("\nHasta luego!")
            break

        else:
            print("Opcion no valida")

        input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    main()