"""A three-node ledger for the consult-gate tests: one decision, one rejected
alternative under it, importable without any real ledger's build cost."""


class _Node:
    def __init__(self, id, kind, children=()):
        self.id, self.kind, self.children = id, kind, list(children)


class _Root:
    def __init__(self, children):
        self.children = children


class _Quern:
    def __init__(self, children):
        self.root = _Root(children)


def build():
    return _Quern([_Node("use-the-front-door", "decision",
                         [_Node("alt-the-window", "alternative")])])
