def mst_without_removed_vertex(n, matrix, removed):
    # PRIM-JARNIK ALGORITHM
    in_mst = [False] * n
    key_values = [float('inf')] * n
    sources = [-1] * n

    # STARTING VERTEX
    start = 0
    if removed == 0:
        start = 1
    key_values[start] = 0

    mst_weight = 0
    for i in range(n - 1):
        u = min((v for v in range(n) if not in_mst[v] and v != removed), key=lambda v: key_values[v])
        in_mst[u] = True
        if sources[u] != -1:
            mst_weight += matrix[u][sources[u]]
        for v in range(n):
            if u != v and matrix[u][v] < key_values[v] and not in_mst[v] and v != removed:
                key_values[v] = matrix[u][v]
                sources[v] = u
    return mst_weight


def sum_of_two_smallest_edges(n, matrix, removed):
    first_min = second_min = float('inf')
    for v in range(n):
        if v != removed:
            edge = matrix[removed][v]
            if edge <= first_min:
                second_min = first_min
                first_min = edge
            elif edge < second_min and edge != first_min:
                second_min = edge
    return first_min + second_min


def best_1_tree_lower_bound(n, matrix):
    max_weight = -1
    for i in range(n):
        current_weight = (mst_without_removed_vertex(n, matrix, i) +
                          sum_of_two_smallest_edges(n, matrix, i))
        if current_weight > max_weight:
            max_weight = current_weight
    print("1-TREE LOWER BOUND:", max_weight)
    return max_weight
