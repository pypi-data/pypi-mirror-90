from colorama import init
init()

for number in range(0, 8):
    text = " SCAM "
    print(f"{number} - \033[3{number}m{text}\033[0m ", end="")

print()

for number in range(0, 8):
    text = " SCAM "
    print(f"{number} - \033[4{number}m{text}\033[0m ", end="")
