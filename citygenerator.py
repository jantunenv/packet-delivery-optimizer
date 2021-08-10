import sys
import numpy as np
import matplotlib.pyplot as plt


class City:
	streets = None
	houses = None

	def __init__(self, n_steps=100, nx=10, ny=10, p_houses=0.1):
		self.create_streets(n_steps, nx, ny)
		self.create_houses(p_houses)

	def create_streets(self, n_steps, nx, ny):
		nodes_and_edges = np.zeros((nx,ny,4))

		previous_step = np.random.randint(3)
		step_options = np.array([[0,1],[1,0],[0,-1],[-1,0]])
		#Starting position
		x = np.array([np.random.randint(nx), np.random.randint(ny)])
		previous_step = np.random.randint(4)

		for i in range(n_steps):
			current_step = np.random.randint(4)
			#stop instead of going back
			if(current_step != (previous_step + 2)%4):
				nodes_and_edges[x[0], x[1], current_step] = 1

				x += step_options[current_step]
				x[0] = x[0]%nx
				x[1] = x[1]%ny
				nodes_and_edges[x[0], x[1], (current_step + 2)%4] = 1

		self.streets = []
		for i in range(nx):
			for j in range(ny):
				if(np.sum(nodes_and_edges[i,j,:]) != 0):
					self.streets.append([[i, j], nodes_and_edges[i,j,:]])

	def create_houses(self, p_houses):
		house_coordinates = []
		for coordinate, edges in self.streets:
			r = np.random.rand()
			if(r<p_houses):
				house_coordinates.append(coordinate)
		self.houses = np.asarray(house_coordinates)

def draw_city(city):
	half_houses = int(len(city.houses)/2)
	plt.plot(city.houses[half_houses:,0] + 0.2, city.houses[half_houses:,1] + 0.2, "bs")
	plt.plot(city.houses[:half_houses,0] - 0.2, city.houses[:half_houses,1] - 0.2, "bs")

	for i in range(len(city.streets)):
		plt.plot([city.streets[i][0][0], city.streets[i][0][0] 
		+ city.streets[i][1][1]], [city.streets[i][0][1], city.streets[i][0][1]])
		plt.plot([city.streets[i][0][0], city.streets[i][0][0]
		+ city.streets[i][1][3]], [city.streets[i][0][1], city.streets[i][0][1]])
		plt.plot([city.streets[i][0][0], city.streets[i][0][0]]
		, [city.streets[i][0][1], city.streets[i][0][1] + city.streets[i][1][0]])
		plt.plot([city.streets[i][0][0], city.streets[i][0][0]]
		, [city.streets[i][0][1], city.streets[i][0][1] + city.streets[i][1][2]])

	plt.show()

def main():
	if(len(sys.argv)==4):
		NewYork = City(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
	elif(len(sys.argv)==5):
		NewYork = City(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
	else:
		NewYork = City()
	draw_city(NewYork)

if __name__ == "__main__":
	main()
