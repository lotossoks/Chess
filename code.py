from copy import deepcopy

# Константы цвета
WHITE = 1
BLACK = 2


# Обратный цвет
def opponent(color):
    return WHITE if color == BLACK else BLACK


# Вывод доски
def print_board(board):
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


# Координата в доске?
def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


# Базовый класс фигур
class Figure:

    def __init__(self, color):
        # Цвет фигуры
        self.color = color
        # Ходи ла ли раньше фигура?
        self.not_step_bef = True

    # Возвращение цвета фигуры
    def get_color(self):
        return self.color


# Пешка
class Pawn(Figure):

    # Краткое название (Дальше не пишу)
    def char(self):
        return "P"

    # Превращение пешки в другую фигуру на конце доски
    def change_pawn_to(self):
        char = input("Замена пешки на (Q - Ферзь; N - Конь; B - Слон; R - Ладья) -> \t")
        board.field[row][col] = Queen(self.color) if char == "Q" else \
            Knight(self.color) if char == "N" else \
                Bishop(self.color) if char == "B" else \
                    Rook(self.color)

    # Корректен ли ход на пустую клетку? (Дальше не пишу)
    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False
        if self.color == WHITE:
            direction, start_row = 1, 1
        else:
            direction, start_row = -1, 6
        if (row + direction == row1) or \
                (row == start_row and row + 2 * direction == row1 and board.field[row + direction][col] is None):
            if row + direction == 7 if self.color == WHITE else row + direction == 0:
                self.change_pawn_to()
            return True
        return False

    # Корректен ли ход на занятую клетку? (Дальше не пишу)
    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        if (row + direction == row1 and (col + 1 == col1 or col - 1 == col1)) and \
                (row + direction == 7 if self.color == WHITE else row + direction == 0):
            self.change_pawn_to()
        return (row + direction == row1) and (col + 1 == col1 or col - 1 == col1)


# Конь
class Knight(Figure):

    def char(self):
        return "N"

    def can_move(self, board, row, col, row1, col1):
        delta_row, delta_col = abs(row - row1), abs(col - col1)
        return (delta_row == 2 and delta_col == 1) or (delta_row == 1 and delta_col == 2)

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


# Ладья
class Rook(Figure):

    def char(self):
        return "R"

    def can_move(self, board, row, col, row1, col1):
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            if not (board.get_piece(row, c) is None):
                return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


# Слон
class Bishop(Figure):

    def char(self):
        return "B"

    def can_move(self, board, row, col, row1, col1):
        delta_row, delta_col = abs(row - row1), abs(col - col1)
        if delta_row - delta_col == 0:
            prov_row, prov_col = row, col
            step, step2 = 1 if (row1 > row) else -1, 1 if (col1 > col) else -1
            for _ in range(delta_row - 1):
                prov_row += step
                prov_col += step2
                if not (board.get_piece(prov_row, prov_col) is None):
                    return False
            return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


# Ферзь
class Queen(Figure):

    def char(self):
        return "Q"

    def can_move(self, board, row, col, row1, col1):
        if abs(row - row1) - abs(col - col1) == 0:
            return Bishop(self.color).can_move(board, row, col, row1, col1)
        if row == row1 or col == col1:
            return Rook(self.color).can_move(board, row, col, row1, col1)
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

# Король
class King(Figure):

    def char(self):
        return "K"

    def can_move(self, board, row, col, row1, col1):
        delta_row, delta_col = abs(row - row1), abs(col - col1)
        return delta_row + delta_col == 1 or delta_col * delta_row == 1

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

# Доска
class Board:

    # Вывод доски
    def __str__(self):
        print_board(self)
        return " "

    def __init__(self):
        # Начальная позиция королей
        self.pos_kings = {WHITE: [0, 4], BLACK: [7, 4]}
        # Цвет игрока ходящего
        self.color = WHITE
        # Поле
        self.field = [[None] * 8 for _ in range(8)]
        # Начальная расстановка фигур
        self.field[0] = [
            Rook(WHITE),
            Knight(WHITE),
            Bishop(WHITE),
            Queen(WHITE),
            King(WHITE),
            Bishop(WHITE),
            Knight(WHITE),
            Rook(WHITE)
        ]
        self.field[1] = [Pawn(WHITE)] * 8
        self.field[6] = [Pawn(BLACK)] * 8
        self.field[7] = [
            Rook(BLACK),
            Knight(BLACK),
            Bishop(BLACK),
            Queen(BLACK),
            King(BLACK),
            Bishop(BLACK),
            Knight(BLACK),
            Rook(BLACK)
        ]

    # Цвет игрока ходящего
    def current_player_color(self):
        return self.color

    # Какая фигура в клетке (row, col)
    def get_piece(self, row, col):
        return self.field[row][col]

    # Отображение фигуры
    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        return 'w' + piece.char() if piece.get_color() == WHITE else 'b' + piece.char()

    # Проверка на шах
    def king_is_under_attack(self, row, col, row1, col1, pos_king):
        will_board = deepcopy(board)
        will_board.field[row1][col1] = will_board.field[row][col]
        will_board.field[row][col] = None
        for i in range(8):
            for j in range(8):
                if will_board.field[i][j] is not None:
                    piece = will_board.field[i][j]
                    if piece.can_attack(will_board, i, j, pos_king[0], pos_king[1]):
                        if piece.get_color() == opponent(self.color):
                            print("Король будет под ударом!")
                            return True

        return False

    # Ход
    def move_piece(self, row, col, row1, col1):
        if (not correct_coords(row, col) or not correct_coords(row1, col1)) or (row == row1 and col == col1):
            return False
        piece = self.field[row][col]
        if (piece is None) or (piece.get_color() != self.color):
            return False
        if self.king_is_under_attack(row, col, row1, col1, self.pos_kings[self.color]):
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(board, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            return piece.can_attack(board, row, col, row1, col1)
        # Рокировка
        elif piece.char() == "K" and self.field[row1][col1].char() == "R" and self.field[row1][col1].not_step_bef:
            if abs(col1 - col) == 4:
                for i in range(1, 4):
                    if board.field[row][i]:
                        return False
                board.field[row][col], board.field[row1][col1] = None, None
                board.field[row][2], board.field[row][3] = King(self.color), Rook(self.color)
            else:
                for i in range(5, 7):
                    if board.field[row][i]:
                        return False
                board.field[row][col], board.field[row1][col1] = None, None
                board.field[row][6], board.field[row][5] = King(self.color), Rook(self.color)
            return True
        else:
            return False
        piece.not_step_bef = False 
        if piece.char == "K":
            self.pos_kings[self.color] = [row1, col1]
        self.field[row1][col1] = self.field[row][col]
        self.field[row][col] = None
        self.color = opponent(self.color)
        return True


board = Board()
while True:
    print(board)
    print('Команды:')
    print('    exit                               -- выход')
    print('    move <col> <row> <col1> <row1>     -- ход из клетки (row, col)')
    print('                                          в клетку (row1, col1)')
    if board.current_player_color() == WHITE:
        print('Ход белых:')
    else:
        print('Ход черных:')
    command = input()
    if command == 'exit':
        break
    col, row, col1, row1 = list(map(int, command.split()))
    if board.move_piece(row, col, row1, col1):
        print('Ход успешен')
    else:
        print('Координаты некорректны! Попробуйте другой ход!')
