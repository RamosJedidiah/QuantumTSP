import random


def generate_random_points(n):
    points = [[0, 0] for x in range(n)]
    for i in range(n):
        points[i][0] = random.randint(0, 5000)
        points[i][1] = random.randint(0, 5000)
    print("POINTS:")
    print(points)
    return points


def get_length(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1.0 / 2.0)


def build_adjacency_matrix(points, n):
    adjacency_matrix = [[0.0 for x in range(n)] for y in range(n)]
    for i in range(n):
        # POINT 1
        from_point = points[i]
        from_x = from_point[0]
        from_y = from_point[1]
        for j in range(i, n):
            if i != j:
                # POINT 2
                to_point = points[j]
                to_x = to_point[0]
                to_y = to_point[1]
                # CALCULATE DISTANCE
                distance = get_length(from_x, from_y, to_x, to_y)
                # SET EDGE WEIGHT
                adjacency_matrix[i][j] = distance
                adjacency_matrix[j][i] = distance
    return adjacency_matrix
