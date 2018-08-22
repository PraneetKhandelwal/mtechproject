import tinyurl as t
f = open('bangalore_newspaper.csv','r')
g = open('new_bangalore_newspaper.csv','w')
c = 0
for line in f:
	line = line.split(',')
	print line
	if(line[1] == '-'):
		g.write(','.join(line)+"\n")
	else:
		final = t.shorten(line[1],"bangalore"+str(c))
		line[1] = final
		g.write(','.join(line)+"\n")
	c+=1