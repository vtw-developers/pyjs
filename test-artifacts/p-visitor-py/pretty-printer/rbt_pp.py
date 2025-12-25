def RedBlackTree(param_0, param_1, param_2, param_3, param_4):
    def __init__(label, color, parent, left, right):
        class_var.label = label
        class_var.parent = parent
        class_var.left = left
        class_var.right = right
        class_var.color = color
    def rotate_left():
        parent = class_var.parent
        right = class_var.right
        if right is None:
            return class_var
        class_var.right = right.left
        if class_var.right:
            class_var.right.parent = class_var
        class_var.parent = right
        right.left = class_var
        if parent is not None:
            if ((hasattr(parent.left, '__eq__') and parent.left.__eq__(class_var)) or (not hasattr(parent.left, '__eq__') and parent.left == class_var)):
                parent.left = right
            else:
                parent.right = right
        right.parent = parent
        return right
    def rotate_right():
        if class_var.left is None:
            return class_var
        parent = class_var.parent
        left = class_var.left
        class_var.left = left.right
        if class_var.left:
            class_var.left.parent = class_var
        class_var.parent = left
        left.right = class_var
        if parent is not None:
            if parent.right is class_var:
                parent.right = left
            else:
                parent.left = left
        left.parent = parent
        return left
    def insert(label):
        if class_var.label is None:
            class_var.label = label
            return class_var
        if class_var.label == label:
            return class_var
        elif class_var.label > label:
            if class_var.left:
                class_var.left.insert(label)
            else:
                class_var.left = RedBlackTree(label, 1, class_var, None, None)
                class_var.left._insert_repair()
        else:
            if class_var.right:
                class_var.right.insert(label)
            else:
                class_var.right = RedBlackTree(label, 1, class_var, None, None)
                class_var.right._insert_repair()
        return class_var.parent or class_var
    def _insert_repair():
        if class_var.parent is None:
            class_var.color = 0
        elif get_color(class_var.parent) == 0:
            class_var.color = 1
        else:
            uncle = class_var.parent.sibling()
            if get_color(uncle) == 0:
                if class_var.is_left() and class_var.parent.is_right():
                    class_var.parent.rotate_right()
                    if class_var.right:
                        class_var.right._insert_repair()
                elif class_var.is_right() and class_var.parent.is_left():
                    class_var.parent.rotate_left()
                    if class_var.left:
                        class_var.left._insert_repair()
                elif class_var.is_left():
                    if class_var.grandparent():
                        class_var.grandparent().rotate_right()
                        class_var.parent.color = 0
                    if class_var.parent.right:
                        class_var.parent.right.color = 1
                else:
                    if class_var.grandparent():
                        class_var.grandparent().rotate_left()
                        class_var.parent.color = 0
                    if class_var.parent.left:
                        class_var.parent.left.color = 1
            else:
                class_var.parent.color = 0
                if uncle and class_var.grandparent():
                    uncle.color = 0
                    class_var.grandparent().color = 1
                    class_var.grandparent()._insert_repair()
    def remove(label):
        if class_var.label == label:
            if class_var.left and class_var.right:
                value = class_var.left.get_max()
                if value is not None:
                    class_var.label = value
                    class_var.left.remove(value)
            else:
                child = class_var.left or class_var.right
                if class_var.color == 1:
                    if class_var.parent:
                        if class_var.is_left():
                            class_var.parent.left = None
                        else:
                            class_var.parent.right = None
                else:
                    if child is None:
                        if class_var.parent is None:
                            return RedBlackTree(None)
                        else:
                            class_var._remove_repair()
                            if class_var.is_left():
                                class_var.parent.left = None
                            else:
                                class_var.parent.right = None
                            class_var.parent = None
                    else:
                        class_var.label = child.label
                        class_var.left = child.left
                        class_var.right = child.right
                        if class_var.left:
                            class_var.left.parent = class_var
                        if class_var.right:
                            class_var.right.parent = class_var
        elif class_var.label is not None and class_var.label > label:
            if class_var.left:
                class_var.left.remove(label)
        else:
            if class_var.right:
                class_var.right.remove(label)
        return class_var.parent or class_var
    def _remove_repair():
        if (class_var.parent is None or class_var.sibling() is None or class_var.parent.sibling() is None or class_var.grandparent() is None):
            return
        if get_color(class_var.sibling()) == 1:
            class_var.sibling().color = 0
            class_var.parent.color = 1
            if class_var.is_left():
                class_var.parent.rotate_left()
            else:
                class_var.parent.rotate_right()
        if (get_color(class_var.parent) == 0 and get_color(class_var.sibling()) == 0 and get_color(class_var.sibling().left) == 0 and get_color(class_var.sibling().right) == 0):
            class_var.sibling().color = 1
            class_var.parent._remove_repair()
            return
        if (get_color(class_var.parent) == 1 and get_color(class_var.sibling()) == 0 and get_color(class_var.sibling().left) == 0 and get_color(class_var.sibling().right) == 0):
            class_var.sibling().color = 1
            class_var.parent.color = 0
            return
        if (class_var.is_left() and get_color(class_var.sibling()) == 0 and get_color(class_var.sibling().right) == 0 and get_color(class_var.sibling().left) == 1):
            class_var.sibling().rotate_right()
            class_var.sibling().color = 0
            if class_var.sibling().right:
                class_var.sibling().right.color = 1
        if (class_var.is_right() and get_color(class_var.sibling()) == 0 and get_color(class_var.sibling().right) == 1 and get_color(class_var.sibling().left) == 0):
            class_var.sibling().rotate_left()
            class_var.sibling().color = 0
            if class_var.sibling().left:
                class_var.sibling().left.color = 1
        if (class_var.is_left() and get_color(class_var.sibling()) == 0 and get_color(class_var.sibling().right) == 1):
            class_var.parent.rotate_left()
            class_var.grandparent().color = class_var.parent.color
            class_var.parent.color = 0
            class_var.parent.sibling().color = 0
        if (class_var.is_right() and get_color(class_var.sibling()) == 0 and get_color(class_var.sibling().left) == 1):
            class_var.parent.rotate_right()
            class_var.grandparent().color = class_var.parent.color
            class_var.parent.color = 0
            class_var.parent.sibling().color = 0
    def check_color_properties():
        if class_var.color:
            print("Property 2")
            return False
        if not class_var.check_coloring():
            print("Property 4")
            return False
        if class_var.black_height() is None:
            print("Property 5")
            return False
        return True
    def check_coloring():
        if class_var.color == 1 and 1 in (get_color(class_var.left), get_color(class_var.right)):
            return False
        if class_var.left and not class_var.left.check_coloring():
            return False
        if class_var.right and not class_var.right.check_coloring():
            return False
        return True
    def black_height():
        if class_var is None or class_var.left is None or class_var.right is None:
            return 1
        left = class_var.left.black_height()
        right = class_var.right.black_height()
        if left is None or right is None:
            return None
        if left != right:
            return None
        return left + (1 - class_var.color)
    def __contains__(label):
        return class_var.search(label) is not None
    def search(label):
        if class_var.label == label:
            return class_var
        elif class_var.label is not None and label > class_var.label:
            if class_var.right is None:
                return None
            else:
                return class_var.right.search(label)
        else:
            if class_var.left is None:
                return None
            else:
                return class_var.left.search(label)
    def floor(label):
        if class_var.label == label:
            return class_var.label
        elif class_var.label is not None and class_var.label > label:
            if class_var.left:
                return class_var.left.floor(label)
            else:
                return None
        else:
            if class_var.right:
                attempt = class_var.right.floor(label)
                if attempt is not None:
                    return attempt
            return class_var.label
    def ceil(label):
        if class_var.label == label:
            return class_var.label
        elif class_var.label is not None and class_var.label < label:
            if class_var.right:
                return class_var.right.ceil(label)
            else:
                return None
        else:
            if class_var.left:
                attempt = class_var.left.ceil(label)
                if attempt is not None:
                    return attempt
            return class_var.label
    def get_max():
        if class_var.right:
            return class_var.right.get_max()
        else:
            return class_var.label
    def get_min():
        if class_var.left:
            return class_var.left.get_min()
        else:
            return class_var.label
    def grandparent():
        if class_var.parent is None:
            return None
        else:
            return class_var.parent.parent
    def sibling():
        if class_var.parent is None:
            return None
        elif class_var.parent.left is class_var:
            return class_var.parent.right
        else:
            return class_var.parent.left
    def is_left():
        if class_var.parent is None:
            return False
        return class_var.parent.left is class_var.parent.left is class_var
    def is_right():
        if class_var.parent is None:
            return False
        return class_var.parent.right is class_var
    def __len__():
        ln = 1
        if class_var.left:
            ln += len(class_var.left)
        if class_var.right:
            ln += len(class_var.right)
        return ln
    def preorder_traverse():
        yield class_var.label
        if class_var.left:
            yield from class_var.left.preorder_traverse()
        if class_var.right:
            yield from class_var.right.preorder_traverse()
    def inorder_traverse():
        if class_var.left:
            yield from class_var.left.inorder_traverse()
        yield class_var.label
        if class_var.right:
            yield from class_var.right.inorder_traverse()
    def postorder_traverse():
        if class_var.left:
            yield from class_var.left.postorder_traverse()
        if class_var.right:
            yield from class_var.right.postorder_traverse()
        yield class_var.label
    def __eq__(other):
        if other.__class__.__name__ != class_var.__class__.__name__:
            return NotImplemented
        if class_var.label == other.label:
            return ((hasattr(class_var.left, '__eq__') and class_var.left.__eq__(other.left)) or (not hasattr(class_var.left, '__eq__') and class_var.left == other.left)) and ((hasattr(class_var.right, '__eq__') and class_var.right.__eq__(other.right)) or (not hasattr(class_var.right, '__eq__') and class_var.right == other.right))
        else:
            return False
    Clz = type('RedBlackTree', (), {})
    class_var = Clz()
    class_var.__init__ = __init__
    class_var.rotate_left = rotate_left
    class_var.rotate_right = rotate_right
    class_var.insert = insert
    class_var._insert_repair = _insert_repair
    class_var.remove = remove
    class_var._remove_repair = _remove_repair
    class_var.check_color_properties = check_color_properties
    class_var.check_coloring = check_coloring
    class_var.black_height = black_height
    class_var.__contains__ = __contains__
    class_var.search = search
    class_var.floor = floor
    class_var.ceil = ceil
    class_var.get_max = get_max
    class_var.get_min = get_min
    class_var.grandparent = grandparent
    class_var.sibling = sibling
    class_var.is_left = is_left
    class_var.is_right = is_right
    class_var.__len__ = __len__
    class_var.preorder_traverse = preorder_traverse
    class_var.inorder_traverse = inorder_traverse
    class_var.postorder_traverse = postorder_traverse
    class_var.__eq__ = __eq__
    __init__(param_0, param_1, param_2, param_3, param_4)
    return class_var
