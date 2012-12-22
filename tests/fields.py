import unittest
from mongomonkey import Model, Field

class SomeEmbeddedModel(Model):
    pass

class SomeModel(Model):
    simple_untyped_field = Field()
    simple_int_field = Field(int)
    bind_to_another_field = Field(str, "some_other_field")
    simple_embedded_field = Field(SomeEmbeddedModel)
    simple_another_embedded_field = Field(SomeEmbeddedModel)


class FieldTest(unittest.TestCase):

    def test_valid_set_field(self):
        embedded_model = SomeEmbeddedModel()
        expected = {'simple_untyped_field': "Some value",
                    'simple_int_field': 42,
                    'some_other_field': None,
                    'simple_embedded_field': embedded_model,
                    'simple_another_embedded_field': {}}

        some_model = SomeModel()
        some_model.simple_untyped_field = "Some value"
        some_model.simple_int_field = 42
        some_model.bind_to_another_field = None
        some_model.simple_embedded_field = embedded_model
        some_model.simple_another_embedded_field = {}
        self.assertDictEqual(expected, some_model)

    def test_invalid_set_field(self):
        expected = {}
        some_model = SomeModel()
        with self.assertRaises(ValueError):
            some_model.simple_int_field = "I'm not int! I'm a string!!!"
        with self.assertRaises(ValueError):
            some_model.bind_to_another_field = 42
        self.assertDictEqual(expected, some_model)

    def test_del_field(self):
        embedded_model = SomeEmbeddedModel()
        expected = {'simple_untyped_field': "Some value",
                    'simple_int_field': 42,
                    'simple_embedded_field': embedded_model}

        some_model = SomeModel()
        some_model.simple_untyped_field = "Some value"
        some_model.simple_int_field = 42
        some_model.bind_to_another_field = None
        some_model.simple_embedded_field = embedded_model
        some_model.simple_another_embedded_field = {}

        del some_model.bind_to_another_field
        del some_model.simple_another_embedded_field

        with self.assertRaises(AttributeError):
            del some_model.simple_another_embedded_field

        self.assertDictEqual(expected, some_model)

    def test_get_field(self):
        embedded_model = SomeEmbeddedModel()
        expected = {'simple_untyped_field': "Some value",
                    'simple_int_field': 42,
                    'simple_embedded_field': embedded_model,
                    'simple_another_embedded_field': {}}
        some_model = SomeModel()
        some_model.simple_untyped_field = "Some value"
        some_model.simple_int_field = 42
        some_model.bind_to_another_field = None
        some_model.simple_embedded_field = embedded_model
        some_model.simple_another_embedded_field = {}

        self.assertEqual("Some value", some_model.simple_untyped_field)
        self.assertEqual(42, some_model.simple_int_field)
        self.assertEqual(None, some_model.bind_to_another_field)
        self.assertEqual(embedded_model, some_model.simple_embedded_field)
        self.assertEqual({}, some_model.simple_another_embedded_field)
        with self.assertRaises(AttributeError):
            some_model.unexisting_field
        del some_model.bind_to_another_field
        with self.assertRaises(AttributeError):
            some_model.bind_to_another_field
        self.assertEqual(expected, some_model)



