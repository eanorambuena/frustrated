import math

from engine2d import Game, RenderEngine, Painter, Object


if __name__ == "__main__":
    with open("sprite_1.txt", "r") as f:
        sprite_1 = f.read()

    def setup(args):
        engine: RenderEngine = args["engine"]

        painter = Painter(engine)
        engine.clear()
        painter.draw_line((0, 0), (10, 15))

    def loop(args):
        t: int               = args["t"]
        engine: RenderEngine = args["engine"]

        painter = Painter(engine)
        painter.draw(*Object(20 * math.cos(t), 20 * math.sin(t), sprite_1))

    game = Game(200, 100, setup, loop)
