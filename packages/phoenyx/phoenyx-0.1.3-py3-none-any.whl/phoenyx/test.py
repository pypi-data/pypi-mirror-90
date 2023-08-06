import phoenyx
from renderer import Renderer  # type: ignore

renderer: phoenyx.Renderer = Renderer(600, 600)


def setup() -> None:
    renderer.create_slider(100, 100, "slider", 0, 10, 1, 0, length=300, shape="SQUARE")

    slider = renderer.get_slider("slider")
    renderer.create_button(
        100,
        300,
        "hide slider",
        action=slider.hide,
        height=50,
        width=100,
        color=70,
        stroke="red",
        shape="ELLIPSE",
    )
    renderer.create_button(
        100,
        400,
        "reveal slider",
        action=slider.reveal,
        height=50,
        width=100,
        color=70,
        stroke="green",
        shape="ELLIPSE",
    )

    renderer.new_keypress(renderer.keys.K_SPACE, lambda: print("space"), behaviour="HOLD")
    renderer.new_keypress(renderer.keys.K_a, lambda: print("a"), behaviour="PRESSED")
    renderer.update_keypress(renderer.keys.K_SPACE, lambda: print("space but updated"))

    renderer.text_size = 15


def draw() -> None:
    renderer.background(51)

    renderer.text(10, 10, f"fps : {round(renderer.fps)}")
    renderer.text(10, 30, f"value of slider : {renderer.get_slider_value('slider')}")


if __name__ == "__main__":
    renderer.run(draw, setup=setup)
