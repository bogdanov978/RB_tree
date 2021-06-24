# encoding - UTF-8
from unittest import TestCase
from RB_tree import RbTree


class TestRbTree_insert(TestCase):
    def test_insert_left_red_right(self):
        # вставка нового элемента в качестве левого потомка красного узла, который является правым потомком своего родителя
        vals = [20, 15, 21, 18]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        tree.display()
        #
        tree.insert(17) # узел 17 будет левым потомком красного узла 18, который является правым потомком узла 15
        tree.display() # вывод перебалансированного дерева, исправлено нарушение красного свойства дерева (красный узел 17 был потомком красного узла 18)

    def test_insert_left_red_left(self):
        # вставка нового элемента в качестве левого потомка красного узла, который является правым потомком своего родителя
        vals = [20, 15, 21, 10]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        tree.display()
        #
        tree.insert(9) # узел 9 будет левым потомком красного узла 10, который является левым потомком узла 15
        tree.display()

    def test_insert_right_red_right(self):
        # вставка нового элемента в качестве правого потомка красного узла, который является правым потомком своего родителя
        vals = [20, 15, 21, 18]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        tree.display()
        #
        tree.insert(19) # узел 19 будет правым потомком красного узла 18, который является правым потомком узла 15
        tree.display()

    def test_insert_right_red_left(self):
        # вставка нового элемента в качестве правого потомка красного узла, который является левым потомком своего родителя
        vals = [20, 15, 21, 10]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        tree.display()
        #
        tree.insert(14) # узел 14 будет правым потомком красного узла 10, который является левым потомком узла 15
        tree.display()


class TestRbTree_find(TestCase):
    def test_find_failed(self):
        # попытка найти элемент, не представленный в дереве
        vals = [20, 10, 30, 5, 14, 25, 35, 1, 11, 17, 22, 26, 32, 36, 16, 18]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        tree.display()
        #
        self.assertIs(tree.find(15), None) # неудачный поиск заканчивается в левом поддереве
        self.assertIs(tree.find(19), None) # неудачный поиск заканчивается в правом поддереве

    def test_find_success(self):
        # попытка найти элемент, не представленный в дереве
        vals = [20, 10, 30, 5, 14, 25, 35, 1, 11, 17, 22, 26, 32, 36, 16, 18]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        tree.display()
        #
        self.assertIs(tree.find(16), 16) # удачный поиск заканчивается в левом поддереве
        self.assertIs(tree.find(26), 26) # удачный поиск заканчивается в правом поддереве


class TestRbTree_remove(TestCase):  # набор тестов для метода remove, осуществляющей удаление узла с заданным значением
    def test_remove_not_found(self):
        # попытка удалить элемент, не содержащийся в дереве
        vals = [10, 5, 12, 4, 6, 11, 14, 16]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        #
        self.assertIs(tree.remove(100), None)

    def test_remove_simple_red(self):
        # удаление красного листового узла
        vals = [10, 5, 12, 4, 6, 11, 14, 13]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        #
        self.assertEqual(tree.remove(13), 13)
        #tree.display()

    def test_remove_simple_black(self):
        # удаление черного узла с единственным красным листовым потомком (левым)
        vals = [10, 5, 12, 4, 6, 11, 14, 13]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        #
        self.assertEqual(tree.remove(14), 14)
        #tree.display()

    def test_remove_simple_black2(self):
        # удаление черного узла с двумя листовыми красными потомками
        vals = [10, 5, 12, 4, 6, 11, 14, 13]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        #
        self.assertEqual(tree.remove(5), 5)
        #tree.display()

    def test_remove_1_4_left(self):
        # удаляемый узел - листовой, черный, случаи 1-->4 в цикле функции remove.
        # на последней итерации цикла текущий узел (x) - корень левого поддерева своего родителя
        vals = [20, 10, 30, 5, 15, 25, 35, 6, 16, 26, 31, 36, 32]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        tree.remove(26)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        #
        self.assertEqual(tree.remove(25), 25)
        #tree.display()

    def test_remove_1_4_right(self):
        # удаляемый узел - листовой, черный, случаи 1-->4 в цикле функции remove.
        # на последней итерации цикла текущий узел (x) - корень правого поддерева своего родителя
        vals = [20, 10, 30, 5, 15, 25, 35, 3, 8, 16, 26, 36, 6]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        tree.remove(16)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        #
        self.assertEqual(tree.remove(15), 15)
        #tree.display()

    def test_remove_1_3_4_left(self):
        # удаляемый узел - листовой, черный, случаи 1-->3-->4 в цикле функции remove.
        # на последней итерации цикла текущий узел (x) - корень левого поддерева своего родителя
        vals = [20, 10, 30, 5, 15, 25, 35, 6, 16, 26, 31, 36, 30]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        tree.remove(26)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        #
        self.assertEqual(tree.remove(25), 25)
        #tree.display()

    def test_remove_1_3_4_right(self):
        # удаляемый узел - листовой, черный, случаи 1-->3-->4 в цикле функции remove.
        # на последней итерации цикла текущий узел (x) - корень правого поддерева своего родителя
        vals = [20, 10, 30, 5, 15, 25, 35, 3, 8, 16, 26, 36, 9]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        tree.remove(16)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        #
        self.assertEqual(tree.remove(15), 15)
        #tree.display()

    def test_remove_2_left_3_4_right(self):
        # удаляемый узел - листовой, черный, случаи 2-->3-->4 в цикле функции remove.
        # во время случая 2 текущий узел левый потомок своего родителя, для случаев 3-->4 - правый
        vals = [20, 10, 30, 5, 15, 25, 35, 1, 14, 16, 26, 36, 17]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        tree.remove(26)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        tree.remove(36)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        #
        self.assertEqual(tree.remove(25), 25)
        #tree.display()

    def test_remove_2_right_3_4_left(self):
        # удаляемый узел - листовой, черный, случаи 2-->3-->4 в цикле функции remove.
        # во время случая 2 текущий узел-правый потомок своего родителя, для случаев 3-->4 - левый
        vals = [20, 10, 30, 5, 15, 25, 35, 1, 14, 24, 27, 36, 26]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        tree.remove(1)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        tree.remove(14)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        #
        self.assertEqual(tree.remove(15), 15)
        #tree.display()

    def test_remove_root_2_left_3_4_right(self):
        # удаляемый узел - корень, минимальный узел правого поддерева удаляемого узла - черный, случаи 2-->3-->4 в цикле функции remove.
        # во время случая 2 текущий узел-левый потомок своего родителя, для случаев 3-->4 - правый
        vals = [20, 10, 30, 5, 15, 25, 35, 1, 14, 16, 26, 36, 17]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        tree.remove(26)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        tree.remove(36)  # удаление красного листового узла, чтобы его родитель (черный узел) стал листовым
        #
        self.assertEqual(tree.remove(20), 20)
        #tree.display()


