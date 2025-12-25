def Node(param_0, param_1):
    def __init__(label, parent):
        class_var.label = label
        class_var.parent = parent
        class_var.left = None
        class_var.right = None
    Clz = type('Node', (), {})
    class_var = Clz()
    class_var.__init__ = __init__
    __init__(param_0, param_1)
    return class_var
def BinarySearchTree():
    def __init__():
        class_var.root = None
    def empty():
        pass
    def is_empty():
        pass
    def put(label):
        class_var.root = class_var._put(class_var.root, label, None)
    def _put(node, label, parent):
        if node is None:
            node = Node(label, parent)
        else:
            if label < node.label:
                node.left = class_var._put(node.left, label, node)
            elif label > node.label:
                node.right = class_var._put(node.right, label, node)
            else:
                pass
        return node
    def search(label):
        pass
    def _search(node, label):
        pass
    def remove(label):
        pass
    def _reassign_nodes(node, new_children):
        pass
    def _get_lowest_node(node):
        pass
    def exists(label):
        pass
    def get_max_label():
        pass
    def get_min_label():
        pass
    def inorder_traversal():
        pass
    def _inorder_traversal(node):
        pass
    def preorder_traversal():
        pass
    def _preorder_traversal(node):
        pass
    Clz = type('BinarySearchTree', (), {})
    class_var = Clz()
    class_var.__init__ = __init__
    class_var.empty = empty
    class_var.is_empty = is_empty
    class_var.put = put
    class_var._put = _put
    class_var.search = search
    class_var._search = _search
    class_var.remove = remove
    class_var._reassign_nodes = _reassign_nodes
    class_var._get_lowest_node = _get_lowest_node
    class_var.exists = exists
    class_var.get_max_label = get_max_label
    class_var.get_min_label = get_min_label
    class_var.inorder_traversal = inorder_traversal
    class_var._inorder_traversal = _inorder_traversal
    class_var.preorder_traversal = preorder_traversal
    class_var._preorder_traversal = _preorder_traversal
    __init__()
    return class_var
def _get_binary_search_tree():
    pass
def test_put():
    pass
def test_search():
    pass
def test_remove():
    pass
def test_remove_2():
    pass
def test_empty():
    pass
def test_is_empty():
    pass
def test_exists():
    pass
def test_get_max_label():
    pass
def test_get_min_label():
    pass
def test_inorder_traversal():
    pass
def test_preorder_traversal():
    pass
def binary_search_tree_example():
    t = BinarySearchTree()
    t.put(8)
    t.put(3)
    t.put(6)
    t.put(1)
    t.put(10)
    t.put(14)
    t.put(13)
    t.put(4)
    t.put(7)
    t.put(5)
    print("""
                8
               / \\
              3   10
             / \\    \\
            1   6    14
               / \\   /
              4   7 13
               \\
                5
            """)
def test():
    binary_search_tree_example()
test()
