#!/usr/bin/env python3

import time
import threading
import os
import sys


class Stopwatch:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.running = False
        self.paused = False
        self.pause_time = 0
        self.lap_times = []

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.paused = False
            self.pause_time = 0
            self.lap_times = []
        elif self.paused:
            self.pause_time += time.time() - self.end_time
            self.paused = False

    def pause(self):
        if self.running and not self.paused:
            self.end_time = time.time()
            self.paused = True

    def stop(self):
        if self.running:
            if not self.paused:
                self.end_time = time.time()
            self.running = False
            self.paused = False

    def reset(self):
        self.start_time = None
        self.end_time = None
        self.running = False
        self.paused = False
        self.pause_time = 0
        self.lap_times = []

    def lap(self):
        if self.running and not self.paused:
            current_time = self.get_elapsed_time()
            self.lap_times.append(current_time)
            return current_time
        return None

    def get_elapsed_time(self):
        if not self.start_time:
            return 0

        if self.running and not self.paused:
            return time.time() - self.start_time - self.pause_time
        elif self.paused:
            return self.end_time - self.start_time - self.pause_time
        else:
            return self.end_time - self.start_time - self.pause_time


class Timer:

    def __init__(self):
        self.duration = 0
        self.start_time = None
        self.running = False
        self.paused = False
        self.pause_time = 0
        self.callback = None
        self.thread = None

    def set_timer(self, hours=0, minutes=0, seconds=0):
        self.duration = hours * 3600 + minutes * 60 + seconds
        return self.duration

    def start(self, callback=None):
        if self.duration > 0 and not self.running:
            self.start_time = time.time()
            self.running = True
            self.paused = False
            self.pause_time = 0
            self.callback = callback

            self.thread = threading.Thread(target=self._run_timer)
            self.thread.daemon = True
            self.thread.start()

    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            self.pause_time += time.time() - self.start_time

    def resume(self):
        if self.running and self.paused:
            self.start_time = time.time()
            self.paused = False

    def stop(self):
        self.running = False
        self.paused = False

    def reset(self):
        self.stop()
        self.start_time = None
        self.pause_time = 0

    def get_remaining_time(self):
        if not self.running:
            return self.duration

        if self.paused:
            elapsed = self.pause_time
        else:
            elapsed = time.time() - self.start_time + self.pause_time

        remaining = max(0, self.duration - elapsed)
        return remaining

    def _run_timer(self):
        while self.running:
            if not self.paused:
                remaining = self.get_remaining_time()
                if remaining <= 0:
                    self.running = False
                    if self.callback:
                        self.callback()
                    break
            time.sleep(0.1)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"


