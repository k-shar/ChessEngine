
from math import e
from random import randint
import matplotlib.pyplot as plt


def normalise_evaluation(eval):
    scale = 0.0001
    return (e**(scale * eval) - 1)/(e**(scale * eval) + 1)


if __name__ == "__main__":
    infinity = 99999

    input_evaluations = []
    for i in range(100):
        input_evaluations.append(randint(-infinity, infinity))

    evaluation_slider_center = []
    for input in input_evaluations:
        evaluation_slider_center.append(normalise_evaluation(input))

    plt.plot(input_evaluations, evaluation_slider_center, "x")
    plt.show()
