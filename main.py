import sys
import numpy as np
import carpacker
import routeplanner
import citygenerator

def main():
	nx = 20
	ny = 20
	steps = 200
	london = citygenerator.City(steps, nx, ny)

	n_packages = 50
	addresses = routeplanner.generate_targets(london, n_packages)

	packages = []

	for i in range(n_packages):
		r = np.random.randint(1,6,size=3)
		packages.append(carpacker.Packet(r[0], r[1], r[2], i, addresses[i]))

	garage = carpacker.Garage()
	garage.add_car(8,8,8)
	garage.set_packets(packages)
	garage.pack_items()

	packing = garage.get_final_packing()

	car_destinations = []
	for car in packing:
		car_destinations.append([])
		for layer in car:
			for item in layer[2]:
				car_destinations[-1].append(item.address)

	for i in range(len(car_destinations)):
		car_destinations[i] = list(set(car_destinations[i]))

	shortest_paths = []
	for dests in car_destinations:
		shortest_paths.append(routeplanner.best_routes(london, dests))

	routes = []

	if(len(sys.argv)>2):
		steps = int(sys.argv[1])
		betamax = float(sys.argv[2])
	else:
		steps = 10000
		betamax = 0.001

	for i in range(len(shortest_paths)):
		solver = routeplanner.Salesman_solver(shortest_paths[i])
		routes.append(solver.solve("naive")) 

	frate = 5
	for i in range(len(routes)):
		#citygenerator.draw_city(london, nx, ny, car_destinations[i], routes[i])
		citygenerator.animate_route(london, nx, ny, car_destinations[i], routes[i], name = "test"+str(i)+".mp4", resolution=100, frate=frate)

if __name__ == "__main__":
	main()
