#!/usr/bin/env python

# This programme picks a name at random 

import random

insert = True

people = []

print("\n")
print("Welcome to Rachel's name picker ")
print("\n")
print("Please insert all names, then type done")
print("\n")

while insert is True:
	name = input()
	if name.upper() == "DONE":
		insert = False
	else:
		people.append(name)

print("\n")
print("There are " + str(len(people)) + " people in the office today.")
print("\n")

index = 1
while len(people) > 0:
	number = random.randint(0,len(people)-1)
	numberwang = random.randint(0,800)
	if number == numberwang:
		print("That's Numberwang")
	print(str(index) + ". " + (people[number].capitalize()))
	people.pop(number)
	index += 1
else: 
	exit()



