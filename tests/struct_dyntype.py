import foreign_library_finder
foreign_library_finder.search_paths.append("libs/")
import inheritance as m
import math

b = m.create_object(0)
print(b)

d = m.create_object(1)
d.data = 0
print(d)

l = m.create_object(2)
l.data = math.pi
l.character = 'l'
print(l)
