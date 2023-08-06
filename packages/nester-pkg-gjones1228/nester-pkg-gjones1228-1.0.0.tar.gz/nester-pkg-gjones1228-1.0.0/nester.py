##create a function using the def statement. Take a list and process each item in the list. If it finds a list within the first list,
##the function needs to repeat. It can do this by invoking itself (recur) on the nested list. Example of a recursive function

movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, 
                ["Graham Chapman", ["Michael Palin", "John Cleese",
                        "Terry Gilliam", "Eric Idle", "Terry Jones"]]]
##define the function
def print_lol(the_list):
	for l in the_list:
		if isinstance(l, list): ##if the item is itself a list, invoke the function and print list item
			print_lol(l)
		else:
			print(l) ###--not a function, display item

### invoke the function
print_lol(movies)