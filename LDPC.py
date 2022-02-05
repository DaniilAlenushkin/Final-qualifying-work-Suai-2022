from function_for_LDPC import *

generator_matrix = [[1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
                    [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1]]

check_matrix = [[0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1],
                [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1]]

if __name__ == '__main__':
    while True:
        signal = [randint(0, 1) for i in range(len(generator_matrix))]
        if max(signal) != 0:
            break
    code_signal = multiplication_vector_on_matrix(signal[:], generator_matrix[:])
    print(code_signal)
    syndrome = multiplication_vector_on_matrix(code_signal[:],
                                               transposition(check_matrix))
    print(syndrome)
