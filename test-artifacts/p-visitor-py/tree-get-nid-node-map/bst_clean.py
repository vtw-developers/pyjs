def Node(param_0, param_1):
    def __init__(label, parent):
        class_var.label = label
        class_var.parent = parent
        class_var.left = None
        class_var.right = None
    class_var = type('Node', (), {})()
    class_var.__init__ = __init__
    __init__(param_0, param_1)
    return class_var
def BinarySearchTree():
    def __init__():
        class_var.root = None
    def empty():
        class_var.root = None
    def is_empty():
        return class_var.root is None
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
                msg = f"Node with label {label} already exists"
                raise Exception(msg)
        return node
    def search(label):
        return class_var._search(class_var.root, label)
    def _search(node, label):
        if node is None:
            msg = f"Node with label {label} does not exist"
            raise Exception(msg)
        else:
            if label < node.label:
                node = class_var._search(node.left, label)
            elif label > node.label:
                node = class_var._search(node.right, label)
        return node
    def remove(label):
        node = class_var.search(label)
        if node.right and node.left:
            lowest_node = class_var._get_lowest_node(node.right)
            lowest_node.left = node.left
            lowest_node.right = node.right
            node.left.parent = lowest_node
            if node.right:
                node.right.parent = lowest_node
            class_var._reassign_nodes(node, lowest_node)
        elif not node.right and node.left:
            class_var._reassign_nodes(node, node.left)
        elif node.right and not node.left:
            class_var._reassign_nodes(node, node.right)
        else:
            class_var._reassign_nodes(node, None)
    def _reassign_nodes(node, new_children):
        if new_children:
            new_children.parent = node.parent
        if node.parent:
            if node.parent.right == node:
                node.parent.right = new_children
            else:
                node.parent.left = new_children
        else:
            class_var.root = new_children
    def _get_lowest_node(node):
        if node.left:
            lowest_node = class_var._get_lowest_node(node.left)
        else:
            lowest_node = node
            class_var._reassign_nodes(node, node.right)
        return lowest_node
    def exists(label):
        try:
            class_var.search(label)
            return True
        except Exception:
            return False
    def get_max_label():
        if class_var.root is None:
            raise Exception("Binary search tree is empty")
        node = class_var.root
        while node.right is not None:
            node = node.right
        return node.label
    def get_min_label():
        if class_var.root is None:
            raise Exception("Binary search tree is empty")
        node = class_var.root
        while node.left is not None:
            node = node.left
        return node.label
    def inorder_traversal():
        return class_var._inorder_traversal(class_var.root)
    def _inorder_traversal(node):
        if node is not None:
            yield from class_var._inorder_traversal(node.left)
            yield node
            yield from class_var._inorder_traversal(node.right)
    def preorder_traversal():
        return class_var._preorder_traversal(class_var.root)
    def _preorder_traversal(node):
        if node is not None:
            yield node
            yield from class_var._preorder_traversal(node.left)
            yield from class_var._preorder_traversal(node.right)
    class_var = type('BinarySearchTree', (), {})()
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
    return t
def test_put():
    t = BinarySearchTree()
    assert t.is_empty()
    t.put(8)
    assert t.root is not None
    assert t.root.parent is None
    assert t.root.label == 8
    t.put(10)
    assert t.root.right is not None
    assert t.root.right.parent == t.root
    assert t.root.right.label == 10
    t.put(3)
    assert t.root.left is not None
    assert t.root.left.parent == t.root
    assert t.root.left.label == 3
    t.put(6)
    assert t.root.left.right is not None
    assert t.root.left.right.parent == t.root.left
    assert t.root.left.right.label == 6
    t.put(1)
    assert t.root.left.left is not None
    assert t.root.left.left.parent == t.root.left
    assert t.root.left.left.label == 1
    try:
        t.put(1)
    except Exception:
        pass
def test_search():
    t = _get_binary_search_tree()
    node = t.search(6)
    assert node.label == 6
    node = t.search(13)
    assert node.label == 13
    try:
        t.search(2)
    except Exception:
        pass
