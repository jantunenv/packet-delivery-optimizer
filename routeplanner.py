import citygenerator
import carpacker
import networkx
import numpy as np

class Salesman_solver:
	paths = None
	visit_list = None

	def __init__(self, paths):
		#Paths: dictionary with keys: nodes and values: [path_length, [path]]
		self.paths = paths
		self.visit_list = np.zeros(len(paths.keys()),dtype=np.int8)

	def solve(self, method="naive", steps = 1000, beta=0.5, initmode="random"):
		if(method=="naive"):
			return(self.solve_naive())
		elif(method=="metropolis"):
			return(self.solve_metropolis(steps, beta, initmode))

	def solve_metropolis(self, steps=1000, beta=0.5, initmode="random"):
		#metropolis monte carlo solution
		route = []
		n = len(self.paths.keys())

		#start from zero
		route.append(0)

		#Fill all but first and last index
		if(initmode == "random"):
			for node in np.arange(1, n):
				route.append(node)
		else:
			print("not implemented")
			exit()

		#connect loop back to zero
		route.append(0)

		e_old = 0.0
		e_new = 0.0
		ind1 = 0
		ind2 = 0
		for step in range(steps):
			#random index not including the first and last index
			while(True):
				ind1 = np.random.randint(1,n)
				ind2 = np.random.randint(1,n)
				if(ind1 != ind2):
					break

			x1 = route[ind1 - 1]
			x2 = route[ind1 + 1]
			x3 = route[ind2 - 1]
			x4 = route[ind2 + 1]

			e_old =   self.paths[x1][ind1 - 1][1] + \
				  self.paths[ind1][x2 - 1][1] + \
				  self.paths[x3][ind2 - 1][1] + \
				  self.paths[ind2][x4 - 1][1]

			e_new =   self.paths[x1][ind2 - 1][1] + \
				  self.paths[ind2][x2 - 1][1] + \
				  self.paths[x3][ind1 - 1][1] + \
				  self.paths[ind1][x4 - 1][1]

			if(e_new <= e_old):
				route[ind1], route[ind2] = route[ind2], route[ind1]
			else:

				rn = np.random.rand()
				p = np.exp(-beta*(e_new - e_old))
				if(rn<p):
					route[ind1], route[ind2] = route[ind2], route[ind1]

		finalroute = []
		#add all but the last one because 0 causes problems

		for i in range(len(route) - 2):

			if(route[i]<route[i+1]):
				for node in self.paths[route[i]][route[i+1] - 1][2]:
					finalroute.append(node)
			else:
				for node in self.paths[route[i]][route[i+1]][2]:
					finalroute.append(node)

		#add final path
		for node in self.paths[route[-2]][0][2]:
			finalroute.append(node)

		return(finalroute)

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
	#Generating the city
	nx = 20
	ny = 20
	steps = 200
	helsinki = citygenerator.City(steps, nx, ny)

	#Generating targets
	targets = generate_targets(helsinki, 10)

	#Solve shortest paths between points and then shortest route
	shortest_paths = best_routes(helsinki, targets)

	solver = Salesman_solver(shortest_paths)
	solution = solver.solve("metropolis")

	citygenerator.draw_city(helsinki, nx, ny, targets, solution)


if (__name__ == "__main__"):
	main()
