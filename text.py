from sympy import plot_parametric, symbols

from engine2d import Painter, RenderEngine


class Text(list):

    def __init__(self, x = 0, y = 0, size = 10) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.t = symbols("t")
        self.density = 3.2
        self.inword_gap = 0.5
        self.string = ""
        self.abstract_painter = Painter(RenderEngine(1, 1))

    def append(self, char: str, plot_char = False) -> None:
        bezier_buffer = []
        with open(f"font/{char}.efn", "r") as file:
            for line in file:
                if line.startswith("#"):
                    continue
                bezier_buffer.append([[float(component) for component in point.split(",")] for point in line.split(" ")])

        t = self.t
        beziers = []

        for i in range(len(bezier_buffer)):
            p0, p1, p2 = tuple(bezier_buffer[i])
            beziers += [(
                    (p0[0] * (1 - t) + p1[0] * t) * (1 - t) + (p1[0] * (1 - t) + p2[0] * t) * t,
                    (p0[1] * (1 - t) + p1[1] * t) * (1 - t) + (p1[1] * (1 - t) + p2[1] * t) * t
                )]
            
            def bezier(t):
                return (
                    (p0[0] * (1 - t) + p1[0] * t) * (1 - t) + (p1[0] * (1 - t) + p2[0] * t) * t,
                    (p0[1] * (1 - t) + p1[1] * t) * (1 - t) + (p1[1] * (1 - t) + p2[1] * t) * t
                )

            iterations = int(self.size ** 2 * self.density)
            for t in range(iterations):
                t /= iterations
                x, y = bezier(t)
                x, y = self.abstract_painter.transform((x + self.x, y + self.y), self.size)
                super().append((x, y))
        
        if plot_char:
            plot_parametric(*beziers, (t, 0, 1))

        self.x += (1 + self.inword_gap) * self.size
        self.string += char

    def __str__(self) -> str:
        return self.string