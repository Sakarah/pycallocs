import elflib
elflib.__path__.append("libs/")
from elflib import nested_struct as m

o = m.outstruct()
a = o.a
a.data1 = 1
o.a.data2 = 2

b = m.instruct()
b.data1 = 3
b.data2 = 6
o.b.__init__(b) # <- TODO: Maybe add an alias method name for this
o.b.data2 = 4

b.data1 = 5

print(o)
print(a)
print(b)

m.print_outstruct(o)
