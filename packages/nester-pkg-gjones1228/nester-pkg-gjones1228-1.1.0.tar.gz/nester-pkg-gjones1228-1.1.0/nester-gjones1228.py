##create a function using the def statement. Take a list and process each item in the list. If it finds a list within the first list,
##the function needs to repeat. It can do this by invoking itself (recur) on the nested list. Example of a recursive function

movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, 
                ["Graham Chapman", ["Michael Palin", "John Cleese",
                        "Terry Gilliam", "Eric Idle", "Terry Jones"]]]
##define the function print_lol. Takes any list (the_list) which can have nested lists. Each item is recursively printed to the screen on its own line.
##Part 2 - added nested_level arg to insert tab-stops when a nested list is encountered
def print_lol(the_list, level ):
	for each_item in the_list:
		if isinstance(each_item, list): ##if the item is itself a list, invoke the function and print list item
			print_lol(each_item, level+1)
		else:
			## the BIF range() returns an iterator that generates numbers in a specified range
			for tab_stop in range(level):
				print("\t",end='')
			print(each_item) ###--not a function, display item

### invoke the function
print_lol(movies, level=1)
