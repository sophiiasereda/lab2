import copy
import numpy as np
SIMPLE, STARRED, PRIMED = 0, 1, 2


def minimize(matrix, deepcopy=True):
    if deepcopy:
        matrix = copy.deepcopy(matrix)
    n = len(matrix)
    
    for row in matrix:
        #m = min(row)
        m = min([i for i in row if i != 0])
        max_value = max(row)
        if m != 0:
            row[:] = map(lambda x: x - m if x != 0 else max_value + 1, row)

    mask_matrix = [[SIMPLE] * n for _ in matrix]
    row_cover = [False] * n
    col_cover = [False] * n

    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0 and not row_cover[r] and not col_cover[c]:
                mask_matrix[r][c] = STARRED
                row_cover[r] = True
                col_cover[c] = True

    row_cover = [False] * n
    col_cover = [False] * n

    match_found = False

    while not match_found:
        for i in range(n):
            col_cover[i] = any(mrow[i] == STARRED for mrow in mask_matrix)

        if all(col_cover):
            match_found = True
            continue
        else:
            zero = _cover_zeroes(matrix, mask_matrix, row_cover, col_cover)

            primes = [zero]
            stars = []
            while zero:
                zero = _find_star_in_col(mask_matrix, zero[1])
                if zero:
                    stars.append(zero)
                    zero = _find_prime_in_row(mask_matrix, zero[0])
                    stars.append(zero)

            for star in stars:
                mask_matrix[star[0]][star[1]] = SIMPLE

            for prime in primes:
                mask_matrix[prime[0]][prime[1]] = STARRED

            for r, row in enumerate(mask_matrix):
                for c, val in enumerate(row):
                    if val == PRIMED:
                        mask_matrix[r][c] = SIMPLE

            row_cover = [False] * n
            col_cover = [False] * n
    
    solution = []
    for r, row in enumerate(mask_matrix):
        for c, val in enumerate(row):
            if val == STARRED:
                solution.append((r, c))
    return solution


def _cover_zeroes(matrix, mask_matrix, row_cover, col_cover):

    while True:
        zero = True

        while zero:
            zero = _find_noncovered_zero(matrix, row_cover, col_cover)
            if not zero:
                break
            else:
                row = mask_matrix[zero[0]]
                row[zero[1]] = PRIMED

                try:
                    index = row.index(STARRED)
                except ValueError:
                    return zero

                row_cover[zero[0]] = True
                col_cover[index] = False

        m = min(_uncovered_values(matrix, row_cover, col_cover))
        for r, row in enumerate(matrix):
            for c, __ in enumerate(row):
                if row_cover[r]:
                    matrix[r][c] += m
                if not col_cover[c]:
                    matrix[r][c] -= m


def _find_noncovered_zero(matrix, row_cover, col_cover):
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0 and not row_cover[r] and not col_cover[c]:
                return (r, c)
    else:
        return None


def _uncovered_values(matrix, row_cover, col_cover):
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if not row_cover[r] and not col_cover[c]:
                yield value


def _find_star_in_col(mask_matrix, c):
    for r, row in enumerate(mask_matrix):
        if row[c] == STARRED:
            return (r, c)
    else:
        return None


def _find_prime_in_row(mask_matrix, r):
    for c, val in enumerate(mask_matrix[r]):
        if val == PRIMED:
            return (r, c)
    else:
        return None
