from function_for_LDPC import *


if __name__ == '__main__':
    generator_matrix, check_matrix = definition_matrix_from_txt('Matrix.txt')
    print(f'Строк в матрице {len(generator_matrix)}')
    print(f'Столбцов в матрице {len(generator_matrix[0])}')
    print(f'Кодовая скорость {len(generator_matrix)/len(generator_matrix[0])}')
    for j in range(10):
        while True:
            signal = [randint(0, 1) for i in range(len(generator_matrix))]
            if max(signal) != 0:
                break
        code_signal = multiplication_vector_on_matrix(signal[:], generator_matrix[:])
        syndrome = multiplication_vector_on_matrix(code_signal[:],
                                                   transposition(check_matrix))
        counter_syndrome = 0
        for k in syndrome:
            counter_syndrome += k
        if counter_syndrome != 0:
            print(syndrome)
        print(f'Вычислил {j+1} синдром')
    print('Прошел стадию выявления ненулевых синдромов')
    check_matrix_one_position = []
    for i in check_matrix:
        check_matrix_one_position_line = []
        for j in range(len(i)):
            if i[j] == 1:
                check_matrix_one_position_line.append(j)
            if j + 1 == len(i):
                check_matrix_one_position.append(check_matrix_one_position_line)
    for i in check_matrix_one_position:
        print(i)
    for i in check_matrix:
        for j in check_matrix:
            if i == j:
                continue
            counter = 0
            for z in range(len(i)):
                if i[z] == j[z] and i[z] == 1:
                    counter += 1
            if counter > 1:
                print(
                    f'{check_matrix.index(i) + 1} строка похожа на '
                    f'{check_matrix.index(j) + 1} {counter} символами')

    number_of_bit_checks = dict()
    for i in range(len(code_signal)):
        number_of_bit_checks[i] = 0

    for i in check_matrix_one_position:
        for j in i:
            number_of_bit_checks[j] += 1
    print(number_of_bit_checks)
