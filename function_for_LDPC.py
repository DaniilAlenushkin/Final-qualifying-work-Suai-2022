from math import comb
from itertools import combinations
from random import randint

import matplotlib.pyplot as plt


# Умножение матриц
def multiplication_matrix(a, b):
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])
    c = [[0 for row in range(cols_b)] for col in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                c[i][j] += a[i][k] * b[k][j]
                c[i][j] = c[i][j] % 2
    return c


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
def plotting(probability_of_error: int, errors: list, legend: list):
    fig, ax = plt.subplots()
    ax.set_title('Зависимость вероятности ошибки на бит от вероятности потери пакета')
    for i in range(len(errors)):
        ax.plot(list(range(probability_of_error)), errors[i])
    ax.legend(legend)
    ax.grid()
    ax.set_xlabel('Вероятность ошибки на бит,%')
    ax.set_ylabel('Вероятность потери пакета,%')
    plt.show()


def cascade_code_solomon_and_golay(probability_of_error):
    errors_golay = []
    for p in range(probability_of_error):
        packet_lost_probability = 0
        for k in range(5, 25):
            packet_lost_probability += (comb(24, k) * ((p/100) ** k) *
                                        ((1 - (p/100))**(24-k))) * 100
        errors_golay.append(packet_lost_probability)

    errors_golay_and_solomon = []
    for error in errors_golay:
        packet_lost_probability = 0
        for k in range(12, 171):
            packet_lost_probability += (comb(170, k) * ((error/100) ** k) *
                                        ((1 - (error/100))**(170-k))) * 100
        errors_golay_and_solomon.append(packet_lost_probability)

    errors_solomon = []
    for p in range(probability_of_error):
        packet_lost_probability = 0
        for k in range(12, 171):
            packet_lost_probability += (comb(170, k) * ((p/100) ** k) *
                                        ((1 - (p/100))**(170-k))) * 100
        errors_solomon.append(packet_lost_probability)

    errors_solomon_and_golay = []
    for error in errors_solomon:
        packet_lost_probability = 0
        for k in range(5, 25):
            packet_lost_probability += (comb(24, k) * ((error/100) ** k) *
                                        ((1 - (error/100))**(24-k))) * 100
        errors_solomon_and_golay.append(packet_lost_probability)

    return [errors_golay_and_solomon]


def definition_matrix_from_txt(file_name):
    with open(file_name) as f:
        check = []
        generator = []
        counter_blank_lines = 0
        for line in f:
            list_line = []
            for symbol in line:
                if symbol.isdigit():
                    list_line.append(int(symbol))
            if not list_line:
                counter_blank_lines += 1
            else:
                if counter_blank_lines in [1, 2]:
                    check.append(list_line)
                elif counter_blank_lines in [3, 4]:
                    generator.append(list_line)
    return generator, check


if __name__ == '__main__':
    cascade_code_solomon_and_golay(20)
