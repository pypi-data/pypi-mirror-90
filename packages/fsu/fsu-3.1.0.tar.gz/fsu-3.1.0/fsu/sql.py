from typing import Any, Callable, List, NamedTuple, Tuple

class SQLBuilder(NamedTuple):
    build   : Callable[[str], Tuple[str, List[Any]]]
    arg     : Callable[[Any], str]
    setcols : Callable[[Any], str]

def make_builder() -> SQLBuilder:
    args : List[Any] = []
    counter          = 0

    def build(s : str) -> Tuple[str, List[Any]]:
        nonlocal args, counter

        ret_args, args = args, []
        counter = 0

        return s, ret_args

    def arg(v : Any) -> str:
        nonlocal counter
        counter += 1

        k = f"${counter}"
        args.append(v)

        return k

    def setcols(d) -> str:
        return ", ".join((f"{k} = {arg(v)}" for k, v in d.items()))

    return SQLBuilder(
        build   = build,
        arg     = arg,
        setcols = setcols,
    )
