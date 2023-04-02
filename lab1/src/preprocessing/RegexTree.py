class RegexTree:
    def __init__(self):
        self.root = None

    def add(self, node):
        if self.root is None:
            self.root = node
        elif self.root.leftChild is None:
            self.root.leftChild = node
        elif self.root.rightChild is None:
            self.root.rightChild = node

    @staticmethod
    def create(rootNode, leftNode, rightNode=None):
        tree = RegexTree()
        tree.root = rootNode
        tree.root.leftChild = leftNode
        tree.root.rightChild = rightNode

        return tree
