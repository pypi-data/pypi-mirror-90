from __future__ import annotations

from collections import OrderedDict
from typing import Any, Callable, ClassVar, Dict, Generic, NamedTuple, Optional, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")
F = TypeVar("F", bound=Callable[..., Any])


class CacheInfo(NamedTuple):
    # pylint: disable=inherit-non-class, too-few-public-methods
    hits: int
    misses: int
    capacity: int
    current_size: int


class LRUCache(Generic[KT, VT]):
    """ Must use an OrderedDict in order to use the move_to_end() command """

    # class variable to map the decorator functions to their respective instance
    decorator_instance_map: ClassVar[Dict[Callable[..., Any], LRUCache[KT, VT]]] = {}

    def __init__(self, max_capacity: int) -> None:
        self.cache: OrderedDict[  # pylint: disable=unsubscriptable-object
            KT, VT
        ] = OrderedDict()
        self.max_capacity = max_capacity
        self.hits = 0
        self.misses = 0

    def __getitem__(self, key: KT) -> Optional[VT]:
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return self.cache[key]

        self.misses += 1
        return None

    def __setitem__(self, key: KT, val: VT) -> None:
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = val
        if len(self.cache) > self.max_capacity:
            self.cache.popitem(last=False)

    def __bool__(self) -> bool:
        return bool(self.cache)

    def __len__(self) -> int:
        return len(self.cache)

    def __contains__(self, key: KT) -> bool:
        return key in self.cache

    def __repr__(self) -> str:
        return str(
            CacheInfo(self.hits, self.misses, self.max_capacity, len(self.cache))
        )

    @classmethod
    def lru_cache(cls, size: int = 128) -> Callable[[F], Callable[..., Any]]:
        def cache_decorator_inner(func: F) -> Callable[..., Any]:
            def cache_decorator_wrapper(*args: Any, **kwargs: Any) -> Any:
                if func not in cls.decorator_instance_map:
                    cls.decorator_instance_map[func] = LRUCache(size)

                result = cls.decorator_instance_map[func][args]
                if result is None:
                    result = func(*args, **kwargs)
                    cls.decorator_instance_map[func][args] = result
                return result

            def cache_info() -> LRUCache[KT, VT]:
                return cls.decorator_instance_map[func]

            cache_decorator_wrapper.cache_info = cache_info  # type: ignore
            return cache_decorator_wrapper

        return cache_decorator_inner


def lru_cache(size: int = 128) -> Callable[[F], Callable[..., Any]]:
    return LRUCache.lru_cache(size)
