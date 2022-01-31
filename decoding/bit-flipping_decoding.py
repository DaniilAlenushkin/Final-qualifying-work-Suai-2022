"""
Алгоритм переключения битов - это алгоритм передачи сообщений с жестким решением для LDPC. Двоичное (жесткое) решение о
каждом принятом бите принимается детектором и передается в декодер. Для алгоритма переключения битов сообщения,
передаваемые по ребрам графа Таннера, также являются двоичными: битовый узел отправляет сообщение, объявляющее,
является ли оно единицей или нулем, и каждый контрольный узел отправляет сообщение каждому подключенному битовому узлу,
объявляя, какое значение бит на основе информации, доступной контрольному узлу. Узел проверки определяет, что
его уравнение проверки четности выполняется, если сумма входящих битовых значений по модулю 2 равна нулю.
Если большинство сообщений, полученных битовым узлом, отличаются от его принятого значения, битовый узел изменяет
(переворачивает) свое текущее значение. Этот процесс повторяется до тех пор, пока не будут выполнены все уравнения
проверки четности или пока не пройдет некоторое максимальное количество итераций декодера и декодер не откажется.
Декодер с переключением битов может быть немедленно отключен всякий раз, когда найдено допустимое кодовое слово,
путем проверки того, все ли уравнения проверки четности удовлетворенный. Это относится ко всему декодированию LDPC-кодов
с передачей сообщений и имеет два важных преимущества; во-первых, после нахождения решения можно избежать
дополнительных итераций, а во-вторых, всегда обнаруживается неспособность сходиться к кодовому слову.
Алгоритм переключения битов основан на принципе, согласно которому бит кодового слова, участвующий в большом количестве
неверных контрольных уравнений, скорее всего, сам по себе будет неверным. Разреженность H помогает распределять биты по
проверкам, так что уравнения проверки четности вряд ли будут содержать один и тот же набор битов кодового слова. В
"""

from LDPC import generator_matrix, check_matrix
from function_for_LDPC import *
"""
check_matrix = [[1, 1, 0, 1, 0, 0],
                [0, 1, 1, 0, 1, 0],
                [1, 0, 0, 0, 1, 1],
                [0, 0, 1, 1, 0, 1]]
"""
signal = [randint(0, 1) for i in range(len(generator_matrix))]
code_signal = multiplication_vector_on_matrix(signal[:], generator_matrix[:])

# code_signal = [0, 0, 1, 0, 1, 1]

print(code_signal)
check_matrix_one_position = []
for i in check_matrix:
    check_matrix_one_position_line = []
    for j in range(len(i)):
        if i[j] == 1:
            check_matrix_one_position_line.append(j)
        if j + 1 == len(i):
            check_matrix_one_position.append(check_matrix_one_position_line)
print(check_matrix_one_position)
errors = []
probability_of_error = 100
number_of_repetitions = 1000
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
        list_of_option = []
        while True:
            if copy_code in list_of_option:
                counter_error += 1
                break
            list_of_option.append(copy_code)
            line_values = []
            for line in check_matrix_one_position:
                line_value = 0
                for value in line:
                    line_value = (line_value + copy_code[value]) % 2
                line_values.append(line_value)
            counter_value = 0
            for value in line_values:
                counter_value = counter_value + value
            # !!!!!!!!!!!!!
            if counter_value == 0:
                """
                if code_signal != copy_code:
                    print(code_signal)
                    print(copy_code)
                    print(line_values)
                    print(reverse_dict)
                    print('-------------------')
                break
                """
                if code_signal == copy_code:
                    break
                else:
                    counter_error += 1
                    break

            # !!!!!!!!!!!!!

            reverse_dict = dict()
            for bit in range(len(copy_code)):
                reverse_dict[bit] = []
                for value in range(len(line_values)):
                    if bit in check_matrix_one_position[value] and line_values[value] == 1:
                        reverse_dict[bit].append(True)
                    elif bit in check_matrix_one_position[value] and line_values[value] == 0:
                        reverse_dict[bit].append(False)
            """            
            print(line_values)
            print(reverse_dict)
            print(copy_code)
            """
            for z in reverse_dict.keys():
                if False not in reverse_dict[z] and reverse_dict[z] != []:
                    copy_code[z] = (copy_code[z] + 1) % 2
            """
            print(copy_code)
            print('--------------')
            """

    errors.append(counter_error * 100 / number_of_repetitions)
plotting(probability_of_error, errors, 'bit-flipping decoding')

# TODO Продумать условие определения, когда проверки на четность выполняется, а исходный и исправленный код отличаются
#  Места, которые продумать в коде отмечены # !!!!
