"""
В двоичном канале стирания (BEC) переданный бит либо принимается корректно, либо полностью
стирается с некоторой вероятностью ε. Поскольку биты, которые полученные всегда полностью
корректны, задача декодера состоит в том, чтобы определить значение неизвестных битов.
Если существует уравнение проверки на четность, которое включает только один стертый бит
правильное значение стертого бита можно определить, выбрав значение,
что удовлетворяет четности.
"""
from LDPC import generator_matrix, check_matrix
from function_for_LDPC import *


def decoding_in_binary_erasure_channel(generator_matrix, check_matrix):
    error_correction_ability_true = dict()
    error_correction_ability_false = dict()
    signal = [randint(0, 1) for i in generator_matrix]
    code_signal = multiplication_vector_on_matrix(signal[:], generator_matrix[:])
    check_matrix_one_position = []
    for i in check_matrix:
        check_matrix_one_position_line = []
        for j in range(len(i)):
            if i[j] == 1:
                check_matrix_one_position_line.append(j)
            if j+1 == len(i):
                check_matrix_one_position.append(check_matrix_one_position_line)
    errors = []
    probability_of_error = 100
    number_of_repetitions = 1000
    for i in range(probability_of_error):
        counter_error = 0
        for j in range(number_of_repetitions):
            copy_code = code_signal[:]
            position_of_x = []
            # Добавление ошибки
            for bit in range(len(copy_code)):
                prob = randint(1, 101)
                if prob < i:
                    copy_code[bit] = "X"
                    position_of_x.append(bit)

            # Исправление ошибки
            while True:
                if 'X' not in copy_code:
                    if copy_code != code_signal:
                        print(0)
                    break
                check_copy_code = copy_code[:]
                for line in check_matrix_one_position:
                    counter_x_in_line = 0
                    for x_pos in position_of_x:
                        if x_pos in line:
                            counter_x_in_line += 1
                            current_x_pos = x_pos

                    parity_check = 0
                    if counter_x_in_line == 1:
                        for pos_one in line:
                            if pos_one == current_x_pos:
                                continue
                            else:
                                parity_check = (parity_check + copy_code[pos_one]) % 2
                        copy_code[current_x_pos] = parity_check
                        if len(position_of_x) not in error_correction_ability_true.keys():
                            error_correction_ability_true[len(position_of_x)] = 0
                        error_correction_ability_true[
                            len(position_of_x)] = \
                            error_correction_ability_true[len(position_of_x)] + 1
                        position_of_x.remove(current_x_pos)
                if check_copy_code == copy_code:
                    counter_error += 1
                    if len(position_of_x) not in error_correction_ability_false.keys():
                        error_correction_ability_false[len(position_of_x)] = 0
                    error_correction_ability_false[len(position_of_x)] = \
                        error_correction_ability_false[len(position_of_x)] + 1
                    break
        errors.append(counter_error * 100 / number_of_repetitions)

    dict_for_correction_ability = dict()
    for z in range(1, len(code_signal)+1):
        try:
            correct = error_correction_ability_true[z]
        except KeyError:
            correct = 0

        try:
            wrong = error_correction_ability_false[z]
        except KeyError:
            wrong = 0

        try:
            dict_for_correction_ability[z] = correct * 100 / (correct + wrong)
        except ZeroDivisionError:
            dict_for_correction_ability[z] = 0

    for z in dict_for_correction_ability.keys():
        print('Код исправляет', z, 'ошибку в',
              dict_for_correction_ability[z], '% случаях')
    title = 'в двоичном канале стирания'
    plotting(probability_of_error, errors, title)


if __name__ == '__main__':
    decoding_in_binary_erasure_channel(generator_matrix, check_matrix)
