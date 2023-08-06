from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Permissions:
    _bits: int

    def __and__(self, rhs: Permissions) -> Permissions:
        return Permissions(self._bits & rhs._bits)

    def __or__(self, rhs: Permissions) -> Permissions:
        return Permissions(self._bits | rhs._bits)

    def __xor__(self, rhs: Permissions) -> Permissions:
        return Permissions(self._bits ^ rhs._bits)

    @property
    def economy(self):
        return bool(self._bits & 0x1)
