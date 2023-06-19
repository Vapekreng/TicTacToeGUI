import tkinter
import tkinter as tk
from tkinter.messagebox import showinfo

GAME_NAME = 'Крестики-нолики'
FIELD_SIZE = 3
INIT_FIELD = [[None, None, None], [None, None, None], [None, None, None]]
INIT_FIELD_ROW = 2
INIT_FIELD_COLUMN = 0
MAX_COUNTER = 9
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
PADS = 20
INIT_IMAGE_PATH = '0.png'
FIRST_PLAYER_IMAGE = '1.png'
SECOND_PLAYER_IMAGE = '2.png'
INPUT_NAMES_TITLE = 'Ввод имени игроков'
DEFAULT_NAMES = ['Игрок 1', 'Игрок 2']
SIGNS = [' (X)', ' (O)']
TURN_MESSAGE = 'Сейчас ходит '
WIN_MESSAGE_TITLE = 'Победа!'
DRAW_MESSAGE_TITLE = 'Ничья!'
WIN_MESSAGE = 'Победил '
DRAW_MESSAGE = 'Победила дружба!'
WIN_LINES = [
    [[0, 0], [0, 1], [0, 2]],
    [[1, 0], [1, 1], [1, 2]],
    [[2, 0], [2, 1], [2, 2]],
    [[0, 0], [1, 0], [2, 0]],
    [[0, 1], [1, 1], [2, 1]],
    [[0, 2], [1, 2], [2, 2]],
    [[0, 0], [1, 1], [2, 2]],
    [[2, 0], [1, 1], [0, 2]],
]


def get_names():
    def read_names(event):
        player1 = input_name_1.get()
        if player1:
            players[0] = player1
        player2 = input_name_2.get()
        if player2:
            players[1] = player2
        name_window.destroy()

    name_window = tk.Tk()
    name_window.title(INPUT_NAMES_TITLE)
    name_frame = tkinter.Frame(name_window)
    name_frame.pack(expand=True, padx=PADS, pady=PADS)
    label_name_1 = tk.Label(name_frame, text='Введите имя первого игрока: ')
    label_name_1.grid(row=0, column=0)
    label_name_2 = tk.Label(name_frame, text='Введите имя второго игрока: ')
    label_name_2.grid(row=1, column=0)
    input_name_1 = tk.Entry(name_frame)
    input_name_1.grid(row=0, column=2)
    input_name_2 = tk.Entry(name_frame)
    input_name_2.grid(row=1, column=2)
    button = tk.Button(name_frame, text='OK')
    button.grid(row=2, column=0, columnspan=3)
    button.bind('<Button-1>', read_names)
    players = DEFAULT_NAMES
    name_window.mainloop()
    return players


class Game:

    def __init__(self):
        self.counter = 0
        self.index = 0
        self.field = INIT_FIELD
        self.players_names = get_names()
        self.window = tk.Tk()
        self.window.title(GAME_NAME)
        self.frame = tk.Frame(self.window)
        self.frame.pack(expand=True,padx=PADS, pady=PADS)
        text = TURN_MESSAGE + self.players_names[self.index] + SIGNS[self.index]
        self.active_player_label = tk.Label(self.frame, text=text, height=3)
        self.active_player_label.grid(row=0, column=0, columnspan=3)
        self.init_image = tk.PhotoImage(file=INIT_IMAGE_PATH)
        self.images = [tk.PhotoImage(file=FIRST_PLAYER_IMAGE), tk.PhotoImage(file=SECOND_PLAYER_IMAGE)]
        self._set_buttons()
        self.window.mainloop()

    def _click(self, event):
        index = self.counter % 2
        event.widget.config(image=self.images[index])
        x = event.widget.grid_info()['column'] - INIT_FIELD_COLUMN
        y = event.widget.grid_info()['row'] - INIT_FIELD_ROW
        self.field[y][x] = index
        if self._we_have_a_winner():
            self._print_winner_message()
            self._finish_game()
        else:
            self.counter += 1
            self.index = self.counter % 2
            if self.counter == MAX_COUNTER:
                self._print_draw_message()
                self._finish_game()
            else:
                self._print_active_player()

    def _we_have_a_winner(self):
        answer = False
        for line in WIN_LINES:
            if self._check_line(line):
                answer = True
        return answer

    def _check_line(self, line):
        answer = True
        for title in line:
            x = title[0]
            y = title[1]
            if self.field[x][y] != self.index:
                answer = False
                break
        return answer

    def _set_buttons(self):
        for x in range(FIELD_SIZE):
            for y in range(FIELD_SIZE):
                new_button = tk.Button(self.frame, text="", width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                       image=self.init_image)
                new_button.grid(row=INIT_FIELD_ROW + x, column=INIT_FIELD_COLUMN + y)
                new_button.bind("<Button-1>", self._click)

    def _print_winner_message(self):
        winner = self.players_names[self.index]
        text = WIN_MESSAGE + winner
        showinfo(WIN_MESSAGE_TITLE, text)

    def _print_draw_message(self):
        showinfo(DRAW_MESSAGE_TITLE, DRAW_MESSAGE)


    def _finish_game(self):
        self.window.destroy()

    def _print_active_player(self):
        text = TURN_MESSAGE + self.players_names[self.index] + SIGNS[self.index]
        self.active_player_label['text'] = text



new_game = Game()
