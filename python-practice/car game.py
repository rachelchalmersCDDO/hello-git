
command = ""
while True:
	command = input ("> ").lower()
	if command == "start":
		status = "moving"
		print ("car started...")
	elif command == "stop":
		status = "stopped"
		print ("car stopped.")
	elif command == "help":
		print(''' 
start - to start the car
stop - to stop the car
quit - to exit''')
	elif command == 'quit':
		break
else:
	print ("sorry I don't understand that")

