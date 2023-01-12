from controls import dual_control, quad_control
from engine2d import RenderEngine, Painter
from engine3d import Camera3d, Object3d


if __name__ == "__main__":
    speed = 0.1
    dx = 0
    dy = 0
    dz = 0
    dd = 0
    dr = 0

    path = "cube.eobj"
    camera = Camera3d()
    engine = RenderEngine(300, 120)
    painter = Painter(engine)
    model = Object3d(path, [0, 0, 0], [])

    while True:
        dx, dy = quad_control(dx, dy, speed)
        dz = dual_control(dz, speed)
        dd = int(dual_control(dd, 1, "k", "j"))
        dr = int(dual_control(dr, 1, "t", "r"))
        painter.density = 1 + dd
        model.position = [dx, dy, dz]
        model.rotation = [dr]

        engine.clear()

        model_positions = []
        for index, point in enumerate(model.points):
            position = camera.calculate_point(point)
            point = painter.transform(position, scale = 50)
            model_positions.append(tuple([point[0], point[1], str(index + 1)]))

        for index, edge in enumerate(model.eobj_edge_buffer):
            vertex_1 = model_positions[index]
            for neighbor in edge:
                vertex_2 = model_positions[neighbor]
                painter.draw_line((int(vertex_1[0]), int(vertex_1[1])), (int(vertex_2[0]), int(vertex_2[1])))
        
        painter.draw(*model_positions)
        for char in _01.chars:
            painter.draw(*char)
        engine.show()
