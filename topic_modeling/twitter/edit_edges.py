
print "hello"
target = open("edges","r")
edges = target.read().split("\n")
print edges
target.close()

i = 0
new_edges = []
for line in edges:
	if i==0:
		l = line + ",Type"
		i += 1
		new_edges.append(l)
		print l
	else:
		l = line + ",Undireced"
		new_edges.append(l)
		print l

target = open("edges2","w")
for line in new_edges:
	target.write(line)
	target.write("\n")

target.close()