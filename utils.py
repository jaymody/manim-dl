import random

import numpy as np


def softmax(x, axis=-1):
    x_max = x - np.max(x, axis=axis, keepdims=True)
    return np.exp(x_max) / np.sum(np.exp(x_max), axis=axis, keepdims=True)


def matrix_to_tex(mat, scale=1):
    rows = []
    for row in mat:
        rows.append(" & ".join(row))
    rows = r" \\ ".join(rows)

    return r"\begin{bmatrix} " + rows + r" \end{bmatrix}"
