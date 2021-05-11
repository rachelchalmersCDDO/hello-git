# you can use single ' and double '' quotes to define a string but sometimes you have to use a specific form

course = 'Python for Beginners'
print(course)

course = "Python's course for beginners"
print(course)

course = 'Python for "Beginners"'
print(course)

# what about for multiline strings? use triple quotes:

course = '''
Hi John, 

here is our first email to you 

Thank you, 
The support team 

'''
print(course)

# can use square brackets to get a character from its index

course = 'Python for Beginners'
print(course[0])

# in Python you can use a negative index (starting from the end)

print(course[-2])

# to print characters from 0 UP TO (not including) 3:

print(course[0:3])

# to print all characters in string

print(course[0:])

print(course[1:4])

# can use this to copy ie return all characters in a variable 

print(course[:])
another = course[:]
print(another)

name = 'Jennifer'
print(name[1:-1])

# FORMATTED STRINGS

first = 'John'
last = 'Smith'
message = first + ' [' + last + '] ' + 'is a coder'
print(message)

# as the above gets more complex it is difficult to visualise concattenated strings
# so use formatted strings with an f prefix and curly brackets

msg = f'{first} [{last}] is a coder'
print(msg)

# len displays how many characters are in a string 

course = 'Python for Beginners'
print(len(course))

# methods: doesnt change the original string, creates new string and returns it 
print(course.upper())
print(course.lower())

# finds index in string
print(course.find('P'))
print(course.find('for'))

# to replace a character or sequence of characters
print(course.replace('Beginners', 'Absolute Beginners'))

# to check the existance of character or sequence of characters in your string
# this is a boolian expression (returns true or false)
print('Python' in course)
print('python' in course)