def get_color(node):
    if node is None:
        return 0
    else:
        return node.color
def test_rotations():
    tree = RedBlackTree(0, 0, None, None, None)
    tree.left = RedBlackTree(-10, 0, tree, None, None)
    tree.right = RedBlackTree(10, 0, tree, None, None)
    tree.left.left = RedBlackTree(-20, 0, tree.left, None, None)
    tree.left.right = RedBlackTree(-5, 0, tree.left, None, None)
    tree.right.left = RedBlackTree(5, 0, tree.right, None, None)
    tree.right.right = RedBlackTree(20, 0, tree.right, None, None)
    left_rot = RedBlackTree(10, 0, None, None, None)
    left_rot.left = RedBlackTree(0, 0, left_rot, None, None)
    left_rot.left.left = RedBlackTree(-10, 0, left_rot.left, None, None)
    left_rot.left.right = RedBlackTree(5, 0, left_rot.left, None, None)
    left_rot.left.left.left = RedBlackTree(-20, 0, left_rot.left.left, None, None)
    left_rot.left.left.right = RedBlackTree(-5, 0, left_rot.left.left, None, None)
    left_rot.right = RedBlackTree(20, 0, left_rot, None, None)
    tree = tree.rotate_left()
    assert ((hasattr(tree, '__eq__') and tree.__eq__(left_rot)) or (not hasattr(tree, '__eq__') and tree == left_rot))
    tree = tree.rotate_right()
    tree = tree.rotate_right()
    right_rot = RedBlackTree(-10, 0, None, None, None)
    right_rot.left = RedBlackTree(-20, 0, right_rot, None, None)
    right_rot.right = RedBlackTree(0, 0, right_rot, None, None)
    right_rot.right.left = RedBlackTree(-5, 0, right_rot.right, None, None)
    right_rot.right.right = RedBlackTree(10, 0, right_rot.right, None, None)
    right_rot.right.right.left = RedBlackTree(5, 0, right_rot.right.right, None, None)
    right_rot.right.right.right = RedBlackTree(20, 0, right_rot.right.right, None, None)
    assert ((hasattr(tree, '__eq__') and tree.__eq__(right_rot)) or (not hasattr(tree, '__eq__') and tree == right_rot))
    return True
