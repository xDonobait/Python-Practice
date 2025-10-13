import time
import sys

def print_slow(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_verse(verse, delay=0.05):
    print_slow(verse, delay)
    time.sleep(0.3)


def main():
    print("🎵  REPRODUCIENDO LETRA  🎵")
    time.sleep(1)

    lyrics = [
        "You need me to get that shit together",
        "So we can get together",
        "You need me to get that shit together",
        "So we can get together",
        "You need me to",
        "(Yeah, yeah)",
        "You need me to"
    ]

    for line in lyrics:
        print_verse(line, delay=0.03)

if __name__ == "__main__":
    main()