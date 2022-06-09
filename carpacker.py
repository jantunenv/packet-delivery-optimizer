import numpy as np
import sys
import binpacking

class Car:
	addresses = []

	def __init__(self, sizex=10, sizey=10, sizez=10):
		self.sizex = sizex
		self.sizey = sizey
		self.sizez = sizez

	def get_size(self):
		return(self.sizex, self.sizey, self.sizez)

	def set_size(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def get_volume(self):
		return(self.sizex*self.sizey*self.sizez)

	def attempt_to_fit(items):
		print("attemp to fit not implemented")



class Garage:
	def __init__(self):
		self.cars = []
		self.items = []
		self.bins = {}

	def add_car(self, sizex=10, sizey=10, sizez=10):
		self.cars.append(Car(sizex, sizey, sizez))
		self.cars = sorted(self.cars, key=lambda x: x.get_volume(), reverse=True)

	def set_items(self, items):
		self.items = items

	def distribute_items_to_bins(self, beta=0.75):
		#Three dimensional bin packing problem
		#Using Lodi et al. 2002 Heuristic algorithms for the three-dimensional bin packing problem
		#Start by sorting the items into clusters with similar heights
		self.bins.clear()
		self.items = sorted(self.items, key=lambda x: x[2], reverse=True)
		current_z = self.items[0][2]
		self.bins[current_z] = []

		for item in self.items:
			#If item close to Z value of current bin, add to bin
			#Else: create new bin with current size
			if(item[2]>=beta*current_z):
				self.bins[current_z].append(item)
			else:
				current_z = item[2]
				self.bins[current_z] = []
				self.bins[current_z].append(item)

		#Sort into non-increasing areae
		self.items.clear()
		for key in self.bins.keys():
			self.bins[key] = sorted(self.bins[key], key=lambda x: x[0]*x[1], reverse=True)
			for item in self.bins[key]:
				self.items.append(item)

	def add_to_fill_map(self, p, item, fill_map, marker = 1):
		for x in range(p[0], p[0] + item[0]):
			for y in range(p[1], p[1] + item[1]):
				fill_map[x,y] = marker

	def perimeter_touching_items_or_walls(self, p, item, fill_map):
		score = 0
		x_wall = len(fill_map[0,:])
		y_wall = len(fill_map[:,0])
		for x in range(p[0] , p[0] + item[0] ):
			for y in range(p[1] , p[1] + item[1] ):
				if(y == 0 or y == y_wall - 1): # next to wall
					score += 1
				if(x == 0 or x == x_wall - 1): #next to wall
					score += 1
				if(x - 1 >= 0 and fill_map[x - 1, y]):
					score += 1
				if(x + 1 < x_wall and fill_map[x + 1, y]):
					score += 1
				if(y - 1 >= 0 and fill_map[x, y - 1]):
					score += 1
				if(y + 1  < y_wall and fill_map[x, y + 1]):
					score += 1

		return(score)

	def compute_S(self, S, item, layer, rho=0.3, mu=0.7):
			W = len(S[:,0])
			D = len(S[0,:])
			w = item[0]
			d = item[1]
			h = item[2]
			layer_h = layer[0]
			fill_map = layer[1]			
			
			for x in range(W):
				for y in range(D):
					#Check out of bounds and overlapping other items
					if(x + w - 1 >= W or y + d - 1 >= D or fill_map[x:x + w, y:y + d].any()):
						S[x,y] = 0.0
					else:
						S[x,y] = rho * self.perimeter_touching_items_or_walls([x, y], item, fill_map) * 2 * w
						+ 2 * d + mu*sum(fill_map>0) * W * D
						- (1 - rho - mu) * abs(h - layer_h)*layer_h

	def generate_packing_layers(self, rho=0.3, mu=0.7, input_layers=[]):
		#Lodi et al. 2002
		#Can use pre-determined layers (Phase 2 in Lodi et al. 2002)
		current_car = list(self.cars[0].get_size())

		S = np.zeros((current_car[0], current_car[1]), dtype=np.float64)

		#first item to left back corner of first layer
		
		layers = []
		
		if(not input_layers):
			fill_map = np.zeros((current_car[0], current_car[1]), dtype=np.int32)
			layer_h = self.items[0][2]
			layers.append([layer_h, fill_map])
			self.add_to_fill_map([0,0], self.items[0], fill_map, 1)
			start_index = 1
		else:
			start_index = 0
			for layer in input_layers:
				layers.append( [layer[0], layer[1]*0] )
				

		S_best = 0.0
		S_temp = 0.0	
		for j in range(start_index, len(self.items)):
			item = self.items[j]
			S_best = 0.0
			S_temp = 0.0
			best_layer = -1
			best_pos = [-1, -1]
			
			for l in range(len(layers)):
				layer = layers[l]
				if(item[2] <= layer[0]):
					self.compute_S(S, item, layer, rho, mu)
					S_temp = np.max(S)
					if(S_temp > S_best):
						best_layer = l
						S_best = S_temp
						best_pos = np.asarray(np.where(S == S_best))[:,0]
			if(S_best > 0.0):
				self.add_to_fill_map(best_pos, item, layers[best_layer][1], j+1)
			else:
				for l in range(len(layers)):
					layer = layers[l]
					if(item[2] > layer[0]):
						self.compute_S(S, item, layer, rho, mu)
						S_temp = np.max(S)
						if(S_temp > S_best):
							best_layer = l
							S_best = S_temp
							best_pos = np.asarray(np.where(S == S_best))[:,0]
				if(S_best > 0.0):
					self.add_to_fill_map(best_pos, item, layers[best_layer][1], j+1)
					layers[best_layer][0] = item[2]
				else:
					layers.append([item[2], np.zeros((current_car[0], current_car[1]), dtype=np.int32)])
					self.add_to_fill_map([0,0], item, layers[-1][1], j+1)
 
		#for layer in layers:
		#	print(layer[1])
		#	print("")
		
		#print("--------")	
		return(layers)

	def swap_coordinates(self, c1=0, c2=1):
		#Swap two coordinates, used to generate more packing attempts
		temp = [0,0,0]
		temp_scalar = 0
		for item in self.items:
			temp[c2] = item[c1]
			temp[c1] = item[c2]
			item[c1] = temp[c1]
			item[c2] = temp[c2]
		
		for car in self.cars:
			temp = list(car.get_size())
			temp_scalar = temp[c1]
			temp[c1] = temp[c2]
			temp[c2] = temp_scalar
			car.set_size(temp[0], temp[1], temp[2])

	def print_cars(self):
		for car in self.cars:
			print(car.get_size())
			
	def pack_items(self):
		#Lodi et al. 2002
		#phase 1:
		
		bins = []
		bins_1d = []
		#Run the algorithm in three different rotations
		for ct in [[0,0], [0,2], [1,2]]:
			self.swap_coordinates(ct[0], ct[1])
			self.distribute_items_to_bins(0.75)
			p1 = self.generate_packing_layers(0.3, 0.7)
			bins.append(p1)
			self.distribute_items_to_bins(0.0)
			p2 = self.generate_packing_layers(0.2, 0.3, p1)
			bins.append(p2)
			bins_1d.append(binpacking.to_constant_volume([a[0] for a in p1 if np.sum(a[1]) > 0], self.cars[0].get_size()[2])) 
			bins_1d.append(binpacking.to_constant_volume([a[0] for a in p2 if np.sum(a[1]) > 0], self.cars[0].get_size()[2])) 

		
		bestbin = -1
		min_cars_needed = 9999999
		for i in range(len(bins_1d)):
			cars_needed = len(bins_1d[i])
			if(cars_needed < min_cars_needed):
				best_bin = i
				min_cars_needed = cars_needed

		print("Cars needed:", min_cars_needed)		
		print("Best packing:", bins_1d[best_bin])

def main():
	
	#Main mainly for testing
	garage = Garage()

	garage.add_car(8,8,8)
	garage.add_car(8,8,8)
	garage.add_car(8,8,8)
	garage.add_car(8,8,8)
	garage.add_car(8,8,8)
	#garage.print_cars()

	np.random.seed(13516166)

	if(len(sys.argv) == 2):
		n_items = int(sys.argv[1])
	else:
		n_items = 5

	itemlist = []
	for i in range(n_items):
		r = np.random.randint(1,6,size=3)
		itemlist.append([r[0],r[1],r[2]])

	garage.set_items(itemlist)
	#garage.distribute_items_to_bins()
	garage.pack_items()
		
if __name__ == "__main__":
	main()
