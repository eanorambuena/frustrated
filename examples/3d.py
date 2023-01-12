import numpy as np
import keyboard

from fr.engine2d import RenderEngine, Painter
from fr.engine3d import Camera3d


if __name__ == "__main__":
    cube_vertex_buffer = [
        np.array([ 1., -1., -1.]),
        np.array([ 1., -1.,  1.]),
        np.array([-1., -1.,  1.]),
        np.array([-1., -1., -1.]),
        np.array([ 1.,  1., -1.]),
        np.array([ 1.,  1.,  1.]),
        np.array([-1.,  1.,  1.]),
        np.array([-1.,  1., -1.]),
    ]
    speed = 0.1
    dx = 0
    dy = 0
    dz = 0

    camera = Camera3d()
    engine = RenderEngine(200, 100)
    painter = Painter(engine)

    while True:
        if keyboard.is_pressed("a"):
            dx -= speed
        if keyboard.is_pressed("d"):
            dx += speed
        if keyboard.is_pressed("w"):
            dy += speed
        if keyboard.is_pressed("s"):
            dy -= speed
        if keyboard.is_pressed("z"):
            dz += speed
        if keyboard.is_pressed("x"):
            dz -= speed

        cube_positions = []
        for vertex in cube_vertex_buffer:
            vertex_copy = vertex.copy() + np.array([dx, dy, dz])
            position = camera.calculate_point(vertex_copy)
            point = painter.transform(position, scale = 10)
            cube_positions.append(point)
        
        engine.clear()
        painter.draw(*cube_positions)
        engine.show()
