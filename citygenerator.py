import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import networkx

class City:
	streets = None

	def __init__(self, n_steps=100, nx=10, ny=10):
		self.create_streets(n_steps, nx, ny)

	def create_streets(self, n_steps, nx, ny):

		nodes_and_edges = networkx.Graph()

		previous_step = np.random.randint(3)
		step_options = np.array([[1,0],[0,1],[-1,0],[0,-1]])
		#Starting position
		x = [np.random.randint(nx), np.random.randint(ny)]
		current_node = x[0] + x[1]*nx
		previous_step = np.random.randint(4)

		for i in range(n_steps):
			while(True):
				current_step = np.random.randint(4)
				x += step_options[current_step]
				if(x[0] != nx and x[0] != -1 and x[1] != ny and x[1] !=-1):
					nodes_and_edges.add_nodes_from([current_node, x[0]+x[1]*nx])
					nodes_and_edges.add_edge(current_node, x[0]+x[1]*nx)
					current_node = x[0] + x[1]*nx
					break
				else:
					x -= step_options[current_step]

		self.streets = nodes_and_edges

def animate_route(city, nx, ny, targets, route, name = "test.mp4", resolution = 100, frate = 10):
	ffmpeg_writer = matplotlib.animation.writers['ffmpeg']
	anim_writer = ffmpeg_writer(fps=frate)
	fig = plt.figure()
	positions = {}
	car_marker, = plt.plot([],[], 'ro', markersize = 10)
	for node in list(city.streets.nodes):
		positions[node] = [node%nx, int(node/ny)]

	networkx.drawing.nx_pylab.draw_networkx_edges(city.streets, pos=positions)
	plt.plot([positions[node][0] for node in targets], [positions[node][1] for node in targets],"*")
	plt.plot([positions[node][0] for node in route], [positions[node][1] for node in route],'r')

	with anim_writer.saving(fig, name, resolution):
		for node in route:
			car_marker.set_data(positions[node][0], positions[node][1])
			anim_writer.grab_frame()

def draw_city(city, nx=10, ny=10, targets=[], route=[]):
	positions = {}
	for node in list(city.streets.nodes):
		positions[node] = [node%nx, int(node/ny)]

	networkx.drawing.nx_pylab.draw_networkx_edges(city.streets, pos=positions)
	if(targets):
		plt.plot([positions[node][0] for node in targets], [positions[node][1] for node in targets],"*")

	if(route):
		plt.plot([positions[node][0] for node in route], [positions[node][1] for node in route],'r')
	plt.show()

def main():
	if(len(sys.argv)==4):
		NewYork = City(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
		draw_city(NewYork, int(sys.argv[2]), int(sys.argv[3]))
	else:
		NewYork = City()
		draw_city(NewYork)

if __name__ == "__main__":
	main()
