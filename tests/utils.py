from datetime import datetime
import unittest
from bson import ObjectId

from mongomonkey import utils

class UtilsTest(unittest.TestCase):

    def test_check_mongo_type(self):
        stdTypes = (ObjectId, int, float, basestring, list, dict, datetime)
        for tp in stdTypes:
            self.assertTrue(utils.check_mongo_type(tp))

    def test_type_name(self):
        self.assertEqual("unicode", utils.type_name(u"some_str"))
        self.assertEqual("unicode", utils.type_name(unicode))
        self.assertEqual("object", utils.type_name(object()))
        self.assertEqual("object", utils.type_name(object))

    def test_cast_to_class(self):
        class SomeCastingClass(object):

            def __init__(self, value):
                self.value = value

            @classmethod
            def cast_to_class(cls, value):
                return cls(value)

        int_val = 8
        str_val = "some_str"
        unicode_val = u"some_unicode"

        self.assertIs(8, utils.cast_to_class(int_val, int))
        self.assertIsInstance(utils.cast_to_class(int_val, float), float)
        self.assertIsInstance(utils.cast_to_class(str_val, unicode), unicode)
        self.assertIsInstance(utils.cast_to_class(unicode_val, str), str)
        self.assertIsInstance(utils.cast_to_class(unicode_val, SomeCastingClass), SomeCastingClass)

    def test_get_path(self):
        self.assertEqual("__builtin__.unicode", utils.get_path(unicode))
        self.assertEqual("tests.utils.UtilsTest", utils.get_path(UtilsTest))

    def test_ClassProperty(self):
        class SomeClassWithClassProperty(object):

            @utils.ClassProperty
            def test(cls):
                return "Yep, this is it! You are calling the class property!"

        self.assertEqual("Yep, this is it! You are calling the class property!", SomeClassWithClassProperty.test)
        self.assertEqual("Yep, this is it! You are calling the class property!", SomeClassWithClassProperty().test)