def test_insertion_speed():
    tree = RedBlackTree(-1, 0, None, None, None)
    for i in range(10):
        tree = tree.insert(i)
    return True
def test_insert():
    tree = RedBlackTree(0, 0, None, None, None)
    tree.insert(8)
    tree.insert(-8)
    tree.insert(4)
    tree.insert(12)
    tree.insert(10)
    tree.insert(11)
    ans = RedBlackTree(0, 0, None, None, None)
    ans.left = RedBlackTree(-8, 0, ans, None, None)
    ans.right = RedBlackTree(8, 1, ans, None, None)
    ans.right.left = RedBlackTree(4, 0, ans.right, None, None)
    ans.right.right = RedBlackTree(11, 0, ans.right, None, None)
    ans.right.right.left = RedBlackTree(10, 1, ans.right.right, None, None)
    ans.right.right.right = RedBlackTree(12, 1, ans.right.right, None, None)
    return ((hasattr(tree, '__eq__') and tree.__eq__(ans)) or (not hasattr(tree, '__eq__') and tree == ans))
def test_insert_and_search():
    tree = RedBlackTree(0, 0, None, None, None)
    tree.insert(8)
    tree.insert(-8)
    tree.insert(4)
    tree.insert(12)
    tree.insert(10)
    tree.insert(11)
    assert not (((hasattr(tree, '__contains__') and tree.__contains__(5)) or (not hasattr(tree, '__contains__') and 5 in tree)) or ((hasattr(tree, '__contains__') and tree.__contains__(-6)) or (not hasattr(tree, '__contains__') and -6 in tree)) or ((hasattr(tree, '__contains__') and tree.__contains__(-10)) or (not hasattr(tree, '__contains__') and -10 in tree)) or ((hasattr(tree, '__contains__') and tree.__contains__(13)) or (not hasattr(tree, '__contains__') and 13 in tree)))
    assert (((hasattr(tree, '__contains__') and tree.__contains__(11)) or (not hasattr(tree, '__contains__') and 11 in tree)) and ((hasattr(tree, '__contains__') and tree.__contains__(12)) or (not hasattr(tree, '__contains__') and 12 in tree)) and ((hasattr(tree, '__contains__') and tree.__contains__(-8)) or (not hasattr(tree, '__contains__') and -8 in tree)) and ((hasattr(tree, '__contains__') and tree.__contains__(0)) or (not hasattr(tree, '__contains__') and 0 in tree)))
    return True
