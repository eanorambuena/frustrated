from sympy import plot_parametric, symbols
from typing import Callable
import math

from fr.engine2d import Painter, RenderEngine


class Text(list):

    def __init__(self, string = "", /, *, x = 0, y = 0, size = 10) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.t = symbols("t")
        self.density = 3.2
        self.weight_layers_density = 0.1
        self.inword_gap = 0.5
        self.underline_gap = 0.2
        self.weight_function = FontStyle()["none"]
        self.weight = 2
        self.string = ""
        self.underlined = False
        self.abstract_painter = Painter(RenderEngine(1, 1))
        for char in string:
            self.append(char)

    def append(self, char: str, plot_char = False) -> None:
        bezier_buffer = []
        with open(f"font/{char}.efn", "r") as file:
            for line in file:
                if line.startswith("#") or line.startswith("\n"):
                    continue
                try:
                    bezier_buffer.append(
                        [
                            [float(component) for component in point.split(",")]
                            for point in line.strip().split(" ")
                        ]
                    )
                except ValueError:
                    raise Exception(f"Some Component in line {line.split(' ')} cannot be converted to float")

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
            for i in range(self.weight - 1):
                for t in range(iterations):
                    t /= iterations
                    x, y = bezier(t)
                    x, y = self.abstract_painter.transform((x + self.x, y + self.y), self.size)
                    super().append(self.apply_weight(x, y, i))

            if self.underlined:
                self.abstract_painter.draw_line(
                    (self.x, self.y - self.underline_gap), (self.x + self.size, self.y - self.underline_gap)
                )
        
        if plot_char:
            plot_parametric(*beziers, (t, 0, 1))

        self.x += (1 + self.inword_gap) * self.size
        self.string += char

    def __str__(self) -> str:
        return self.string

    def set_bold_style(self, weight_style: str):
        if weight_style in FontStyle().keys():
            self.weight_function = FontStyle()[weight_style]

    def set_underline(self, state: bool):
        self.underlined = state

    @property
    def supported_chars(self):
        return "0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,l,V"

    def apply_weight(self, x: float, y: float, index: int):
        return self.weight_function(x, y, index, self.weight_layers_density)


class FontStyle(dict):

    def __init__(self) -> None:
        super().__init__()
        self["none"] = self.around_weight
        self["italic"] = self.italic_weight
        self["left_italic"] = self.left_italic_weight

    def italic_weight(self, x, y, index, density):
        return (x + index * density, y + index * density)

    def left_italic_weight(self, x, y, index, density):
        return (x - index * density, y + index * density)

    def around_weight(self, x, y, index, density):
        return (
            x + math.cos(index * math.pi / 2) * index * density,
            y + math.sin(index * math.pi / 2) * index * density
        )
