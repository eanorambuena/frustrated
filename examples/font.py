from fr.text import Text, FontStyle
from fr.controls import recognizer_control, dual_control, switch_control
from fr.engine2d import RenderEngine, Painter

if __name__ == "__main__":
    engine = RenderEngine(350, 100)
    dkey = "0"
    dw = 2
    dweight = "none"

    while True:
        engine.clear()
        painter = Painter(engine)
        dkey = recognizer_control(dkey, Text().supported_chars.split(","))
        dw = dual_control(dw, 1)
        dweight = switch_control(dweight, FontStyle().keys())

        digit = Text(size = 5)
        digit.set_bold_style(dweight)
        digit.set_underline(True)
        digit.weight = dw
        digit.append(dkey)
        painter.draw(*digit)

        text = Text(supported_chars.replace(",", ""), x = -25, y = -10, size = 2)

        painter.draw(*text)
        engine.show()
