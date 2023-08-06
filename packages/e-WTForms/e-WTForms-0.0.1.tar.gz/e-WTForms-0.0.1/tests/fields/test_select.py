import pytest
from tests.common import DummyPostData

from wtforms import widgets
from wtforms.fields import SelectField
from wtforms.form import Form


def make_form(name="F", **fields):
    return type(str(name), (Form,), fields)


def test_select_field_copies_choices():
    class F(Form):
        items = SelectField(choices=[])

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def add_choice(self, choice):
            self.items.choices.append((choice, choice))

    f1 = F()
    f2 = F()

    f1.add_choice("a")
    f2.add_choice("b")

    assert f1.items.choices == [("a", "a")]
    assert f2.items.choices == [("b", "b")]
    assert f1.items.choices is not f2.items.choices


class F(Form):
    a = SelectField(choices=[("a", "hello"), ("btest", "bye")], default="a")
    b = SelectField(
        choices=[(1, "Item 1"), (2, "Item 2")],
        coerce=int,
        option_widget=widgets.TextInput(),
    )


def test_defaults():
    form = F()
    assert form.a.data == "a"
    assert form.b.data is None
    assert form.validate() is False
    assert form.a() == (
        '<select id="a" name="a"><option selected value="a">hello</option>'
        '<option value="btest">bye</option></select>'
    )
    assert form.b() == (
        '<select id="b" name="b"><option value="1">Item 1</option>'
        '<option value="2">Item 2</option></select>'
    )


def test_with_data():
    form = F(DummyPostData(a=["btest"]))
    assert form.a.data == "btest"
    assert form.a() == (
        '<select id="a" name="a"><option value="a">hello</option>'
        '<option selected value="btest">bye</option></select>'
    )


def test_value_coercion():
    form = F(DummyPostData(b=["2"]))
    assert form.b.data == 2
    assert form.b.validate(form)
    form = F(DummyPostData(b=["b"]))
    assert form.b.data is None
    assert not form.b.validate(form)


def test_iterable_options():
    form = F()
    first_option = list(form.a)[0]
    assert isinstance(first_option, form.a._Option)
    assert list(str(x) for x in form.a) == [
        '<option selected value="a">hello</option>',
        '<option value="btest">bye</option>',
    ]
    assert isinstance(first_option.widget, widgets.Option)
    assert isinstance(list(form.b)[0].widget, widgets.TextInput)
    assert (
        first_option(disabled=True)
        == '<option disabled selected value="a">hello</option>'
    )


def test_default_coerce():
    F = make_form(a=SelectField(choices=[("a", "Foo")]))
    form = F(DummyPostData(a=[]))
    assert not form.validate()
    assert form.a.data is None
    assert len(form.a.errors) == 1
    assert form.a.errors[0] == "Not a valid choice."


def test_validate_choices():
    F = make_form(a=SelectField(choices=[("a", "Foo")]))
    form = F(DummyPostData(a=["b"]))
    assert not form.validate()
    assert form.a.data == "b"
    assert len(form.a.errors) == 1
    assert form.a.errors[0] == "Not a valid choice."


def test_validate_choices_when_empty():
    F = make_form(a=SelectField(choices=[]))
    form = F(DummyPostData(a=["b"]))
    assert not form.validate()
    assert form.a.data == "b"
    assert len(form.a.errors) == 1
    assert form.a.errors[0] == "Not a valid choice."


def test_validate_choices_when_none():
    F = make_form(a=SelectField())
    form = F(DummyPostData(a="b"))
    with pytest.raises(TypeError, match="Choices cannot be None"):
        form.validate()


def test_dont_validate_choices():
    F = make_form(a=SelectField(choices=[("a", "Foo")], validate_choice=False))
    form = F(DummyPostData(a=["b"]))
    assert form.validate()
    assert form.a.data == "b"
    assert len(form.a.errors) == 0


def test_choice_shortcut():
    F = make_form(a=SelectField(choices=["foo", "bar"], validate_choice=False))
    form = F(a="bar")
    assert '<option value="foo">foo</option>' in form.a()


def test_choice_shortcut_post():
    F = make_form(a=SelectField(choices=["foo", "bar"]))
    form = F(DummyPostData(a=["foo"]))
    assert form.validate()
    assert form.a.data == "foo"
    assert len(form.a.errors) == 0


@pytest.mark.parametrize("choices", [[], None])
def test_empty_choice(choices):
    F = make_form(a=SelectField(choices=choices, validate_choice=False))
    form = F(a="bar")
    assert form.a() == '<select id="a" name="a"></select>'


def test_callable_choices():
    def choices():
        return ["foo", "bar"]

    F = make_form(a=SelectField(choices=choices))
    form = F(a="bar")

    assert list(str(x) for x in form.a) == [
        '<option value="foo">foo</option>',
        '<option selected value="bar">bar</option>',
    ]
