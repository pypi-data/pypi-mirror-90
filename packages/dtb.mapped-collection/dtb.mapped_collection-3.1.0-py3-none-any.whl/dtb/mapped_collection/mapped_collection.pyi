from __future__ import annotations

from typing import Collection, Dict, List, Protocol, TypeVar, Iterator, Iterable, Any, Optional


class WithKey(Protocol):
    def key(self) -> str:
        ...


T = TypeVar("T", bound=WithKey)


class MappedCollection(Iterable[T]):
    _collection: Dict[str, T]

    def __init__(self, items: Iterable[T]) -> None:
        ...

    def add(self, item: T) -> None:
        ...

    def filter_by(self, name: str, value: Any) -> MappedCollection[T]:
        ...

    def first(self) -> Optional[T]:
        ...

    def __iter__(self) -> Iterator[T]:
        ...

    def __contains__(self, item: T) -> bool:
        ...

    def __getitem__(self, item: str) -> T:
        ...

    def __eq__(self, other: object) -> bool:
        ...
