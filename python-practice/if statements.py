# IF STATEMENTS 

is_hot = True 
is_cold = False

if is_hot:
	print("It's a hot day")
	print("Drink plenty of water")

elif is_cold:
	print("It's a cold day")
	print("Wear warm clothes")

else:
	print("It's a lovely day")

# House exercise

price = 1000000
is_credit_good = True

if is_credit_good:
	down_payment = 0.1 * int(price)

else:
	down_payment = 0.2 * int(price)

print(f'Down payment: ${down_payment}')

# LOGICAL OPERATORS 
# AND: both should be true
# OR: at least one should be tru e
# NOT

has_high_income = True
has_good_credit = False

if has_high_income and has_good_credit:
	print('Eligible for a loan')

if has_high_income or has_good_credit:
	print('Eligible for a loan')

has_good_credit = True 
has_criminal_record = True

if has_good_credit and not has_criminal_record:
	print('Eligible for a loan')


# COMPARISON OPERATORS
	# < > <= >= == !=

temperature = 34

if (temperature) > 30:
	print("It's a hot day") 

else:
	print("It's not a hot day")

# NAME PROGRAMME 

name = input('Please enter your name here: ')

if len(name) < 3:
	print('Name must be at least 3 characters long')

elif len(name) > 50:
	print('Name cannot exceed 50 characters')

else:
	print('Name looks good!')

# WEIGHT CONVERTER 

weight = int(input('Weight: '))
unit = input('(L)bs or (K)g: ')

if unit.upper() == 'L':
	converted = weight * 0.45
	print(f'You are {converted} kilos')

else:
	converted = weight / 0.45
	print(f'You are {converted} pounds')














