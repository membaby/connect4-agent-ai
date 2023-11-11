class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child):
        child.parent = None
        self.children.remove(child)

    def get_children(self):
        return self.children

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None

    def depth(self):
        if self.is_root():
            return 0
        else:
            return self.parent.depth() + 1

    def height(self):
        if self.is_leaf():
            return 0
        else:
            return max(child.height() for child in self.children) + 1

    def size(self):
        if self.is_leaf():
            return 1
        else:
            return 1 + sum(child.size() for child in self.children)

    def print_tree(self):
        spaces = ' ' * 4 * self.depth()
        prefix = spaces + '|__ ' if self.parent else ''
        print(prefix + str(self.data))
        for child in self.children:
            child.print_tree()