def format_time_simple(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def timer_finished():
    print("\n" + "=" * 50)
    print("           ⏰ ¡TIEMPO TERMINADO! ⏰")
    print("=" * 50)
    print("¡BEEP! ¡BEEP! ¡BEEP!")
    input("Presiona ENTER para continuar...")


def stopwatch_interface():
    stopwatch = Stopwatch()

    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("              CRONÓMETRO")
        print("=" * 50)

        if stopwatch.running and not stopwatch.paused:
            elapsed = stopwatch.get_elapsed_time()
            status = "CORRIENDO"
        elif stopwatch.paused:
            elapsed = stopwatch.get_elapsed_time()
            status = "PAUSADO"
        else:
            elapsed = 0
            status = "DETENIDO"

        print(f"Estado: {status}")
        print(f"Tiempo: {format_time(elapsed)}")

        if stopwatch.lap_times:
            print("\nVueltas:")
            for i, lap in enumerate(stopwatch.lap_times, 1):
                print(f"  Vuelta {i}: {format_time(lap)}")

        print("\n" + "-" * 50)
        print("Comandos:")
        print("  1 - Iniciar/Reanudar")
        print("  2 - Pausar")
        print("  3 - Vuelta (Lap)")
        print("  4 - Detener")
        print("  5 - Reiniciar")
        print("  0 - Volver al menú")
        print("-" * 50)

        try:
            command = input("Selecciona una opción: ").strip()

            if command == "1":
                if not stopwatch.running or stopwatch.paused:
                    stopwatch.start()

            elif command == "2":
                if stopwatch.running and not stopwatch.paused:
                    stopwatch.pause()

            elif command == "3":
                lap_time = stopwatch.lap()
                if lap_time:
                    print(f"Vuelta {len(stopwatch.lap_times)} marcada: {format_time(lap_time)}")
                    input("Presiona ENTER para continuar...")
                else:
                    print("El cronómetro debe estar corriendo")
                    input("Presiona ENTER para continuar...")

            elif command == "4":
                stopwatch.stop()

            elif command == "5":
                stopwatch.reset()

            elif command == "0":
                break

            else:
                print("Opción no válida")
                input("Presiona ENTER para continuar...")

        except KeyboardInterrupt:
            break


def timer_interface():
    timer = Timer()

    clear_screen()
    print("\n" + "=" * 50)
    print("              TEMPORIZADOR")
    print("=" * 50)

    try:
        hours = int(input("Horas (0-23): ") or 0)
        minutes = int(input("Minutos (0-59): ") or 0)
        seconds = int(input("Segundos (0-59): ") or 0)

        if hours < 0 or minutes < 0 or seconds < 0:
            print("Error: Los valores no pueden ser negativos")
            input("Presiona ENTER para continuar...")
            return

        total_seconds = timer.set_timer(hours, minutes, seconds)

        if total_seconds == 0:
            print("Error: Debe establecer un tiempo mayor a cero")
            input("Presiona ENTER para continuar...")
            return

        while True:
            clear_screen()
            print("\n" + "=" * 50)
            print("              TEMPORIZADOR")
            print("=" * 50)

            if timer.running and not timer.paused:
                remaining = timer.get_remaining_time()
                status = "CORRIENDO"
                if remaining <= 0:
                    print("Estado: TERMINADO")
                    print("Tiempo restante: 00:00:00")
                    timer_finished()
                    break
            elif timer.paused:
                remaining = timer.get_remaining_time()
                status = "PAUSADO"
            else:
                remaining = timer.duration
                status = "DETENIDO"

            print(f"Estado: {status}")
            print(f"Tiempo restante: {format_time_simple(remaining)}")

            print("\n" + "-" * 50)
            print("Comandos:")
            print("  1 - Iniciar/Reanudar")
            print("  2 - Pausar")
            print("  3 - Detener")
            print("  4 - Reiniciar")
            print("  0 - Volver al menú")
            print("-" * 50)

            command = input("Selecciona una opción: ").strip()

            if command == "1":
                if not timer.running:
                    timer.start(timer_finished)
                elif timer.paused:
                    timer.resume()

            elif command == "2":
                if timer.running and not timer.paused:
                    timer.pause()

            elif command == "3":
                timer.stop()

            elif command == "4":
                timer.reset()
                timer.set_timer(hours, minutes, seconds)

            elif command == "0":
                timer.stop()
                break

            else:
                print("Opción no válida")
                input("Presiona ENTER para continuar...")

    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
        input("Presiona ENTER para continuar...")
    except KeyboardInterrupt:
        pass


def show_main_menu():
    clear_screen()
    print("\n" + "=" * 50)
    print("        TEMPORIZADOR Y CRONÓMETRO")
    print("=" * 50)
    print("1. Cronómetro")
    print("2. Temporizador")
    print("3. Salir")
    print("-" * 50)


def main():
    while True:
        show_main_menu()
        choice = input("Selecciona una opción: ").strip()

        if choice == '1':
            stopwatch_interface()
        elif choice == '2':
            timer_interface()
        elif choice == '3':
            print("¡Gracias por usar la aplicación!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            input("Presiona ENTER para continuar...")


if __name__ == "__main__":
    main()