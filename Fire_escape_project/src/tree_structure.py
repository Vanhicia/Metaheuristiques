class Node:
    """ A Node is defined by
    - its father
    - its son list
    """

    def __init__(self):
        self._father=None
        self._sons=[]

    def __init__(self, father):
        self._father=father
        self._sons=[]

    def add_son(self, son):
        self._sons.append(son)


class Tree:
    """ ATree is defined by
        - its root (node)
        """

    def __init__(self, node):
        self._root=node