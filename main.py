import pygame as pg
import const
from cylinder import Cylinder


def main() -> None:
    pg.init()
    pg.display.set_caption("Cylinder")
    screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
    screen.fill(const.WHITE)
    clock = pg.time.Clock()

    cylinder = Cylinder(size=(const.WIDTH, const.HEIGHT))

    running = True
    while running:
        screen.fill(const.WHITE)
        clock.tick(const.FPS)

        screen.blit(cylinder, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        cylinder.update()
        pg.display.flip()


if __name__ == "__main__":
    main()
