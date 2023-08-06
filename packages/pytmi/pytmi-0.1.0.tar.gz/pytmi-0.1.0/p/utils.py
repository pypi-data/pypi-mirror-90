__all__ = []


hexdigits = list(map(str, list(range(10))))
hexalpha = ['a', 'b', 'c', 'd', 'e', 'f']
hexdigits.extend(hexalpha)
hexdigits.extend(list(map(str.upper, hexalpha)))


def ishex(s: str) -> bool:
    for c in s:
        if not c in hexdigits:
            return False
    return True


__all__.append(ishex)
