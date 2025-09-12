from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Dict

@dataclass
class _Node:
    key: Any
    val: Any
    prev: Optional["_Node"] = None
    next: Optional["_Node"] = None

class LRUCache:
    """
    Classic LRU with O(1) get/put using:
      - dict: key -> node
      - doubly linked list: head <-> ... <-> tail
        (MRU near head, LRU near tail)
    get(k) -> value or -1 if missing (LeetCode-style)
    """
    def __init__(self, capacity: int):
        assert capacity > 0
        self.cap = capacity
        self.map: Dict[Any, _Node] = {}
        # sentinels
        self.head = _Node(None, None)
        self.tail = _Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    # ----- list helpers -----
    def _add_front(self, node: _Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove(self, node: _Node) -> None:
        p, n = node.prev, node.next
        p.next = n
        n.prev = p
        node.prev = node.next = None

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._add_front(node)

    def _pop_lru(self) -> _Node:
        node = self.tail.prev
        self._remove(node)
        return node

    # ----- API -----
    def get(self, key: Any) -> Any:
        node = self.map.get(key)
        if not node:
            return -1
        self._move_to_front(node)
        return node.val

    def put(self, key: Any, value: Any) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._move_to_front(node)
            return
        node = _Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.cap:
            lru = self._pop_lru()
            del self.map[lru.key]

    def __len__(self) -> int:
        return len(self.map)
