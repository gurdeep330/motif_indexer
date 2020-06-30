import itertools

its = [range(3)] * 2
print (its)
for x, y in itertools.product(*its):
    print (x, y)

x = [['ABCD', 'EFG'], ['xy'], ['12', '3']]
print (x)
for case in itertools.product(*x):
    print (case)
