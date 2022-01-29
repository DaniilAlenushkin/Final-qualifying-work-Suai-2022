from itertools import combinations
from random import randint
import matplotlib.pyplot as plt


# Умножение матриц
def multiplication_matrix(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    C = [[0 for row in range(cols_B)] for col in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] = C[i][j] % 2
    return C


# Умножение вектора на матрицу
def multiplication_vector_on_matrix(x, y):
    result = []
    value = 0
    for f in range(len(y[0])):
        for i in range(len(x)):
            value += x[i] * y[i][f]
        result.append(value % 2)
        value = 0
    return result


# Транспонирование матрицы
def transposition(x):
    result = []
    length = len(x[0])
    for i in range(length):
        result.append([])
    for i in range(length):
        for k in x:
            result[i].append(k[i])
    return result


# Построение графиков
def plotting(probability_of_error, errors, title):
    fig, ax = plt.subplots()
    ax.set_title('Зависимость вероятности ошибки на бит от вероятности потери пакета для LDPC кода ' + title)
    ax.plot(list(range(probability_of_error)), errors)
    ax.grid()
    ax.set_xlabel('Вероятность ошибки на бит,%')
    ax.set_ylabel('Вероятность потери пакета,%')
    plt.show()
