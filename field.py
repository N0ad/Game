import field_cells as f_s
import objects as obj
import subjects as sbj

import numpy as np
import cv2
import random

class Field():
    "Класс игрового поля"

    map_list = []

    "Стандартные настройки"
    seed = 2431
    levels_counter = 5
    size_map_x_list = [200, 150, 200, 150, 300]
    size_map_y_list = [200, 150, 200, 150, 300]
    min_room_size_list = [5, 5, 5, 5, 10]
    min_room_size_list = [12, 9, 12, 10, 25]
    boss_mode_list = [0, 0, 0, 0, 1]
    boss_room_size_list = [0, 0, 0, 0, 40]
    rooms_count_list = [10, 7, 9, 6, 15]
    actual_map = 0
    map_changed = True

    "Стандартные текстуры"
    void_texture =  np.zeros([4, 4, 3], np.uint8)
    wall_texture = np.zeros([4, 4, 3], np.uint8)
    wall_texture[:, :, 0] = np.zeros([4, 4]) + 17
    wall_texture[:, :, 1] = np.zeros([4, 4]) + 56
    wall_texture[:, :, 2] = np.zeros([4, 4]) + 80
    floor_texture = np.zeros([4, 4, 3], np.uint8)
    floor_texture[:, :, 0] = np.zeros([4, 4]) + 52
    floor_texture[:, :, 1] = np.zeros([4, 4]) + 52
    floor_texture[:, :, 2] = np.zeros([4, 4]) + 52

    "Стандартные типы клеток"
    void_cell = f_s.Cell("Void", -1, void_texture)
    floor_cell = f_s.Cell("Floor", 1, floor_texture)
    wall_cell = f_s.Cell("Wall", 0, wall_texture)

    def __init__(self, name):
        self.name = name
        random.seed(self.seed)

    def generate_levels(self):
        for i in range(self.levels_counter):
            self.generate_map(i, "cave")

    def show_map(self):
        actual_map = self.actual_map
        if self.map_changed: ## проверка на смену уровня
            self.res_map_texture = np.zeros([4 * self.size_map_y_list[actual_map], 4 * self.size_map_x_list[actual_map], 3], np.uint8)
            self.map_changed = False
        for y in range(self.size_map_y_list[actual_map]):
            for x in range(self.size_map_x_list[actual_map]):
                if self.map_list[actual_map][y][x].changed: ##проверка на наличие изменений в клетке
                    self.res_map_texture[y*4:y*4+4, x*4:x*4+4] = self.map_list[actual_map][y][x].texture
        self.map_list[actual_map][y][x].changed = False
        
        cv2.imshow("Game", self.res_map_texture)
        cv2.waitKey(0)
            

    def generate_map(self, map_number, generate_mode):
        self.map_list.append([[self.void_cell] * self.size_map_x_list[map_number] for i in range(self.size_map_y_list[map_number])])
        if generate_mode == "dungeon":
            a = 1

        if generate_mode == "cave":
            random_field = np.random.rand(self.size_map_y_list[map_number] * 3 + 6, self.size_map_x_list[map_number] * 3 + 6) ## генерация случайного шума
            random_field = cv2.blur(random_field, (3, 3)) ## размытие шума
            random_field = cv2.resize(random_field, (self.size_map_y_list[map_number] + 2, self.size_map_x_list[map_number] + 2)) ## сжатие шума до размера игрового поля
            ## создание рамок в шуме для проверки 
            for y in range(self.size_map_y_list[map_number]):
                random_field[y][0] = 0
                random_field[y][self.size_map_x_list[map_number] + 1] = 0
            for x in range(self.size_map_x_list[map_number]):
                random_field[0][x] = 0
                random_field[self.size_map_y_list[map_number] + 1][x] = 0

            ## создание игрового поля на основе шума
            for y in range(1, self.size_map_y_list[map_number] + 1):
                for x in range(1, self.size_map_x_list[map_number] + 1):
                    if random_field[y][x] > 0.5:
                        self.map_list[map_number][y-1][x-1] = self.floor_cell
                    elif (random_field[y-1][x] > 0.5) or (random_field[y-1][x-1] > 0.5) or (random_field[y-1][x+1] > 0.5) or (random_field[y][x-1] > 0.5) or (random_field[y+1][x] > 0.5) or (random_field[y+1][x-1] > 0.5) or (random_field[y-1][x+1] > 0.5) or (random_field[y+1][x] > 0.5):
                        self.map_list[map_number][y-1][x-1] = self.wall_cell
            
