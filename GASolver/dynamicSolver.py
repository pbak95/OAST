def dynamic_alg(capacity, weight_arr, values_arr):
    A = init_array(capacity, len(values_arr))
    for i in range(1, len(values_arr)):
        for j in range(1, capacity):
            old = A[i - 1][j]
            if weight_arr[i] > j:
                A[i][j] = old
            else:
                new = A[i - 1][j - weight_arr[i]] + values_arr[i]
                if new > old:
                    A[i][j] = new
                else:
                    A[i][j] = old
    return A[len(values_arr) - 1][capacity - 1]


def init_array(n, m):
    """
	create n x m array filled with 0
	:param n:
	:param m:
	:return:
	"""
    return [[0 for x in range(n)] for y in range(m)]
