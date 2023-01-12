import os, platform


class RenderEngine():

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.render()

    def clear(self):
        self.render()
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def render(self):
        self.framebuffer = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(" ")
            self.framebuffer.append(row)

    def show(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.framebuffer[y][x], end="")
            print()


class Painter():

    def __init__(self, engine: RenderEngine, auto_scaled_contents = True) -> None:
        self.engine = engine
        self.density = 1
        self.auto_scaled_contents = auto_scaled_contents

    def adapt_coords(self, x: float, y: float):
        x = round(x + self.engine.width // 2)
        y = round(self.engine.height // 2 - y)
        return x, y

    def draw_point(self, x: float, y: float, char: str = "O"):
        if self.auto_scaled_contents:
            (x, y) = self.scale_contents((x, y))
        x, y = self.adapt_coords(x, y)
        if 0 <= x < self.engine.width and 0 <= y < self.engine.height:
            self.engine.framebuffer[y][x] = char

    def draw_line(self, point_1: tuple, point_2: tuple):
        lerp = lambda a, b, t: a + (b - a) * t
        x1, y1 = point_1
        x2, y2 = point_2
        iterations = max(abs(x2 - x1), abs(y2 - y1)) * self.density
        for t in range(iterations):
            t /= iterations
            x = lerp(x1, x2, t)
            y = lerp(y1, y2, t)
            self.draw_point(x, y)
        self.draw_point(x2, y2)

    def draw(self, *points):
        for point in points:
            self.draw_point(*point)

    def transform(self, point, scale = 1):
        if scale != 1:
            point = [scale * component for component in point]

        return tuple(point)

    def scale_contents(self, point):
        ratio = 2.4
        return tuple([point[0] * ratio, point[1]])


class Object(list):

    def __init__(self, start_x: float, start_y: float, chars: str) -> None:
        super().__init__()
        dy = 0
        for row in chars.splitlines():
            dx = 0
            for char in row:
                self.append((start_x + dx, start_y + dy, char))
                dx += 1
            dy += 1


class Game():

    def __init__(self, width: int, height: int, setup, loop) -> None:
        self.engine = RenderEngine(width, height)
        t = 0
        while True:
            setup({
                "engine": self.engine,
            })
            loop({
                "t": t,
                "engine": self.engine,
            })
            self.engine.show()
            t += 1
    