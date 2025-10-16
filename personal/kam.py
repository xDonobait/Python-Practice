import tkinter as tk
from tkinter import font
import random


class RomanticMessage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Para Kam")
        self.root.geometry("800x600")
        self.root.configure(bg='#FFE5E5')

        self.canvas = tk.Canvas(self.root, bg='#FFE5E5', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.hearts = []
        self.messages = [
            "Cada momento contigo es especial",
            "Eres la razon de mi sonrisa cada dia",
            "Tu presencia ilumina mi vida",
            "Contigo todo es mejor",
            "Gracias por ser parte de mi vida",
            "Te amo con todo mi ser"
        ]

        self.current_message = 0
        self.heart_symbols = ['♥', '❤', '💕', '💖', '💗', '💓', '💞', '💝', '🐸']

        self.title_label = None
        self.message_label = None
        self.footer_label = None

        self.setup_ui()
        self.animate()

    def setup_ui(self):
        title_font = font.Font(family='Arial', size=32, weight='bold')
        message_font = font.Font(family='Arial', size=18)

        self.title_label = tk.Label(
            self.root,
            text="Para: Kam ♥",
            font=title_font,
            bg='#FFE5E5',
            fg='#FF1493'
        )
        self.title_label.place(relx=0.5, rely=0.15, anchor='center')

        self.message_label = tk.Label(
            self.root,
            text="",
            font=message_font,
            bg='#FFE5E5',
            fg='#FF69B4',
            wraplength=600
        )
        self.message_label.place(relx=0.5, rely=0.5, anchor='center')

        self.footer_label = tk.Label(
            self.root,
            text="♥♥♥ Te quiero mucho ♥♥♥",
            font=font.Font(family='Arial', size=16, weight='bold'),
            bg='#FFE5E5',
            fg='#FF1493'
        )
        self.footer_label.place(relx=0.5, rely=0.85, anchor='center')

    def create_heart(self):
        x = random.randint(0, 800)
        y = random.randint(-50, 0)
        symbol = random.choice(self.heart_symbols)
        size = random.randint(20, 40)
        color = random.choice(['#FF1493', '#FF69B4', '#FFB6C1', '#FF6B9D'])

        heart = self.canvas.create_text(
            x, y,
            text=symbol,
            font=('Arial', size),
            fill=color
        )

        speed = random.uniform(1, 3)
        self.hearts.append({'id': heart, 'speed': speed, 'x': x})

    def update_hearts(self):
        for heart in self.hearts[:]:
            coords = self.canvas.coords(heart['id'])
            if coords:
                new_y = coords[1] + heart['speed']

                if new_y > 650:
                    self.canvas.delete(heart['id'])
                    self.hearts.remove(heart)
                else:
                    wobble = random.uniform(-0.5, 0.5)
                    self.canvas.coords(heart['id'], coords[0] + wobble, new_y)

        if random.random() < 0.3:
            self.create_heart()

    def cycle_messages(self):
        if self.message_label:
            self.message_label.config(text=self.messages[self.current_message])
            self.current_message = (self.current_message + 1) % len(self.messages)
            self.root.after(3000, self.cycle_messages)

    def pulse_title(self):
        if self.title_label:
            current_font = self.title_label['font']
            if isinstance(current_font, str):
                current_size = 32
            else:
                current_size = current_font.cget('size')

            new_size = 32 if current_size == 34 else 34

            self.title_label.config(
                font=font.Font(family='Arial', size=new_size, weight='bold')
            )
            self.root.after(500, self.pulse_title)

    def animate(self):
        self.update_hearts()
        self.root.after(50, self.animate)

    def run(self):
        self.cycle_messages()
        self.pulse_title()

        for _ in range(20):
            self.create_heart()

        self.root.mainloop()


if __name__ == "__main__":
    app = RomanticMessage()
    app.run()