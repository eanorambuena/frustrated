import numpy as np
import keyboard

from fr.controls import dual_control, quad_control
from fr.engine2d import RenderEngine, Painter
from fr.engine3d import Camera3d, Object3d


if __name__ == "__main__":
    speed = 0.1
    dx = 0
    dy = 0
    dz = 0

    path = "cube.obj"
    camera = Camera3d()
    engine = RenderEngine(800, 200)
    painter = Painter(engine)
    model = Object3d(path, [0, 0, 0], [])

    while True:
        dx, dy = quad_control(dx, dy, speed)
        dz = dual_control(dz, speed)
        model.position = [dx, dy, dz]

        engine.clear()

        model_positions = []
        for point in model.points:
            position = camera.calculate_point(point)
            point = painter.transform(position, scale = 50)
            model_positions.append(tuple([point[0], point[1]]))
        
        for edge in model.edge_buffer:
            for count, value in enumerate(edge):
                if count == len(edge) - 1:
                    continue
    
                i, j = model_positions[value]
                x, y = model_positions[edge[count + 1]]
                painter.draw_line((int(i), int(j)), (int(x), int(y)))
        
        painter.draw(*model_positions)
        engine.show()
