from prettytable import PrettyTable  # Импортируем установленный модуль.
import yaml
from kanobu.core import Kanobu

Kanobu().logo()

lang = "uk_UA"
with open(f"locale/{lang}.yaml", encoding="utf-8") as L:
    locale = yaml.safe_load(L.read())

th = ['#', 'Result', 'Player1', 'Player2']
td = ['1', f'\033[32m{locale["results"][0]}\033[0m', 'Bot #4323224', 'Bot jDan735',
      '2', f'\033[31m{locale["results"][1]}\033[0m', 'Bot #4323224', 'Bot Obama',
      '3', f'\033[33m{locale["results"][2]}\033[0m', 'Bot Obama', 'Bot Kanobu',
      '4', f'\033[32m{locale["results"][0]}\033[0m', 'Bot Kanobu', 'Bot jDan735',
      '5', f'\033[32m{locale["results"][0]}\033[0m', '???', '???']

columns = len(th)  # Подсчитаем кол-во столбцов на будущее.

table = PrettyTable(th)  # Определяем таблицу.

table.align["Result"] = "l"

# Cкопируем список td, на случай если он будет использоваться в коде дальше.
td_data = td[:]
# Входим в цикл который заполняет нашу таблицу.
# Цикл будет выполняться до тех пор пока у нас не кончатся данные
# для заполнения строк таблицы (список td_data).
while td_data:
    # Используя срез добавляем первые пять элементов в строку.
    # (columns = 5).
    table.add_row(td_data[:columns])
    # Используя срез переопределяем td_data так, чтобы он
    # больше не содержал первых 5 элементов.
    td_data = td_data[columns:]

print(table)  # Печатаем таблицу
