from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    key: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None


class SplayTree:
    def __init__(self):
        self.root: Optional[Node] = None

    # ---------- Rotations ----------
    def _rotate_left(self, x: Node) -> None:
        """Rotate x with its right child."""
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _rotate_right(self, x: Node) -> None:
        """Rotate x with its left child."""
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.right = x
        x.parent = y

    # ---------- Splaying ----------
    def _splay(self, x: Node) -> None:
        """Move x to the root using zig / zig-zig / zig-zag."""
        while x.parent is not None:
            p = x.parent
            g = p.parent

            if g is None:
                # Zig step
                if x is p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                # Zig-zig or zig-zag
                if x is p.left and p is g.left:
                    # Zig-zig (left-left)
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif x is p.right and p is g.right:
                    # Zig-zig (right-right)
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif x is p.right and p is g.left:
                    # Zig-zag (left-right)
                    self._rotate_left(p)
                    self._rotate_right(g)
                else:
                    # Zig-zag (right-left)
                    self._rotate_right(p)
                    self._rotate_left(g)

    # ---------- BST search (splays last accessed node) ----------
    def find(self, key: int) -> Optional[Node]:
        cur = self.root
        last = None
        while cur:
            last = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                self._splay(cur)
                return cur
        if last:
            self._splay(last)
        return None

    # ---------- Insert ----------
    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = Node(key)
            return

        cur = self.root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = Node(key, parent=cur)
                    self._splay(cur.left)
                    return
                cur = cur.left
            elif key > cur.key:
                if cur.right is None:
                    cur.right = Node(key, parent=cur)
                    self._splay(cur.right)
                    return
                cur = cur.right
            else:
                # already exists; splay it
                self._splay(cur)
                return

    # ---------- Delete ----------
    def delete(self, key: int) -> bool:
        node = self.find(key)
        if node is None or self.root is None or self.root.key != key:
            return False  # not found

        # Now node is at root
        left = self.root.left
        right = self.root.right
        if left:
            left.parent = None
        if right:
            right.parent = None

        # If no left subtree, right becomes root
        if left is None:
            self.root = right
            return True

        # Otherwise: make max of left subtree the new root, then attach right
        self.root = left
        # Find max in left subtree
        cur = self.root
        while cur.right:
            cur = cur.right
        self._splay(cur)  # splay max(left) to root
        # Attach right subtree
        self.root.right = right
        if right:
            right.parent = self.root
        return True

    # ---------- Helpers ----------
    def inorder(self) -> list[int]:
        out = []
        def dfs(x: Optional[Node]):
            if not x:
                return
            dfs(x.left)
            out.append(x.key)
            dfs(x.right)
        dfs(self.root)
        return out
