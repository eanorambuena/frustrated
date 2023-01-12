from fr.text import Text, FontStyle
from fr.controls import recognizer_control, dual_control, switch_control
from fr.engine2d import RenderEngine, Painter

if __name__ == "__main__":
    engine = RenderEngine(300, 70)
    dw = 4
    dweight = "italic"

    while True:
        engine.clear()
        painter = Painter(engine)
        dw = dual_control(dw, 1)
        dweight = switch_control(dweight, FontStyle().keys())

        text = Text("Vale", x = -7, y = 0, size = 4)
        text.set_bold_style(dweight)
        text.set_underline(True)
        text.inword_gap = 0.1
        text.weight = dw
        painter.draw(*text)

        engine.show()
