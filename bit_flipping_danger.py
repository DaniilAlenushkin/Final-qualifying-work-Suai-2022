import datetime as dt
from multiprocessing import Pool, cpu_count

from function_for_LDPC import *

generator_matrix, check_matrix = definition_matrix_from_txt('Matrix.txt')
check_matrix_one_position = []
for i in check_matrix:
    check_matrix_one_position_line = []
    for j in range(len(i)):
        if i[j] == 1:
            check_matrix_one_position_line.append(j)
        if j + 1 == len(i):
            check_matrix_one_position.append(check_matrix_one_position_line)


def bit_flipping(copy_code):
    counter_error = 0
    list_of_option = []
    while True:
        if copy_code in list_of_option:
            counter_error += 1
            break
        list_of_option.append(copy_code[:])
        line_values = []
        for line in check_matrix_one_position:
            line_value = 0
            for value in line:
                line_value = (line_value + copy_code[value]) % 2
            line_values.append(line_value)
        counter_value = 0
        for value in line_values:
            counter_value = counter_value + value
        if counter_value == 0:
            break
        reverse_dict = dict()
        for bit in range(len(copy_code)):
            reverse_dict[bit] = []
            for value in range(len(line_values)):
                if bit in check_matrix_one_position[value] and line_values[value] == 1:
                    reverse_dict[bit].append(True)
                elif bit in check_matrix_one_position[value] and line_values[value] == 0:
                    reverse_dict[bit].append(False)

        for z in reverse_dict.keys():
            if False not in reverse_dict[z] and reverse_dict[z] != []:
                copy_code[z] = (copy_code[z] + 1) % 2
    return counter_error


if __name__ == '__main__':
    counter_loops = 0
    print(dt.datetime.now())
    probability_of_error = 13
    number_of_repetitions = 1
    dataset = []
    generator_matrix, check_matrix = definition_matrix_from_txt('Matrix.txt')
    signal = [randint(0, 1) for i in generator_matrix]
    code_signal = multiplication_vector_on_matrix(signal[:], generator_matrix[:])
    print(code_signal)
    for i in range(probability_of_error):
        for j in range(number_of_repetitions):
            copy_code = code_signal[:]
            # Добавление ошибки
            for bit in range(len(copy_code)):
                prob = randint(1, 101)
                if prob < i:
                    copy_code[bit] = (copy_code[bit] + 1) % 2
            dataset.append(copy_code)

    with Pool(processes=cpu_count()) as pool:
        result = pool.map(bit_flipping, dataset, 3)

    list_for_plotting = []
    for i in range(0, probability_of_error*number_of_repetitions, number_of_repetitions):
        list_for_plotting.append(sum(result[i:i+number_of_repetitions])*100/number_of_repetitions)
    image = cascade_code_solomon_and_golay(probability_of_error)
    image.append(list_for_plotting)
    print(dt.datetime.now())
    plotting(probability_of_error, image, ['golay + solomon', 'LDPC'])
