import math

class First():
	x = int(input("Enter 1 num: "))
	z = int(input("Enter 2 num: "))
	s = input("Enter + or × or / or - : ")
	
	if s == "+":
		print(z + x)
	
	if s == "-":
		print(x - z)
	
	if s == "/":
		print(x / z)
	
	if s == "×":
		print(x * z)
