from text import Text
from controls import recognizer_control
from engine2d import Game, RenderEngine, Painter

if __name__ == "__main__":
    engine = RenderEngine(100, 50)
    dkey = "0"

    while True:
        engine.clear()
        painter = Painter(engine)
        dkey = recognizer_control(dkey, range(0, 6))

        zero = Text(size = 4)
        zero.append(dkey)
        painter.draw(*zero)
        engine.show()
