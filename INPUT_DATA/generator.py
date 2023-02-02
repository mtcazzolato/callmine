# generate a csv file (source, destination, measure)
# ready for processing

import random

N = 10_000 # number of subscribers
M = 20_000 # number of phonecalls
D = 3_600 # maximum duration of a phonecall

SOURCE="source"
DESTINATION="destination"
MEASURE="measure"
print("{},{},{}".format(SOURCE, DESTINATION, MEASURE))

for ph in range(M):
	source = 'S'+str( random.randint(1,N))
	destination = 'S'+str( random.randint(1,N))
	duration = random.randint(1,D)
	print("{},{},{}".format(source, destination, duration))



