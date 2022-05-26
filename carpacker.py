import numpy as np

class Car:
	addresses = []

	def __init__(self, sizex=10, sizey=10, sizez=10):
		self.sizex = sizex
		self.sizey = sizey
		self.sizez = sizez

	def get_size(self):
		return(self.sizex, self.sizey, self.sizez)

	def get_volume(self):
		return(self.sizex*self.sizey*self.sizez)

	def attempt_to_fit(items):
		print("attemp to fit not implemented")




class Garage:
	def __init__(self):
		self.cars = []
		self.items = []

	def add_car(self, sizex=10, sizey=10, sizez=10):
		self.cars.append(Car(sizex, sizey, sizez))
		self.cars = sorted(self.cars, key=lambda x: x.get_volume(), reverse=True)

	def set_items(self, items):
		self.items = items

	def distribute_items(self):
		#Three dimensional bin packing problem

		#Total amount of cars needed
		#for-loop is slow but should be good enough here
		enough_cars = True
		total_volume = 0
		for item in self.items:
			total_volume += item[0]*item[1]*item[2]

		n_cars = 0
		while(True):
			if(total_volume <= 0):
				break
			elif(n_cars > len(self.cars) - 1):
				enough_cars = False
				break

			total_volume -= self.cars[n_cars].get_volume()
			n_cars += 1

		print(n_cars)
		return(enough_cars)

	def print_cars(self):
		for car in self.cars:
			print(car.get_size())

def main():
	garage = Garage()

	garage.add_car(4,2,2)
	garage.add_car(4,2,2)
	garage.add_car(4,2,2)
	garage.add_car(8,3,3)
	garage.add_car(8,3,3)
	garage.print_cars()

	itemlist = []
	itemlist.append([1,1,1])
	itemlist.append([1,1,1])
	itemlist.append([1,1,1])
	itemlist.append([1,1,1])

	garage.set_items(itemlist)
	print(garage.distribute_items())

if __name__ == "__main__":
	main()