def test_remove():
    t = _get_binary_search_tree()
    t.remove(13)
    assert t.root is not None
    assert t.root.right is not None
    assert t.root.right.right is not None
    assert t.root.right.right.right is None
    assert t.root.right.right.left is None
    t.remove(7)
    assert t.root.left is not None
    assert t.root.left.right is not None
    assert t.root.left.right.left is not None
    assert t.root.left.right.right is None
    assert t.root.left.right.left.label == 4
    t.remove(6)
    assert t.root.left.left is not None
    assert t.root.left.right.right is not None
    assert t.root.left.left.label == 1
    assert t.root.left.right.label == 4
    assert t.root.left.right.right.label == 5
    assert t.root.left.right.left is None
    assert t.root.left.left.parent == t.root.left
    assert t.root.left.right.parent == t.root.left
    t.remove(3)
    assert t.root is not None
    assert t.root.left.label == 4
    assert t.root.left.right.label == 5
    assert t.root.left.left.label == 1
    assert t.root.left.parent == t.root
    assert t.root.left.left.parent == t.root.left
    assert t.root.left.right.parent == t.root.left
    t.remove(4)
    assert t.root.left is not None
    assert t.root.left.left is not None
    assert t.root.left.label == 5
    assert t.root.left.right is None
    assert t.root.left.left.label == 1
    assert t.root.left.parent == t.root
    assert t.root.left.left.parent == t.root.left
def test_remove_2():
    t = _get_binary_search_tree()
    t.remove(3)
    assert t.root is not None
    assert t.root.left is not None
    assert t.root.left.left is not None
    assert t.root.left.right is not None
    assert t.root.left.right.left is not None
    assert t.root.left.right.right is not None
    assert t.root.left.label == 4
    assert t.root.left.right.label == 6
    assert t.root.left.left.label == 1
    assert t.root.left.right.right.label == 7
    assert t.root.left.right.left.label == 5
    assert t.root.left.parent == t.root
    assert t.root.left.right.parent == t.root.left
    assert t.root.left.left.parent == t.root.left
    assert t.root.left.right.left.parent == t.root.left.right
def test_empty():
    t = _get_binary_search_tree()
    t.empty()
    assert t.root is None
def test_is_empty():
    t = _get_binary_search_tree()
    assert not t.is_empty()
    t.empty()
    assert t.is_empty()
def test_exists():
    t = _get_binary_search_tree()
    assert t.exists(6)
    assert not t.exists(-1)
def test_get_max_label():
    t = _get_binary_search_tree()
    assert t.get_max_label() == 14
    t.empty()
    try:
        t.get_max_label()
    except Exception:
        pass
def test_get_min_label():
    t = _get_binary_search_tree()
    assert t.get_min_label() == 1
    t.empty()
    try:
        t.get_min_label()
    except Exception:
        pass
def test_inorder_traversal():
    t = _get_binary_search_tree()
    inorder_traversal_nodes = [i.label for i in t.inorder_traversal()]
    assert inorder_traversal_nodes == [1, 3, 4, 5, 6, 7, 8, 10, 13, 14]
def test_preorder_traversal():
    t = _get_binary_search_tree()
    preorder_traversal_nodes = [i.label for i in t.preorder_traversal()]
    assert preorder_traversal_nodes == [8, 3, 1, 6, 4, 5, 7, 10, 14, 13]
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
    print(    """
                8
               / \\
              3   10
             / \\    \\
            1   6    14
               / \\   /
              4   7 13
               \\
                5
            """    )
    print("Label 6 exists:", t.exists(6))
    print("Label 13 exists:", t.exists(13))
    print("Label -1 exists:", t.exists(-1))
    print("Label 12 exists:", t.exists(12))
    inorder_traversal_nodes = [i.label for i in t.inorder_traversal()]
    print("Inorder traversal:", inorder_traversal_nodes)
    preorder_traversal_nodes = [i.label for i in t.preorder_traversal()]
    print("Preorder traversal:", preorder_traversal_nodes)
    print("Max. label:", t.get_max_label())
    print("Min. label:", t.get_min_label())
    print("\nDeleting elements 13, 10, 8, 3, 6, 14")
    print(    """
              4
             / \\
            1   7
                 \\
                  5
            """    )
    t.remove(13)
    t.remove(10)
    t.remove(8)
    t.remove(3)
    t.remove(6)
    t.remove(14)
    inorder_traversal_nodes = [i.label for i in t.inorder_traversal()]
    print("Inorder traversal after delete:", inorder_traversal_nodes)
    preorder_traversal_nodes = [i.label for i in t.preorder_traversal()]
    print("Preorder traversal after delete:", preorder_traversal_nodes)
    print("Max. label:", t.get_max_label())
    print("Min. label:", t.get_min_label())
def test():
    binary_search_tree_example()
    test_put()
    test_search()
    test_remove()
    test_remove_2()
    test_is_empty()
    test_empty()
    test_exists()
    test_get_max_label()
    test_get_min_label()
    test_inorder_traversal()
    test_preorder_traversal()
test()