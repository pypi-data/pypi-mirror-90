from __future__ import annotations

from typing import Any, Dict, Iterable, Iterator, Optional, Protocol, TypeVar


class WithKey(Protocol):
    def key(self) -> str:  # pragma: no cover
        ...


T = TypeVar("T", bound=WithKey)


class MappedCollection(Iterable[T]):
    def __init__(self, items: Iterable[T]) -> None:
        self._collection: Dict[str, T] = {}
        for item in items:
            self._collection[item.key()] = item

    def add(self, item: T) -> None:
        self._collection[item.key()] = item

    def filter_by(self, name: str, value: Any) -> MappedCollection[T]:
        return type(self)(
            [x for x in self._collection.values() if getattr(x, name) == value]
        )

    def first(self) -> Optional[T]:
        if not self._collection:
            return None
        return [*self._collection.values()][0]

    def __iter__(self) -> Iterator[T]:
        return iter(self._collection.values())

    def __contains__(self, item: T) -> bool:
        return item.key() in self._collection

    def __getitem__(self, item: str) -> T:
        return self._collection[item]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError

        return self._collection == other._collection
