import hashlib
from typing import List, Tuple

def H(x: bytes) -> bytes:
    return hashlib.sha256(x).digest()

# (Optional but recommended) domain separation:
# leaf = H(b"\x00" + data)
# node = H(b"\x01" + left + right)
def merkle_root(datas: List[bytes]) -> bytes:
    if not datas:
        return H(b"")  # convention for empty tree

    level = [H(b"\x00" + d) for d in datas]  # leaf hashes

    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])  # duplicate last if odd

        nxt = []
        for i in range(0, len(level), 2):
            left, right = level[i], level[i + 1]
            nxt.append(H(b"\x01" + left + right))
        level = nxt

    return level[0]

# Returns a proof as a list of (sibling_hash, is_left_sibling)
# is_left_sibling=True means sibling is on the left of the current hash.
def merkle_proof(datas: List[bytes], index: int) -> List[Tuple[bytes, bool]]:
    if index < 0 or index >= len(datas):
        raise IndexError("index out of range")
    if not datas:
        raise ValueError("empty tree has no proofs")

    level = [H(b"\x00" + d) for d in datas]
    proof = []
    idx = index

    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])

        sibling_idx = idx ^ 1  # flip last bit: 0<->1, 2<->3, etc.
        sibling = level[sibling_idx]
        is_left_sibling = (sibling_idx < idx)
        proof.append((sibling, is_left_sibling))

        # move up
        nxt = []
        for i in range(0, len(level), 2):
            nxt.append(H(b"\x01" + level[i] + level[i + 1]))
        level = nxt
        idx //= 2

    return proof

def verify_proof(data: bytes, index: int, proof: List[Tuple[bytes, bool]], root: bytes) -> bool:
    cur = H(b"\x00" + data)
    idx = index
    for sibling, is_left_sibling in proof:
        if is_left_sibling:
            cur = H(b"\x01" + sibling + cur)
        else:
            cur = H(b"\x01" + cur + sibling)
        idx //= 2
    return cur == root
