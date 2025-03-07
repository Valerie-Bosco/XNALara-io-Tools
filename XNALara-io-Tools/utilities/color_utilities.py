import random


def random_color_rgb() -> tuple[float, float, float]:
    return (1 / random.randint(1, 255), 1 / random.randint(1, 255), 1 / random.randint(1, 255))
