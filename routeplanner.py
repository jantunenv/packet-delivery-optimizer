import citygenerator
import networkx
import numpy as np

class Salesman_solver:
	paths = None
	visit_list = None

	def __init__(self, paths):
		#Paths: dictionary with keys: nodes and values: [path_length, [path]]
		self.paths = paths
		self.visit_list = np.zeros(len(paths.keys()),dtype=np.int8)

	def solve(self, method="naive"):
		if(method=="naive"):
			return(self.solve_naive())

	def solve_naive(self):
		#always go to the closest unvisited neighbour
		route = []
		current = list(self.paths.keys())[0]
		self.visit_list[current] = 1

		for i in range(len(self.visit_list)-1):
			shortest = [999999,999999,[-1,-1,-1]]
			targets = self.paths[current]
			for target in targets:
				if(self.visit_list[target[0]] == 1):
					continue
				elif(target[1]<shortest[1]):
					shortest = target

			current = shortest[0]
			self.visit_list[current] = 1
			route.append(shortest)



		#remove dublicates from the final route and compress in together

		finalroute = []

		for index, length, path in route:
			for i in range(0,len(path)-1):
				finalroute.append(path[i])


		for node in self.paths[current][0][2]:
			finalroute.append(node)

		#for i in range(len(self.paths[0][current-1][2])):
		#	finalroute.append(self.paths[0][current-1][2][-i-1])

		return(finalroute)


def best_routes(city, targets):
	shortest_paths = {}
	for i in range(len(targets)):
		shortest_paths[i] = []

	for i in range(len(targets)-1):
		for j in range(i+1, len(targets)):
			sp = networkx.shortest_path(city.streets, source=targets[i], target=targets[j])
			sp_reverse = [node for node in sp]
			sp_reverse.reverse()

			shortest_paths[i].append([j, len(sp) - 1, sp])
			shortest_paths[j].append([i, len(sp) - 1, sp_reverse])

	return(shortest_paths)

def generate_targets(city, n):
	targets = []

	prob = n/len(list(city.streets.nodes))
	for node in list(city.streets.nodes):
		rn = np.random.rand()
		if(rn<=prob):
			targets.append(node)
	return(targets)

def main():
	nx = 20
	ny = 20
	steps = 200
	helsinki = citygenerator.City(steps, nx, ny)
	targets = generate_targets(helsinki, 10)
	shortest_paths = best_routes(helsinki, targets)

	solver = Salesman_solver(shortest_paths)
	solution = solver.solve()

	citygenerator.draw_city(helsinki, nx, ny, targets, solution)


if (__name__ == "__main__"):
	main()
