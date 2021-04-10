import math
import copy
import const

import pygame as pg
import numpy as np


class Cylinder(pg.surface.Surface):
    def __init__(
            self,
            n: int = 20,
            r: float = 2,
            h: float = 2,
            size: tuple[int, int] = (200, 200)
    ) -> None:
        """
        Initialization

        :param n: Number of ribs.
        :param r: Radius.
        :param h: Height.
        :param size: The size of the area on which the sphere will be drawn.
        """
        pg.surface.Surface.__init__(self, size)

        self.speed = 0.02
        self.scale = 600
        self.position = (size[0]//2, size[1]//2)

        self.n = n
        self.h = h
        self.r = math.sqrt(r)
        self.phi = math.pi / self.n
        self.delta_phi = 2 * math.pi / self.n

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        self.points = []
        self.__calculation()

    def __calculation(self) -> None:
        """
        Calculating the points of a sphere.
        """
        points1 = []
        points2 = []

        for i in range(self.n):
            y = self.r * math.sin(self.phi)
            x = self.r * math.cos(self.phi)
            if y > 0:
                points1.append([x, y])
            else:
                points2.append([x, y])
            self.phi += self.delta_phi

        points1.sort()
        points2.sort()

        points_down = points1[::-1] + points2
        points_up = copy.deepcopy(points_down)

        for i in range(self.n):
            points_down[i].insert(1, self.h/2)
            points_up[i].insert(1, -self.h/2)

        self.points = np.array(points_down + points_up, dtype=np.float64)

    def update(self) -> None:
        """
        The function that will be called to redraw the points.
        """
        self.fill(color="white")
        if pg.key.get_pressed()[pg.K_DOWN]:
            self.angle_x -= self.speed
        if pg.key.get_pressed()[pg.K_UP]:
            self.angle_x += self.speed
        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.angle_y -= self.speed
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.angle_y += self.speed
        if pg.key.get_pressed()[pg.K_1]:
            self.angle_z += self.speed
        if pg.key.get_pressed()[pg.K_2]:
            self.angle_z -= self.speed

        rotate_x = np.array([
            [1, 0, 0],
            [0, math.cos(self.angle_x), -math.sin(self.angle_x)],
            [0, math.sin(self.angle_x), math.cos(self.angle_x)]
        ])

        rotate_y = np.array([
            [math.cos(self.angle_y), 0, -math.sin(self.angle_y)],
            [0, 1, 0],
            [math.sin(self.angle_y), 0, math.cos(self.angle_y)]
        ])

        rotate_z = np.array([
            [math.cos(self.angle_z), -math.sin(self.angle_z), 0],
            [math.sin(self.angle_z), math.cos(self.angle_z), 0],
            [0, 0, 1]
        ])

        projection_points = []
        for point in self.points:
            point = np.dot(rotate_y, point)
            point = np.dot(rotate_x, point)
            point = np.dot(rotate_z, point)

            distance = 5
            z = 1 / (distance - point[2])

            projection_matrix = np.array([
                [z, 0, 0],
                [0, z, 0]
            ])
            point = np.dot(projection_matrix, point)

            x = int(point[0] * self.scale) + self.position[0]
            y = int(point[1] * self.scale) + self.position[1]
            projection_points.append((x, y))

        self.__connect_points(projection_points)

    def __connect_points(self, points: list[tuple[int, int]]) -> None:
        """
        Function for connecting dots.

        :param points: List of points to be connected.
        """
        for i in range(self.n):
            pg.draw.line(
                self,
                const.GREEN,
                (points[i][0], points[i][1]),
                (points[(i + 1) % self.n][0], points[(i + 1) % self.n][1])
            )

            pg.draw.line(
                self,
                const.GREEN,
                (points[i + self.n][0], points[i + self.n][1]),
                (points[(i + 1) % self.n + self.n][0], points[(i + 1) % self.n + self.n][1])
            )

            pg.draw.line(
                self,
                const.GREEN,
                (points[i][0], points[i][1]),
                (points[i + self.n][0], points[i + self.n][1])
            )
