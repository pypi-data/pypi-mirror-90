# -*- encoding: utf-8 -*-

import unittest


class TestUM(unittest.TestCase):
    def setUp(self):
        self.numbers = [0, 1, 2, 3, 4, 5, 6]
        self.numbers2 = [0, 1, 2, 3, 4, 5, 6]

    def test(self):
        for number in self.numbers:
            index = self.numbers.index(number)
            try:
                sum_ = self.numbers[index] + self.numbers[index + 1]
                self.numbers2.insert(index * 2 + 1, sum_ / 2)
            except:
                pass

    def test2(self):
        for index, number in enumerate(self.numbers):
            try:
                sum_ = self.numbers[index] + self.numbers[index + 1]
                self.numbers2.insert(index * 2 + 1, sum_ / 2)
            except:
                pass


if __name__ == '__main__':
    unittest.main()
