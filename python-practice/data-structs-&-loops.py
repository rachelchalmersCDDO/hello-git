# Data Structures

# 1. Array - an array is like an ice cube tray and all your ice cubes are variables (called Lists in Python)

emptyArray = []

singleArray = [5]

stringArray = ["dog", "cat", "fish"]

numArray = [1, 6, 8, 9]

mixedArray = [1, "two"]

# to access elements of an array do the following:
# (note: indexed from zero not one)

print(stringArray[0])

print("The " + stringArray[2] + " is aged " + str(numArray[1]) + ".")

# str is a string function to convert any variable into a string. Here we need to convert the number into a string to pass it through the print function 

print(mixedArray[1])

# 2. Dictionary - links simple and complex values eg table - a piece of furniture 

emptyDict = {}

numberDict = {1: "one", 200: "two hundred", 3: "three"}

boolDict = {"true": True, "false": False}

print(numberDict[200])

print(str(boolDict["true"]) + " is the opposite of " + str(boolDict["false"]) + ".")

# Quick Maths  

num = 0 

print(num)

# num + 1 = num - shorthand below 
num += 1

print(num)

# num + 80 = num - shorthand below 
num += 80

print(num)

# can also subtract, multiply and divide:

num -= 700

print(num)

num *= -6

print(num)

num /= 2

print(num)

num = 0

# Loops

# 1. For loop

for i in range(0, 5): 
	num += 12
	print(str(i) + ": " + str(num))


