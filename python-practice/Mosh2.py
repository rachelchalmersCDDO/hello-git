# This programme will ask the year you're born in then calculate your age
# int() converts string to integer 
# float() converts string into number with decimal point
# bool() converts string into boolian variable 

birth_year = input('Birth year: ')
print(type(birth_year))
age = 2021 - int(birth_year)
print (type(age))
print(age)

# converting weight exercise

weight_lb = input('What is your weight in pounds? ')
weight_kg = float(weight_lb) * 0.45
print('You weigh ' + str(weight_kg) + ' in kilos!')



