numbers = [0, 1, 2, 3, 4, 5, 6]
numbers2 = [0, 1, 2, 3, 4, 5, 6]

for number in numbers:
    index = numbers.index(number)
    try:
        sum_ = numbers[index] + numbers[index + 1]
        numbers2.insert(index * 2 + 1, sum_ / 2)
    except:
        pass

print(f"{numbers = }")
print(f"{numbers2 = }")
