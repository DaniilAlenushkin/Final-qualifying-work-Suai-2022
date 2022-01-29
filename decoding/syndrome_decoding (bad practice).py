from function_for_LDPC import *
from LDPC import generator_matrix, check_matrix


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
def add_and_correct_errors(generator_matrix, check_matrix):
    signal = [randint(0, 1) for i in range(len(generator_matrix))]
    code_signal = multiplication_vector_on_matrix(signal[:], generator_matrix[:])
    vectors = correction_ability(code_signal, check_matrix)
    probability_of_error = 50
    number_of_repetitions = 10
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
    title = 'c использованием синдромов'
    plotting(probability_of_error, errors, title)

if __name__ == '__main__':
    add_and_correct_errors(generator_matrix, check_matrix)