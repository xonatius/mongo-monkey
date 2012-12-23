import unittest
from mongomonkey import Model, Field
from tests.examle_models import SomeEmbeddedModel, SomeModel, Node


class TestModel(unittest.TestCase):

    def test_valid_setitem(self):
        embedded_model = SomeEmbeddedModel()
        expected = {'simple_untyped_field': "Some value",
                    'simple_int_field': 42,
                    'some_other_field': None,
                    'simple_embedded_field': embedded_model,
                    'simple_another_embedded_field': {},
                    'not_a_field': "Any value"}

        some_model = SomeModel()
        some_model["simple_untyped_field"] = "Some value"
        some_model["simple_int_field"] = 42
        some_model["some_other_field"] = None
        some_model["simple_embedded_field"] = embedded_model
        some_model["simple_another_embedded_field"] = {}
        some_model["not_a_field"] = "Any value"
        self.assertDictEqual(expected, some_model)
        self.assertIsInstance(some_model['simple_another_embedded_field'], SomeEmbeddedModel)

    def test_invalid_setitem(self):
        expected = {}
        some_model = SomeModel()
        with self.assertRaises(ValueError):
            some_model.simple_int_field = "I'm not int! I'm a string!!!"
        with self.assertRaises(ValueError):
            some_model.bind_to_another_field = 42
        self.assertDictEqual(expected, some_model)

    def test_valid_update(self):
        embedded_model = SomeEmbeddedModel()
        expected = {'simple_untyped_field': "Some value",
                    'simple_int_field': 42,
                    'some_other_field': None,
                    'simple_embedded_field': embedded_model,
                    'simple_another_embedded_field': {},
                    'not_a_field': "Any value"}

        some_model = SomeModel()
        some_model.update(expected)
        self.assertDictEqual(expected, some_model)
        self.assertIsInstance(some_model['simple_another_embedded_field'], SomeEmbeddedModel)

    def test_invalid_update(self):
        expected = {}
        some_model = SomeModel()
        with self.assertRaises(ValueError):
            some_model.update({'simple_int_field': "I'm not int! I'm a string!!!",
                               'some_other_field': 42})
        self.assertDictEqual(expected, some_model)

    def test_valid_init(self):
        embedded_model = SomeEmbeddedModel()
        expected = {'simple_untyped_field': "Some value",
                    'simple_int_field': 42,
                    'some_other_field': None,
                    'simple_embedded_field': embedded_model,
                    'simple_another_embedded_field': {},
                    'not_a_field': "Any value"}

        some_model = SomeModel(expected)
        self.assertDictEqual(expected, some_model)
        self.assertIsInstance(some_model['simple_another_embedded_field'], SomeEmbeddedModel)
        some_model = SomeModel(**expected)
        self.assertDictEqual(expected, some_model)
        self.assertIsInstance(some_model['simple_another_embedded_field'], SomeEmbeddedModel)

    def test_invalid_update(self):
        with self.assertRaises(ValueError):
            SomeModel({'simple_int_field': "I'm not int! I'm a string!!!",
                       'some_other_field': 42})

    def test_recursive_model(self):
        expected = {'child1':
                        {
                            'child2':
                                {
                                    'child1': {},
                                    'child2': {}
                                }
                        },
                    'child2':
                        {
                            'some_node_double_list': [[{}, {}], [], [{}]],
                            'child1': {}
                        },
                    'some_node_double_list': []
        }
        node = Node(child1=Node(child2=Node(child1=Node(), child2=Node())))
        node.child2 = Node(some_node_double_list=[[Node(), Node()], [], [Node()]])
        node["child2"]["child1"] = {}
        node["some_node_double_list"] = []
        self.assertDictEqual(expected, node)

    def test_binding_on_same_field(self):
        with self.assertRaises(ValueError):
            class InvalidModel(Model):
                a = Field(field_name="a")
                b = Field(field_name="a")
