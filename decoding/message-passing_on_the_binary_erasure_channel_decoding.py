"""
В двоичном канале стирания (BEC) переданный бит либо принимается корректно, либо полностью стирается с некоторой
вероятностью ε. Поскольку биты, которые полученные всегда полностью корректны, задача декодера состоит в том, чтобы
определить значение неизвестных битов.Если существует уравнение проверки на четность, которое включает только один
стертый бит правильное значение стертого бита можно определить, выбрав значение что удовлетворяет  четности.
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
# print(signal)
code_signal = multiplication_vector_on_matrix(signal[:], generator_matrix[:])
# print(code_signal)
parity_check_matrix = transposition(check_matrix[:])[:len(generator_matrix)]
# code_signal = [0, 0, 1, 0, 1, 1]
print('---')
check_matrix_one_position = []
for i in check_matrix:
    check_matrix_one_position_line = []
    for j in range(len(i)):
        if i[j] == 1:
            check_matrix_one_position_line.append(j)
        if j+1 == len(i):
            check_matrix_one_position.append(check_matrix_one_position_line)
print('Позиции единиц в матрице проверки на четность')
for i in check_matrix_one_position:
    print(i)
errors = []
probability_of_error = 100
number_of_repetitions = 10000
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
                            parity_check = (parity_check + copy_code[pos_one])%2
                    copy_code[current_x_pos] = parity_check
                    position_of_x.remove(current_x_pos)
            if check_copy_code == copy_code:
                counter_error += 1
                break
    errors.append(counter_error * 100 / number_of_repetitions)




fig, ax = plt.subplots()
ax.set_title('Зависимость вероятности ошибки на бит от вероятности потери пакета для LDPC кода')
ax.plot(list(range(probability_of_error)), errors)
ax.grid()
ax.set_xlabel('Вероятность ошибки на бит,%')
ax.set_ylabel('Вероятность потери пакета,%')
plt.show()

"""
смотрю на места Х и ищу эти места в линиях таблицы проверки на четность
Если линия таблицы проверки на четность содержит 1 Х (а остальные позиции известны), то тогда исправляем,ол 
если нет идем к следующей линии.  
и так далее, если спустя проход по всей таблице ничего не поменялось считаем, что потеря потерь 
"""




# TODO каждая строка матрицы проверки на четность это номера битов кодового слова, которые при сложении
#  дают 0, по этой теме нужно воостанавливать недостающие биты, продумать логику(24 страница книги)

