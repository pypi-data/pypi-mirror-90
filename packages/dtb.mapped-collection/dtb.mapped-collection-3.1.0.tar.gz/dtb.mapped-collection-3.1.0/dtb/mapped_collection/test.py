from dataclasses import dataclass

import pytest

from .mapped_collection import MappedCollection


class Item(str):
    def key(self) -> str:
        return self


class C(MappedCollection[Item]):
    pass


@pytest.mark.parametrize("initial", [[], [Item("a")], [Item("b"), Item("c")]])
def test_mapped_collection_init(initial):
    assert C(initial)


@pytest.mark.parametrize(
    ["initial", "expected"],
    [([], []), ([Item("a")], ["a"]), ([Item("b"), Item("c")], ["b", "c"])],
)
def test_mapped_collection_list(initial, expected):
    assert list(C(initial)) == expected


@pytest.mark.parametrize(
    ["initial", "value", "expected"],
    [
        (C([]), Item("a"), C([Item("a")])),
        (C([Item("a")]), Item("a"), C([Item("a")])),
        (C([Item("a")]), Item("b"), C([Item("a"), Item("b")])),
    ],
)
def test_mapped_collection_add(initial, value, expected):
    initial.add(value)

    assert initial == expected


@pytest.mark.parametrize(
    ["collection", "value", "expected"],
    [
        (C([]), Item("a"), False),
        (C([Item("a")]), Item("a"), True),
        (C([Item("b")]), Item("a"), False),
    ],
)
def test_mapped_collection_contains(collection, value, expected):
    assert (value in collection) is expected


def test_mapped_collection_getitem():
    collection = C([Item("a")])

    assert collection["a"] == Item("a")


def test_mapped_collection_getitem_error():
    collection = C([Item("a")])

    with pytest.raises(KeyError):
        collection["b"]


@pytest.mark.parametrize(
    ["c1", "c2", "equal"],
    [
        (C([Item("a"), Item("b")]), C([Item("a"), Item("b")]), True),
        (C([Item("a"), Item("b")]), C([Item("b"), Item("a")]), True),
        (C([Item("a"), Item("b")]), C([Item("b")]), False),
    ],
)
def test_mapped_collection_eq(c1, c2, equal):
    assert (c1 == c2) is equal


def test_mapped_collection_eq_error():
    with pytest.raises(NotImplementedError):
        assert C([]) == 0


@dataclass
class Item2:
    id: str
    name: str

    def key(self) -> str:
        return self.id


class C2(MappedCollection[Item2]):
    pass


def test_mapped_collection_filter_by():
    c = C2([Item2(id="a", name="foo"), Item2(id="b", name="bar")])

    filtered = c.filter_by("name", "bar")

    assert filtered == C2([Item2(id="b", name="bar")])


def test_mapped_collection_first():
    c = C2([Item2(id="a", name="foo"), Item2(id="b", name="bar")])

    assert c.first() == Item2(id="a", name="foo")
