import citygenerator
import numpy as np

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
	citygenerator.draw_city(helsinki, nx, ny, targets)

if (__name__ == "__main__"):
	main()
