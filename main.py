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

        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

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

        self.draw_snakes_and_ladders()

    def draw_snakes_and_ladders(self):
        for start, end in self.snakes.items():
            self.draw_line(start, end, 'red')
        for start, end in self.ladders.items():
            self.draw_line(start, end, 'green')

    def draw_line(self, start, end, color):
        start_x, start_y = self.get_coordinates(start)
        end_x, end_y = self.get_coordinates(end)
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=5, arrow=tk.LAST)

    def get_coordinates(self, position):
        row = (position - 1) // 10
        col = (position - 1) % 10
        if row % 2 == 0:
            x = col * 50 + 25
        else:
            x = (9 - col) * 50 + 25
        y = (9 - row) * 50 + 25
        return x, y

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

        new_position = self.snakes.get(new_position, new_position)
        new_position = self.ladders.get(new_position, new_position)

        self.player_positions[player] = new_position
        self.update_ui()

        self.current_player = 2 if self.current_player == 1 else 1
        self.info_label.config(text=f"Player {self.current_player}'s Turn")

    def update_ui(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakesAndLadders(root)
    root.mainloop()
