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


# Способность исправлять ошибки
def correction_ability(code_signal, check_matrix):
    result = dict()
    vector_syndrome = transposition(check_matrix[:])
    test_vector_syndrome = []
    result['vector_syndrome'] = vector_syndrome[:]
    combs_vector = list(combinations(range(len(code_signal)), 1))
    result['combs_vector'] = combs_vector[:]
    for i in range(1, len(code_signal)):
        combs = list(combinations(list(range(len(code_signal))), i+1))
        for j in combs:
            test = code_signal[:]
            for k in j:
                test[k] = (test[k]+1) % 2
            test_syndrome = multiplication_vector_on_matrix(test[:], transposition(check_matrix[:]))
            if (test_syndrome in vector_syndrome) or (test_syndrome in test_vector_syndrome):
                result['i'] = i
                return result
            test_vector_syndrome.append(test_syndrome)
        vector_syndrome += test_vector_syndrome
        test_vector_syndrome = []
        result['vector_syndrome'] = vector_syndrome[:]
        combs_vector += combs
        result['combs_vector'] = combs_vector[:]


# Добавление и исправление ошибок, построение графиков
def add_and_correct_errors(code_signal, vectors, check_matrix, title):
    probability_of_error = 50
    number_of_repetitions = 1000
    errors = []
    vector_syndrome = vectors['vector_syndrome']
    combs_vector = vectors['combs_vector']
    for i in range(probability_of_error):
        counter_error = 0

        for j in range(number_of_repetitions):
            copy_code = code_signal[:]
            # Добавление ошибки
            for bit in range(len(copy_code)):
                prob = randint(1, 101)
                if prob < i:
                    copy_code[bit] = (copy_code[bit] + 1) % 2
            # Исправление ошибки
            syndrome = multiplication_vector_on_matrix(copy_code[:], transposition(check_matrix[:]))
            if sum(syndrome) != 0:
                if syndrome in vector_syndrome:
                    index_error = vector_syndrome.index(syndrome)
                    comb = combs_vector[index_error]
                    for k in comb:
                        copy_code[k] = (copy_code[k] + 1) % 2

                    if sum(multiplication_vector_on_matrix(copy_code[:], transposition(check_matrix[:]))) != 0:
                        counter_error += 1
                else:
                    counter_error += 1
        errors.append(counter_error*100/number_of_repetitions)

    fig, ax = plt.subplots()
    ax.set_title('Зависимость вероятности ошибки на бит от вероятности потери пакета для LDPC кода' + title)
    ax.plot(list(range(probability_of_error)), errors)
    ax.grid()
    ax.set_xlabel('Вероятность ошибки на бит,%')
    ax.set_ylabel('Вероятность потери пакета,%')
    plt.show()


'''
Cделать вектор комбинаций, где индекс порядка ошибок равен индексу синдрома синдрому (чтобы добавлялось ровно то что исправляет)
Потом добавлять ошибки с шансами, смотреть какой синдром получается и в соотношении с нашими векторами смотреть
Cпросить нужно ли учитывать синдромы которые не повторяются например как в консоли
Оптимизировать метод декадирования (умножение на 0 нелогично)
Сравнить  с какой вероятностью исправдяет определенное кол-во ошибок и высчитать
'''
