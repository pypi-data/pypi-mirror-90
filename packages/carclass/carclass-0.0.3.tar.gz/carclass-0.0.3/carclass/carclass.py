class Car:
  def __init__(_self,name,color,price):
    _self.name = name
    _self.color = color
    _self.price = price
    
  def get_name(_self):
     return _self.name
  def get_color(_self):
    return _self.color
  def get_price(_self):
    return _self.price
  def __repr__(_self):
	  return f"{_self.name}:{_self.color}:{_self.price}"

class CarList:
  def __init__(_self,cars):
    _self.cars = cars

  def total_price(_self):
    total = 0
    print(_self.cars)
    for i in _self.cars:
      total += i.get_price()
    return total

  def __add__(_self,other):
    _self.cars += other.cars
    return "Total Price: " + str(_self.total_price())
  
  def __repr__(_self):
	  return str(_self.cars)