def test_insert_delete():
    tree = RedBlackTree(0, 0, None, None, None)
    tree = tree.insert(-12)
    tree = tree.insert(8)
    tree = tree.insert(-8)
    tree = tree.insert(15)
    tree = tree.insert(4)
    tree = tree.insert(12)
    tree = tree.insert(10)
    tree = tree.insert(9)
    tree = tree.insert(11)
    tree = tree.remove(15)
    tree = tree.remove(-12)
    tree = tree.remove(9)
    assert tree.check_color_properties()
    assert list(tree.inorder_traverse()) == [-8, 0, 4, 8, 10, 11, 12]
    return True
def test_floor_ceil():
    tree = RedBlackTree(0, 0, None, None, None)
    tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    tuples = [(-20, None, -16), (-10, -16, 0), (8, 8, 8), (50, 24, None)]
    for val, floor, ceil in tuples:
        assert tree.floor(val) == floor and tree.ceil(val) == ceil
    return True
def test_min_max():
    tree = RedBlackTree(0, 0, None, None, None)
    tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    assert tree.get_max() == 24 and tree.get_min() == -16
    return True
def test_tree_traversal():
    tree = RedBlackTree(0, 0, None, None, None)
    tree = tree.insert(-16)
    tree.insert(16)
    tree.insert(8)
    tree.insert(24)
    tree.insert(20)
    tree.insert(22)
    assert list(tree.inorder_traverse()) == [-16, 0, 8, 16, 20, 22, 24]
    assert list(tree.preorder_traverse()) == [0, -16, 16, 8, 22, 20, 24]
    assert list(tree.postorder_traverse()) == [-16, 8, 20, 24, 22, 16, 0]
    return True
def test_tree_chaining():
    tree = RedBlackTree(0, 0, None, None, None)
    tree = tree.insert(-16).insert(16).insert(8).insert(24).insert(20).insert(22)
    assert list(tree.inorder_traverse()) == [-16, 0, 8, 16, 20, 22, 24]
    assert list(tree.preorder_traverse()) == [0, -16, 16, 8, 22, 20, 24]
    assert list(tree.postorder_traverse()) == [-16, 8, 20, 24, 22, 16, 0]
    return True
def print_results(msg, passes):
    print(str(msg), "works!" if passes else "doesn't work :|")
def test():
    print_results("Rotating right and left", test_rotations())
    print_results("Inserting", test_insert())
    print_results("Searching", test_insert_and_search())
    print_results("Deleting", test_insert_delete())
    print_results("Floor and ceil", test_floor_ceil())
    print_results("Min and max", test_min_max())
    print_results("Tree traversal", test_tree_traversal())
    print_results("Tree traversal", test_tree_chaining())
    print("Testing tree balancing...")
    print("This should only be a few seconds.")
    test_insertion_speed()
    additional_tests()
    print("Done!")
def additional_tests():
    tree = RedBlackTree(0, 0, None, None, None)
    assert tree.__len__() == 1
    tree = RedBlackTree(0, 0, None, None, None)
    tree.insert(-16).insert(16).insert(-8).insert(12)
    tree.insert(-20).insert(8).insert(-4).insert(4)
    tree.insert(-3).insert(24).insert(-20).insert(20)
    tree.insert(-1).insert(2).insert(-3).insert(3)
    tree.insert(10).insert(26)
    tree.right.right.left._remove_repair()
    assert tree.right.right.left.label == 20
test()