def CheckIfValidTour(tour):
    n = len(tour)
    print("n =", n)
    checklist = [False for x in range(n)]
    for i in range(n):
        vertex = tour[i]
        if (not isinstance(vertex, int)) or vertex < 0 or vertex >= n:
            return False
        if checklist[vertex]:
            # FOUND DUPLICATE
            return False
        checklist[vertex] = True
    return True

def TourDistance(matrix, tour):
    V = len(tour)
    fromVertex = tour[0]
    toVertex = tour[1]
    sum = matrix[fromVertex][toVertex]
    for i in range(1, V - 1):
        fromVertex = tour[i]
        toVertex = tour[i + 1]
        sum += matrix[fromVertex][toVertex]
    # DISTANCE OF TOUR + RETURN TO STARTING VERTEX
    return sum + matrix[toVertex][tour[0]]


tour = [3, 2, 1, 0]
print("IS VALID TOUR?", ("YES" if CheckIfValidTour(tour) else "NO"))
matrix = [
    [0, 1, 4, 6],
    [1, 0, 2, 5],
    [4, 2, 0, 3],
    [6, 5, 3, 0]
]
print("DWAVE TOUR DISTANCE:")
print(TourDistance(matrix, tour))
