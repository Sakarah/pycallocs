import elflib
elflib.__path__.append("libs/")
from elflib import alphanum

print(alphanum.NB_LETTERS)
alph1 = alphanum.get_alphabet()
alph1[0] = '@'
print(alph1[0])
alph2 = alphanum.get_alphabet()
print(alph2[0])
print(alph2[8])

