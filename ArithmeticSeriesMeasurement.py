import math


def vectorize(n, edge_count, matrix):
    edges = [0] * edge_count

    # READ MATRIX WITH LEFT-TO-RIGHT VECTORIZATION
    edge = 0
    for i in range(n):
        for j in range(i + 1, n):
            # COLLECT EDGE
            edges[edge] = matrix[i][j]
            edge += 1

    return edges


def measure_arithmetic_series(n, matrix):
    # NUMBER OF EDGES
    edge_count = (n * (n - 1)) >> 1

    # COLLECT EDGES
    edges = vectorize(n, edge_count, matrix)
    # SORT EDGES
    edges.sort()

    difference_count = edge_count - 1
    differences = [0] * difference_count

    is_arithmetic_series = "YES"
    previous_difference = edges[1] - edges[0]
    differences[0] = previous_difference
    # LIST DIFFERENCES
    for i in range(1, difference_count):
        differences[i] = edges[i + 1] - edges[i]
        if differences[i] != previous_difference:
            is_arithmetic_series = "NO"
        previous_difference = differences[i]

    print("SORTED EDGES ARE AN ARITHMETIC SERIES?", is_arithmetic_series)

    # AVERAGE DIFFERENCE
    average_difference = 0
    for i in range(difference_count):
        average_difference += differences[i]
    average_difference /= difference_count

    print("AVERAGE DIFFERENCE BETWEEN SORTED EDGES:", average_difference)

    # EACH DIFFERENCE MINUS AVERAGE SQUARED
    squared_margins = [0] * difference_count
    for i in range(difference_count):
        squared_margins[i] = (differences[i] - average_difference) ** 2

    # VARIANCE OF DIFFERENCES
    variance = 0
    for i in range(difference_count):
        variance += squared_margins[i]
    variance /= difference_count

    print("VARIANCE OF DIFFERENCES BETWEEN SORTED EDGES:", variance)
    print("STANDARD DEVIATION OF DIFFERENCES BETWEEN SORTED EDGES:", math.sqrt(variance))
    return
