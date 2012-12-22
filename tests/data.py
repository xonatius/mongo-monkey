import unittest
from mongomonkey import list_of

IntList = list_of(int)

class TypedListTest(unittest.TestCase):

    def test_changing_with_valid_type(self):
        expected = [i for i in range(10)]
        actual = IntList([0, 1, 2])
        actual.append(4)
        actual.extend([5, 96, 97, 98, 99])
        actual.insert(3, 3)
        actual[6] = 6
        actual[7:9] = (7, 8)
        actual[7:10:2] = (7, 9)

        self.assertListEqual(expected, actual)

    def test_changing_with_invalid_type(self):
        expected = [i for i in range(10)]
        with (self.assertRaises(ValueError)):
            IntList(['a', 'b', 'c'])
        actual = IntList([i for i in range(10)])
        with (self.assertRaises(ValueError)):
            actual.append('e')
        with (self.assertRaises(ValueError)):
            actual.extend(['if', 'ig', 'ih', 'ii'])
        with (self.assertRaises(ValueError)):
            actual.insert(3, 'd')
        with (self.assertRaises(ValueError)):
            actual[5] = 'f'
        with (self.assertRaises(ValueError)):
            actual[7:9] = ('g', 'h')
        with (self.assertRaises(ValueError)):
            actual[7:10:2] = ('g', 'i')
        self.assertListEqual(expected, actual)

    def test_cast_to_class(self):
        valid_list = [1, 2, 3, 4, 5]
        invalid_list = [1, 'a', 3, 4, 5]
        not_a_list = object()

        self.assertIsInstance(IntList.cast_to_class(valid_list), IntList)
        with (self.assertRaises(ValueError)):
            IntList.cast_to_class(invalid_list)
        with (self.assertRaises(TypeError)):
            IntList.cast_to_class(not_a_list)


