from mongomonkey import Model, Field, list_of

class SomeEmbeddedModel(Model):
    pass


class SomeModel(Model):
    simple_untyped_field = Field()
    simple_int_field = Field(int)
    bind_to_another_field = Field(str, "some_other_field")
    simple_embedded_field = Field(SomeEmbeddedModel)
    simple_another_embedded_field = Field(SomeEmbeddedModel)


class Node(Model):
    child1 = Field('self')
    child2 = Field('Node')
    some_node_double_list = list_of(list_of("Node"))