def shift(lst, steps):
    for i in range(steps):
        lst.insert(0, lst.pop())


edict = [
    [2, 0, 1],
    [1, 2, 0],
    [0, 1, 2]
]

a = [2, 0, 1]
b = []

for num in range(1, 4):
    print(num)
    shift(a, num)
    b.append(num)

print(b)
print(edict)
