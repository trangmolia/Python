import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        clist = CellList(self.cell_height, self.cell_width, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist: list) -> None:
        white = (255, 255, 255)
        green = (0, 128, 0)

        for cell in clist:
            x1 = cell.col * self.cell_size
            y1 = cell.row * self.cell_size
            x2 = self.cell_size
            y2 = self.cell_size
            if cell.is_alive():
                pygame.draw.rect(self.screen, green, (x1, y1, x2, y2))
            else:
                pygame.draw.rect(self.screen, white, (x1, y1, x2, y2))


class Cell:

    def __init__(self, row: int, col: int, state=0):
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self) -> int:
        return self.state

    def __repr__(self):
        return str(int(self.state))


class CellList():

    def __init__(self, nrows: int, ncols: int, randomize=False, ok=False):
        self.nrows = nrows
        self.ncols = ncols

        if ok:
            return

        if randomize:
            self.clist = [[Cell] * ncols for _ in range(nrows)]
            for i in range(nrows):
                for j in range(ncols):
                    self.clist[i][j] = Cell(i, j, random.randint(0, 1))

        else:
            self.clist = [[Cell] * ncols for _ in range(nrows)]
            for i in range(nrows):
                for j in range(ncols):
                    self.clist[i][j] = Cell(i, j, 0)

    def get_neighbours(self, cell: Cell) -> list:
        neighbours = []
        row, col = cell.row, cell.col
        max_row = self.nrows - 1
        max_col = self.ncols - 1

        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i < 0 or j < 0 or i > max_row or j > max_col:
                    continue
                elif (i, j) != (row, col):
                    neighbours.append(self.clist[i][j])
        return neighbours

    def update(self) -> list:
        new_clist = deepcopy(self.clist)

        for i in new_clist:
            for cell in i:
                neighbours = self.get_neighbours(cell)
                sum = 0
                for value in neighbours:
                        sum += value.state
                if sum == 3 and cell.state == 0:
                    cell.state = 1
                elif (sum == 2 or sum == 3) and cell.state == 1:
                    cell.state = 1
                else:
                    cell.state = 0
        self.clist = new_clist
        return self

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:

            r = 0
            matrix = []

            for line in f:
                c = 0
                arr = []
                for ch in line:
                    if ch == '0' or ch == '1':
                        arr.append(Cell(r, c, int(ch)))
                    c += 1
                matrix.append(arr)
                r += 1

        cls.r_max = r
        cls.c_max = c - 1
        cls.clist = matrix

        return CellList(cls.r_max, cls.c_max, False, ok=True)

    def __iter__(self):
        self.row = 0
        self.col = 0
        return self

    def __next__(self) -> int:
        if self.row < self.nrows:
            if self.col < self.ncols:
                cell = self.clist[self.row][self.col]
            if self.col == self.ncols - 1:
                self.row += 1
                self.col = 0
            else:
                self.col += 1
            return cell
        else:
            raise StopIteration

    def __str__(self) -> str:
        str = ''
        for i in range(self.nrows):
            for j in range(self.ncols):
                if (self.clist[i][j].is_alive()):
                    str += '1'
                else:
                    str += '0'
            str += '\n'
        return str
