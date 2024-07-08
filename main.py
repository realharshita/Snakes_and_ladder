import tkinter as tk
from tkinter.colorchooser import askcolor
from random import randint

class SnakesAndLadders:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes and Ladders")
        self.root.geometry("600x750")

        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        
        self.player_count = 2  # Default to 2 players

        self.show_player_selection_screen()

    def show_player_selection_screen(self):
        self.selection_frame = tk.Frame(self.root)
        self.selection_frame.pack(pady=20)

        tk.Label(self.selection_frame, text="Select Number of Players", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.selection_frame, text="1 Player", command=lambda: self.start_game(1), font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.selection_frame, text="2 Players", command=lambda: self.start_game(2), font=("Helvetica", 16)).pack(pady=10)

    def start_game(self, player_count):
        self.player_count = player_count
        self.selection_frame.destroy()

        self.create_board()
        self.create_ui_elements()
        
        self.tokens = {
            1: self.canvas.create_oval(15, 15, 35, 35, fill='blue'),
            2: self.canvas.create_oval(15, 15, 35, 35, fill='red')
        }
        self.player_colors = {1: 'blue', 2: 'red'}
        self.player_positions = {1: 1, 2: 1}
        self.current_player = 1
        self.highlight_current_player()
        self.update_ui()

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

        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game, font=("Helvetica", 16))
        self.reset_button.pack(pady=10)

        self.color_button1 = tk.Button(self.root, text="Player 1 Color", command=lambda: self.choose_color(1), font=("Helvetica", 16))
        self.color_button1.pack(pady=10)

        self.color_button2 = tk.Button(self.root, text="Player 2 Color", command=lambda: self.choose_color(2), font=("Helvetica", 16))
        self.color_button2.pack(pady=10)

        self.player_info_label = tk.Label(self.root, text="Player Positions:", font=("Helvetica", 16))
        self.player_info_label.pack(pady=10)

        self.player_positions_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.player_positions_label.pack()

    def roll_dice(self):
        self.roll_button.config(state='disabled')
        self.animate_dice()

    def animate_dice(self):
        result = randint(1, 6)
        self.dice_result_label.config(text=f"Dice Result: {result}")
        self.root.after(1000, self.move_player, result)

    def move_player(self, steps):
        player = self.current_player
        current_position = self.player_positions[player]
        new_position = current_position + steps

        if new_position > 100:
            new_position = current_position

        new_position = self.snakes.get(new_position, new_position)
        new_position = self.ladders.get(new_position, new_position)

        self.player_positions[player] = new_position
        self.animate_move(player, current_position, new_position)

    def animate_move(self, player, start, end):
        if start < end:
            self.move_step_by_step(player, start, end)
        self.check_win_condition(player, end)

    def move_step_by_step(self, player, start, end):
        if start < end:
            self.player_positions[player] = start + 1
            self.update_ui()
            self.root.after(100, self.move_step_by_step, player, start + 1, end)
        else:
            self.update_ui()

    def check_win_condition(self, player, position):
        if position == 100:
            self.info_label.config(text=f"Player {player} wins!")
            self.roll_button.config(state='disabled')
            self.dice_result_label.config(text="Dice Result: ")
            self.highlight_winner(player)
        else:
            self.current_player = 2 if self.current_player == 1 else 1
            self.info_label.config(text=f"Player {self.current_player}'s Turn")
            self.highlight_current_player()
            if self.current_player == 2 and self.player_count == 1:
                self.root.after(1000, self.roll_dice)
            else:
                self.roll_button.config(state='normal')

    def highlight_current_player(self):
        for player in self.tokens:
            if player == self.current_player:
                self.canvas.itemconfig(self.tokens[player], outline='black', width=3)
            else:
                self.canvas.itemconfig(self.tokens[player], outline='')

    def update_ui(self):
        self.highlight_current_player()
        self.player_positions_label.config(text=f"Player 1: {self.player_positions[1]} | Player 2: {self.player_positions[2]}")
        for player, position in self.player_positions.items():
            x, y = self.get_coordinates(position)
            self.canvas.coords(self.tokens[player], x - 10, y - 10, x + 10, y + 10)
            self.canvas.itemconfig(self.tokens[player], fill=self.player_colors[player])

    def highlight_winner(self, player):
        x, y = self.get_coordinates(100)
        self.canvas.create_text(x, y - 40, text=f"Player {player} Wins!", font=("Helvetica", 16), fill="gold")

    def reset_game(self):
        self.canvas.delete("all")
        self.create_board()
        self.player_positions = {1: 1, 2: 1}
        self.current_player = 1
        self.roll_button.config(state='normal')
        self.update_ui()
        self.info_label.config(text="Player 1's Turn")
        self.dice_result_label.config(text="Dice Result: ")

    def choose_color(self, player):
        color = askcolor()[1]
        if color:
            self.player_colors[player] = color
            self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = SnakesAndLadders(root)
    root.mainloop()