class TestRbTree_bounds(TestCase):  # тестрование функций upper_bound, lower_bound, min, max
    def test_upper_bound(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 27, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertEqual(tree.upper_bound(24), 23)  # путь от корня до нижнего уровня дерева включает в себя узлы [20, 30, 23, 27, 25]
        self.assertEqual(tree.upper_bound(26), 25)  # путь от корня до нижнего уровня дерева включает в себя узлы [20, 30, 23, 27, 25]

    def test_upper_bound_equal(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 27, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertEqual(tree.upper_bound(27), 27) # случай когда значение-аргумент функции присутствует в дереве

    def test_upper_bound_not_found(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 27, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertIs(tree.upper_bound(0), None)  # случай когда значение-аргумент функции левее всех элементов в дереве

    def test_lower_bound(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertEqual(tree.lower_bound(29), 30)  # путь от корня до нижнего уровня дерева включает в себя узлы [20, 30, 23, 26, 28]
        self.assertEqual(tree.lower_bound(27), 28)  # путь от корня до нижнего уровня дерева включает в себя узлы [20, 30, 23, 26, 28]

    def test_lower_bound_equal(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertEqual(tree.lower_bound(26), 26) # случай когда значение-аргумент функции присутствует в дереве

    def test_lower_bound_not_found(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertIs(tree.lower_bound(100), None)  # случай когда значение-аргумент функции правее всех элементов в дереве

    def test_min(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        tree.display()
        self.assertEqual(tree.min(), 1)

    def test_max(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        tree.display()
        self.assertEqual(tree.max(), 36)


class TestRbTree_get(TestCase):
    def test_get_min(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertEqual(tree.get(0), tree.min())  # если представить дерево как отсортированную по возрастанию версию массива vals, то элемент в позиции 0 должен совпадать с минимальным элементом дерева

    def test_get_max(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertEqual(tree.get(len(vals)-1), tree.max())

    def test_get(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree()
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertEqual(tree.get(10), 28)


def descending_order(left, right):
    return left > right

class TestRbTree_predicates(TestCase):
    def test_descending(self):
        vals = [20, 10, 30, 5, 15, 23, 35, 1, 14, 21, 26, 34, 36, 25, 28]
        tree = RbTree(descending_order)
        for v in vals:
            tree.insert(v)
        #tree.display()
        self.assertEqual(tree.find(25), 25)
        self.assertIs(tree.find(24), None)

        self.assertEqual(tree.min(), max(vals))
        self.assertEqual(tree.max(), min(vals))

        self.assertEqual(tree.get(6), 25)

        self.assertEqual(tree.remove(21), 21)
        # tree.display()

