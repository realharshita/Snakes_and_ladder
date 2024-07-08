import tkinter as tk
from random import randint

class SnakesAndLadders:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes and Ladders")
        self.root.geometry("600x700")
        self.create_board()
        self.create_ui_elements()
        self.current_player = 1

    def create_board(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg='white')
        self.canvas.pack(pady=20)

        size = 50
        for i in range(10):
            for j in range(10):
                x1 = j * size
                y1 = i * size
                x2 = x1 + size
                y2 = y1 + size

                color = 'lightblue' if (i + j) % 2 == 0 else 'white'
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill=color)

                if i % 2 == 0:
                    num = 100 - (i * 10 + j)
                else:
                    num = 100 - (i * 10 + (9 - j))
                self.canvas.create_text(x1 + size/2, y1 + size/2, text=str(num))

    def create_ui_elements(self):
        self.info_label = tk.Label(self.root, text="Player 1's Turn", font=("Helvetica", 16))
        self.info_label.pack(pady=10)

        self.roll_button = tk.Button(self.root, text="Roll Dice", command=self.roll_dice, font=("Helvetica", 16))
        self.roll_button.pack(pady=10)

        self.dice_result_label = tk.Label(self.root, text="Dice Result: ", font=("Helvetica", 16))
        self.dice_result_label.pack(pady=10)

        self.player_positions = {1: 1, 2: 1} 

    def roll_dice(self):
        result = randint(1, 6)
        self.dice_result_label.config(text=f"Dice Result: {result}")
        self.move_player(result)

    def move_player(self, steps):
        player = self.current_player
        current_position = self.player_positions[player]
        new_position = current_position + steps

        if new_position > 100:
            new_position = current_position  

        self.player_positions[player] = new_position
        self.update_ui()

        self.current_player = 2 if self.current_player == 1 else 1
        self.info_label.config(text=f"Player {self.current_player}'s Turn")

    def update_ui(self):
        pass  # Placeholder

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakesAndLadders(root)
    root.mainloop()