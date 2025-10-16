import random
import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple


class Move(Enum):
    ROCK = "piedra"
    PAPER = "papel"
    SCISSORS = "tijera"


class GameResult(Enum):
    WIN = "victoria"
    LOSE = "derrota"
    TIE = "empate"


class GameStats:
    def __init__(self):
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.move_history = []
        self.results_history = []
        self.start_date = datetime.now().strftime("%Y-%m-%d")

    def add_game(self, player_move: Move, computer_move: Move, result: GameResult):
        self.games_played += 1
        self.move_history.append((player_move.value, computer_move.value))
        self.results_history.append(result.value)

        if result == GameResult.WIN:
            self.wins += 1
        elif result == GameResult.LOSE:
            self.losses += 1
        else:
            self.ties += 1

    def get_win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return (self.wins / self.games_played) * 100

    def get_favorite_move(self) -> str:
        if not self.move_history:
            return "Ninguno"

        moves_count = {}
        for player_move, _ in self.move_history:
            moves_count[player_move] = moves_count.get(player_move, 0) + 1

        return max(moves_count, key=moves_count.get).capitalize()

    def to_dict(self) -> Dict:
        return {
            'games_played': self.games_played,
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'move_history': self.move_history,
            'results_history': self.results_history,
            'start_date': self.start_date
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'GameStats':
        stats = cls()
        stats.games_played = data.get('games_played', 0)
        stats.wins = data.get('wins', 0)
        stats.losses = data.get('losses', 0)
        stats.ties = data.get('ties', 0)
        stats.move_history = data.get('move_history', [])
        stats.results_history = data.get('results_history', [])
        stats.start_date = data.get('start_date', datetime.now().strftime("%Y-%m-%d"))
        return stats


class RockPaperScissorsGame:
    WINNING_COMBINATIONS = {
        Move.ROCK: Move.SCISSORS,
        Move.PAPER: Move.ROCK,
        Move.SCISSORS: Move.PAPER
    }

    MOVE_ICONS = {
        Move.ROCK: "🪨",
        Move.PAPER: "📄",
        Move.SCISSORS: "✂️"
    }

    def __init__(self, stats_file: str = "rps_stats.json"):
        self.stats_file = stats_file
        self.stats = self.load_stats()
        self.computer_strategy = "random"

    def load_stats(self) -> GameStats:
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return GameStats.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                print("⚠️  Error al cargar estadísticas. Iniciando nuevas.")
        return GameStats()

    def save_stats(self):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error al guardar estadísticas: {e}")

    def get_computer_move(self) -> Move:
        if self.computer_strategy == "random":
            return random.choice(list(Move))
        elif self.computer_strategy == "adaptive":
            return self._get_adaptive_move()
        elif self.computer_strategy == "counter":
            return self._get_counter_move()
        else:
            return random.choice(list(Move))

    def _get_adaptive_move(self) -> Move:
        if len(self.stats.move_history) < 3:
            return random.choice(list(Move))

        recent_moves = [move[0] for move in self.stats.move_history[-3:]]
        most_common = max(set(recent_moves), key=recent_moves.count)

        for move, beats in self.WINNING_COMBINATIONS.items():
            if beats.value == most_common:
                return move

        return random.choice(list(Move))

    def _get_counter_move(self) -> Move:
        if not self.stats.move_history:
            return random.choice(list(Move))

        last_player_move = self.stats.move_history[-1][0]

        for move, beats in self.WINNING_COMBINATIONS.items():
            if beats.value == last_player_move:
                return move

        return random.choice(list(Move))

    def determine_winner(self, player_move: Move, computer_move: Move) -> GameResult:
        if player_move == computer_move:
            return GameResult.TIE
        elif self.WINNING_COMBINATIONS[player_move] == computer_move:
            return GameResult.WIN
        else:
            return GameResult.LOSE

    def play_round(self, player_move: Move) -> Tuple[Move, GameResult]:
        computer_move = self.get_computer_move()
        result = self.determine_winner(player_move, computer_move)

        self.stats.add_game(player_move, computer_move, result)
        self.save_stats()

        return computer_move, result

    def reset_stats(self):
        self.stats = GameStats()
        self.save_stats()


class RockPaperScissorsUI:
    def __init__(self):
        self.game = RockPaperScissorsGame()

    def show_title(self):
        print("\n" + "═" * 50)
        print("🎮 PIEDRA, PAPEL O TIJERA")
        print("═" * 50)

    def show_main_menu(self):
        stats = self.game.stats
        print(f"\n📊 Partidas jugadas: {stats.games_played}")
        if stats.games_played > 0:
            print(f"🏆 Victorias: {stats.wins} | ❌ Derrotas: {stats.losses} | 🤝 Empates: {stats.ties}")
            print(f"📈 Tasa de victoria: {stats.get_win_rate():.1f}%")

        print("\n" + "─" * 50)
        print("1. 🎯 Jugar una partida")
        print("2. 🔥 Modo torneo (mejor de 5)")
        print("3. 🤖 Cambiar dificultad de IA")
        print("4. 📊 Ver estadísticas detalladas")
        print("5. 🗑️  Reiniciar estadísticas")
        print("6. 🚪 Salir")
        print("─" * 50)

    def get_player_move(self) -> Move:
        print("\n🎯 Elige tu jugada:")
        print("  1. 🪨 Piedra")
        print("  2. 📄 Papel")
        print("  3. ✂️  Tijera")

        while True:
            try:
                choice = input("\n👉 Tu elección (1-3): ").strip()
                if choice == '1':
                    return Move.ROCK
                elif choice == '2':
                    return Move.PAPER
                elif choice == '3':
                    return Move.SCISSORS
                else:
                    print("❌ Opción inválida. Elige 1, 2 o 3.")
            except (ValueError, KeyboardInterrupt):
                print("❌ Entrada inválida.")

    def show_round_result(self, player_move: Move, computer_move: Move, result: GameResult):
        player_icon = self.game.MOVE_ICONS[player_move]
        computer_icon = self.game.MOVE_ICONS[computer_move]

        print(f"\n🎭 RESULTADO:")
        print(f"  Tú:        {player_icon} {player_move.value.upper()}")
        print(f"  Máquina:   {computer_icon} {computer_move.value.upper()}")
        print("  " + "─" * 30)

        if result == GameResult.WIN:
            print("  🎉 ¡GANASTE! 🏆")
        elif result == GameResult.LOSE:
            print("  😔 Perdiste... 💔")
        else:
            print("  🤝 ¡EMPATE! 🤝")

    def play_single_game(self):
        print("\n🚀 ¡Nueva partida!")

        player_move = self.get_player_move()
        computer_move, result = self.game.play_round(player_move)

        self.show_round_result(player_move, computer_move, result)

    def play_tournament(self):
        print("\n🏟️  MODO TORNEO - Mejor de 5 rondas")
        print("─" * 40)

        player_score = 0
        computer_score = 0
        round_num = 1

        while player_score < 3 and computer_score < 3:
            print(f"\n🎯 RONDA {round_num}")
            print(f"Marcador: Tú {player_score} - {computer_score} Máquina")

            player_move = self.get_player_move()
            computer_move, result = self.game.play_round(player_move)

            self.show_round_result(player_move, computer_move, result)

            if result == GameResult.WIN:
                player_score += 1
            elif result == GameResult.LOSE:
                computer_score += 1

            round_num += 1

            if player_score < 3 and computer_score < 3:
                input("\n📱 Presiona Enter para la siguiente ronda...")

        print("\n" + "═" * 40)
        if player_score > computer_score:
            print("🏆 ¡GANASTE EL TORNEO! 🎉")
        else:
            print("😔 La máquina ganó el torneo... 💔")
        print(f"Resultado final: {player_score} - {computer_score}")
        print("═" * 40)

    def change_ai_difficulty(self):
        print("\n🤖 CONFIGURACIÓN DE IA")
        print("─" * 25)
        print("1. 😴 Fácil (Aleatorio)")
        print("2. 🧠 Medio (Adaptativo)")
        print("3. 🔥 Difícil (Contador)")

        current = self.game.computer_strategy
        print(f"\nModo actual: {current.upper()}")

        choice = input("\n👉 Selecciona dificultad (1-3): ").strip()

        if choice == '1':
            self.game.computer_strategy = "random"
            print("✅ Dificultad cambiada a FÁCIL")
        elif choice == '2':
            self.game.computer_strategy = "adaptive"
            print("✅ Dificultad cambiada a MEDIO")
        elif choice == '3':
            self.game.computer_strategy = "counter"
            print("✅ Dificultad cambiada a DIFÍCIL")
        else:
            print("❌ Opción inválida")

    def show_detailed_stats(self):
        stats = self.game.stats

        print("\n📊 ESTADÍSTICAS DETALLADAS")
        print("═" * 35)

        if stats.games_played == 0:
            print("💭 No hay partidas jugadas aún")
            return

        print(f"📅 Jugando desde: {stats.start_date}")
        print(f"🎮 Total de partidas: {stats.games_played}")
        print(f"🏆 Victorias: {stats.wins}")
        print(f"❌ Derrotas: {stats.losses}")
        print(f"🤝 Empates: {stats.ties}")
        print(f"📈 Tasa de victoria: {stats.get_win_rate():.1f}%")
        print(f"⭐ Jugada favorita: {stats.get_favorite_move()}")

        if stats.games_played > 0:
            print("\n🎯 Progreso:")
            wins_bars = int(stats.get_win_rate() / 5)
            progress_bar = "█" * wins_bars + "░" * (20 - wins_bars)
            print(f"  [{progress_bar}] {stats.get_win_rate():.1f}%")

        if len(stats.results_history) >= 5:
            recent_results = stats.results_history[-5:]
            result_icons = {"victoria": "🏆", "derrota": "❌", "empate": "🤝"}
            recent_display = " ".join([result_icons[r] for r in recent_results])
            print(f"\n📝 Últimos 5 resultados: {recent_display}")

    def reset_stats_confirm(self):
        print("\n🗑️  REINICIAR ESTADÍSTICAS")
        print("─" * 25)
        print("⚠️  Esto eliminará todas tus estadísticas")

        confirm = input("¿Estás seguro? (escribe 'CONFIRMAR'): ")
        if confirm == 'CONFIRMAR':
            self.game.reset_stats()
            print("✅ Estadísticas reiniciadas")
        else:
            print("↩️  Operación cancelada")

    def run(self):
        print("🚀 Bienvenido a Piedra, Papel o Tijera")

        while True:
            try:
                self.show_title()
                self.show_main_menu()

                choice = input("👉 Selecciona una opción (1-6): ").strip()

                if choice == '1':
                    self.play_single_game()
                elif choice == '2':
                    self.play_tournament()
                elif choice == '3':
                    self.change_ai_difficulty()
                elif choice == '4':
                    self.show_detailed_stats()
                elif choice == '5':
                    self.reset_stats_confirm()
                elif choice == '6':
                    print("\n👋 ¡Gracias por jugar!")
                    print("📊 Tus estadísticas están guardadas en rps_stats.json")
                    break
                else:
                    print("❌ Opción inválida. Selecciona del 1 al 6.")

                input("\n📱 Presiona Enter para continuar...")

            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"⚠️  Error inesperado: {e}")


if __name__ == "__main__":
    game = RockPaperScissorsUI()
    game.run()