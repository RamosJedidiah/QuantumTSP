from EuclideanTSPHeuristics import test_all

# CHOOSE NUMBER OF VERTICES
n = 10
DISTANCE_MATRIX = test_all(n)

from dwave.optimization.generators import traveling_salesperson
model = traveling_salesperson(distance_matrix=DISTANCE_MATRIX)

from dwave.system import LeapHybridNLSampler
sampler = LeapHybridNLSampler()

# THIS ACTUALLY GETS SENT TO D-WAVE IN CANADA
results = sampler.sample(model, label='EuclideanTSP')

route, = model.iter_decisions()
print("DWAVE TOUR:")
print(route.state(0))
