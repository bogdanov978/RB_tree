# encoding - UTF-8

def ascending_order(left, right):
    return left < right


class RbTree:
    class Node:
        def __init__(self, item, parent, side, left_child, right_child):
            self.item = item
            self.N = 1
            self.child = [left_child, right_child]  # указатели на дочерние вершины, child[0] - левое поддерево, child[1] - правое
            self.is_red = True # все узлы при создании имеют красный цвет
            self.parent = parent
            self.side = side

        def __del__(self):
            #print(self.item, "Node deleted!")
            pass

        def __str__(self):
            return "{item} {color}: [ {left} {right} ] {size}".format(
                item=self.item,
                color="R" if self.is_red else "B",
                left=self.child[0].item,
                right=self.child[1].item,
                size=self.N)

    def __init__(self, predicate = ascending_order):
        """
        predicate: функция, задающая отношение строгого порядка для объектов, находящихся в узлах конкретного экземпляра класса RbTree.
        строгость требуется так как выражение !predicate(a,b) and !predicate(b, a) --> a == b, позволяет устанавливать равенстсво значений,
        убирая необходимость определения дополнительного оператора равентсва
        """
        self.__leaf = RbTree.Node(None, None, 0, None, None)  # общий для всего дерева объект-лист, на который узлы, имеющие ноль или один дочерний узел, ссылаются "пустой" ссылкой
        self.__leaf.is_red = False  # все листья - черные
        self.__leaf.N = 0  # листья не увеличивают размер содержащих их поддеревьев
        self.__head = RbTree.Node(None, None, 0, self.__leaf, self.__leaf)  # фиктивный узел-корень, настоящий корень, с обработки которого начинаются все операции (вставка, поиск, удаление etc.) будет находиться в левом поддереве фиктивного узла
        self.predicate = predicate

    @staticmethod
    def __rotR(cur_n):
        x = cur_n.child[0]
        cur_n.parent.child[cur_n.side] = x  # x объявляется потомком родителя cur_n, на x указывает та же ссылка, что и ранее указывала на cur_n
        x.side = cur_n.side  # изначально x-левый потомок, но cur_n может быть как правым потомком, так и левым, поэтому данное присваивание необходимо
        x.parent = cur_n.parent  # родитель cur_n объявляется родителем x
        # правое поддерево х становится левым поддеревом cur_n:
        cur_n.child[0] = x.child[1]
        if x.child[1].item is not None: # если правый потомок x - общий для всего дерева объект-лист, то поля этого объекта не меняются
            x.child[1].parent = cur_n
            x.child[1].side = 0
        # cur_n становится правым потомком x:
        x.child[1] = cur_n
        cur_n.parent = x
        cur_n.side = 1
        #
        x.N = cur_n.N
        cur_n.N -= 1 + x.child[0].N
        return x

    @staticmethod
    def __rotL(cur_n):
        x = cur_n.child[1]
        cur_n.parent.child[cur_n.side] = x  # x объявляется потомком родителя cur_n, на x указывает та же ссылка, что и ранее указывала на cur_n
        x.side = cur_n.side  # изначально x-правый потомок, но cur_n может быть как правым потомком, так и левым, поэтому данное присваивание необходимо
        x.parent = cur_n.parent
        # левое поддерево х становится правым поддеревом cur_n:
        cur_n.child[1] = x.child[0]
        if x.child[0].item is not None:  # если левый потомок x - общий для всего дерева объект-лист, то поля этого объекта не меняются
            x.child[0].child[1].parent = cur_n
            x.child[0].child[1].side = 1
        # cur_n становится левым потомком x
        x.child[0] = cur_n
        cur_n.parent = x
        cur_n.side = 0
        #
        x.N = cur_n.N
        cur_n.N -= 1 + x.child[1].N
        return x

    def __insert(self, cur_n:Node, new_item):
        cur_n.N += 1 # размер поддеревьев, посещенных в результате рекурсивных вызовов, увеличивается на 1
        #  при движении вниз по дереву 4-узлы разбиваются путем перекрашивания, потенциально нарушая красные свойства дерева (два красных узла подряд).
        #  после вставки элемента в нижнюю часть дерева начинается подъем вверх по дереву исправляя нарушения красных свойств
        if cur_n.child[0].is_red and cur_n.child[1].is_red:
            cur_n.is_red = True
            cur_n.child[0].is_red = False
            cur_n.child[1].is_red = False

        if self.predicate(new_item, cur_n.item):  # вставляемый объект находится левее текущего узла -> дальнейшие операции проводятся для левого поддерева
            if cur_n.child[0].item is None:
                cur_n.child[0] = RbTree.Node(new_item, cur_n, 0, self.__leaf, self.__leaf)  # вставка нового элемента в соответствующую позицию
            else:
                self.__insert(cur_n.child[0], new_item)  # рекурсивный вызов, продвижение вниз по дереву

            if cur_n.is_red and cur_n.child[0].is_red and cur_n.side == 1:
                cur_n = RbTree.__rotR(cur_n)

            if cur_n.child[0].is_red and cur_n.child[0].child[0].is_red:
                cur_n = RbTree.__rotR(cur_n)
                cur_n.is_red = False
                cur_n.child[1].is_red = True
        else:  # вставляемый объект находится правее текущего узла (или равен ему) -> дальнейшие операции проводятся для правого поддерева
            if cur_n.child[1].item is None:
                cur_n.child[1] = RbTree.Node(new_item, cur_n, 1, self.__leaf, self.__leaf)
            else:
                self.__insert(cur_n.child[1], new_item)

            if cur_n.is_red and cur_n.child[1].is_red and cur_n.side == 0:
                cur_n = RbTree.__rotL(cur_n)

            if cur_n.child[1].is_red and cur_n.child[1].child[1].is_red:
                cur_n = RbTree.__rotL(cur_n)
                cur_n.is_red = False
                cur_n.child[0].is_red = True

    def __find(self, val):  # возвращает ссылку на узел, содержащий заданный объект
        cur_n = self.__head.child[0]  # изначально cur_n указывает на корень дерева
        while True:
            #print("find:", cur_n.item)
            if self.predicate(val, cur_n.item):  # искомый объект находится левее текущего узла
                if cur_n.child[0].item is None:  # текущий узел не имеет левого потомка
                    return None  # поиск неудачен
                cur_n = cur_n.child[0]
            elif self.predicate(cur_n.item, val):  # искомый объект находится правее текущего узла
                if cur_n.child[1].item is None: # текущий узел не имеет правого потомка
                    return None # поиск неудачен
                cur_n = cur_n.child[1]
            else:  # если оба условия выше не выполнены, то item == cur_n.item
                return cur_n

    @staticmethod
    def __min(root):
        """
        возвращает узел, содержащий наименьшее значение в поддереве с корнем в узле root
        """
        cur_n = root
        while cur_n.child[0].item is not None:
            cur_n = cur_n.child[0]
        return cur_n

    def insert(self, val):
        if self.__head.child[0].item is None:
            self.__head.child[0] = RbTree.Node(val, self.__head, 0, self.__leaf, self.__leaf)
        else:
            self.__insert(self.__head.child[0], val)
        self.__head.child[0].is_red = False

    def find(self, val):
        result = self.__find(val)
        return result.item if result is not None else None

    def remove(self, val):
        d_node = self.__find(val)
        if d_node is None:
            return None

        def transplant(u, v):
            u.parent.child[u.side] = v
            v.side = u.side
            v.parent = u.parent

        y = d_node
        y_original_is_red = y.is_red
        if y.child[0].item is None:
            x = y.child[1]
            transplant(y, x)
        elif y.child[1].item is None:
            x = y.child[0]
            transplant(y, x)
        else:
            y = RbTree.__min(y.child[1])  # возвращает самый левый узел правого поддерева удаляемого узла
            y_original_is_red = y.is_red
            x = y.child[1]
            if y.parent is d_node:
                x.parent = y  # имеет смысл когда x - листовой узел, общий для всего класса, в ином случае y уже является родителем x
            else:
                transplant(y, x)
                y.child[1] = d_node.child[1]
                y.child[1].parent = y
            transplant(d_node, y)
            y.child[0] = d_node.child[0]
            y.child[0].parent = y
            y.is_red = d_node.is_red
            y.N = d_node.N  # размер y оказывается больше рельного размера на 1, как и у всех вершин на пути от корня дерева до вершины х

        if y_original_is_red is False: # если удаляемый узел-черный
            while x.parent is not self.__head and x.is_red is False: # идея цикла в проталкивании "излишней черноты", которой обладает текущая вершина (x), вверх по дереву до нахождения красного узла
                if x.side == 0:  # x - корень левого поддерева своего родителя
                    sibling = x.parent.child[1]  # переменная, указывающая на "брата" x
                    # случай 1: брат x красный, в результате следующих строк новый брат x гарантировано черный, случай 1 сводится к случаю 2, 3 или 4 в зависимости от цветов потомков нового брата
                    if sibling.is_red:
                        sibling.is_red = False
                        x.parent.is_red = True
                        RbTree.__rotL(x.parent)
                        sibling = x.parent.child[1]
                    # во всех рассмотренных ниже случаях (2, 3, 4) брат x - черный
                    # случай 2: оба потомка брата ("племянники")- черные, перекрашивание брата и подъем выше по дереву, переход к новой итерации цикла.
                    if sibling.child[0].is_red is False and sibling.child[1].is_red is False:
                        sibling.is_red = True
                        x.parent.N -= 1
                        x = x.parent
                    else:
                        # случай 3: правый (дальний от х) племянник - черный --> приведение к ситуации, когда дальний от x потомок брата гарантированно красный, переход к случаю 4
                        if sibling.child[1].is_red is False:
                            sibling.child[0].is_red = False
                            sibling.is_red = True
                            RbTree.__rotR(sibling)
                            sibling = x.parent.child[1]
                        # случай 4: правый (дальний от х) племянник - красный --> путем перекрашивания и одной ротации красно-черные свойства дерева восстановлены, выход из цикла
                        sibling.is_red = x.parent.is_red
                        x.parent.is_red = False
                        sibling.child[1].is_red = False
                        RbTree.__rotL(x.parent)
                        break
                else:  # дублирования кода можно избежать, вычисляя индекс поддеревьев как 1-x.side
                       # и добавив условные операторы перед выполнением ротаций, но в целях облегчения понимания случаи разделены
                    sibling = x.parent.child[0]
                    if sibling.is_red:
                        sibling.is_red = False
                        x.parent.is_red = True
                        RbTree.__rotR(x.parent)
                        sibling = x.parent.child[0]

                    if sibling.child[0].is_red is False and sibling.child[1].is_red is False:
                        sibling.is_red = True
                        x.parent.N -= 1
                        x = x.parent
                    else:
                        if sibling.child[0].is_red is False:
                            sibling.child[1].is_red = False
                            sibling.is_red = True
                            RbTree.__rotL(sibling)
                            sibling = x.parent.child[0]

                        sibling.is_red = x.is_red
                        x.parent.is_red = False
                        sibling.child[0].is_red = False
                        RbTree.__rotR(x.parent)
                        break
            x.is_red = False
        # подъем до корня дерева и уменьшение размера всех узлов по пути
        x = x.parent
        while x is not self.__head:
            x.N -= 1
            x = x.parent

        return d_node.item

    def upper_bound(self, val):
        """
        возвращает самое правое (относительно отношения порядка, заданного предикатом) значение, которое находится перед значением val ( val может и не присутствовать в дереве) или None если такого значения нет
        """
        cur_n = self.__head.child[0]
        result = None
        while True:
            print(cur_n.item)
            if self.predicate(cur_n.item, val):  # значение в текущем узле левее val
                result = cur_n.item  # значение текущего узла считается искомым результатом, однако в правом поддереве текущего узла может содержаться более подходящий результат x: cur_n.item < x < val
                if cur_n.child[1].item is None:  # текущий узел не имеет правого потомка
                    break  # выход из цикла, result указывает на искомое значение
                cur_n = cur_n.child[1]  # новый текущий узел - правый потомок, переход к следующей итерации
            elif self.predicate(val, cur_n.item):  # значение в текущем узле правее val, искомый результат может находиться только в левом поддереве
                if cur_n.child[0].item is None:  # текущий узел не имеет левого потомка
                    break  # поддерево с корнем в текущем узле не содержит искомого результата. result указывает на искомое значение если условие cur_n.item < val было выполнено хоть раз на пути от корня дерева до текущего узла
                cur_n = cur_n.child[0]  # новый текущий узел - левый потомок, переход к следующей итерации
            else:  # если оба условия выше не выполнены, то item == cur_n.item обрабатывать этот случай можно по-разному в зависимости от того, хотим ли мы получить значение == val в качестве результата функции или нас интересует только значение строго левее val
                # случай когда значения узлов == val считаются результатом функции:
                result = cur_n.item
                break
                # для случая, когда эти значения не должны быть возвращены, достаточно не делать различий между случаями val < cur_n.item и val == cur_n.item
        return result

    def lower_bound(self, val):
        """
        возвращает самое левое (относительно отношения порядка, заданного предикатом) значение, которое находится после значения val ( val может и не присутствовать в дереве) или None если такого значения нет
        """
        cur_n = self.__head.child[0]
        result = None
        while True:
            print(cur_n.item)
            if self.predicate(cur_n.item, val):
                if cur_n.child[1].item is None:
                    break
                cur_n = cur_n.child[1]
            elif self.predicate(val, cur_n.item):
                result = cur_n.item
                if cur_n.child[0].item is None:
                    break
                cur_n = cur_n.child[0]
            else:
                result = cur_n.item
                break

        return result

    def min(self):
        return RbTree.__min(self.__head.child[0]).item

    def max(self):
        cur_n = self.__head.child[0]
        while cur_n.child[1].item is not None:
            cur_n = cur_n.child[1]
        return cur_n.item

    def get(self, index):
        """
        возвращает значение узла, находящегося в позиции index, если представить содержимое дерева как отсортированный (критерий - predicate) массив
        """
        cur_n = self.__head.child[0]
        t = cur_n.child[0].N  # количество элементов в левом поддереве текущего узла
        while t != index:  # если число узлов в левом поддереве текущего узла == index, то текущий узел- искомый (так как счет позиций index ведется от 0)
            if t > index:  # левое поддерево текущего узла содержит количество элементов > index
                cur_n = cur_n.child[0] # поиск продолжается в левом поддереве
            else:  # левое поддерево текущего узла содержит количество элементов < index --> искомый элемент находится в правом поддереве
                index -= (t + 1)  # так как поиск продолжится в правом поддереве текущего узла, из индекса вычитаются размер левого поддерева текущего узла + 1 (текущий узел)
                cur_n = cur_n.child[1]  # поиск продолжается в правом поддереве

            t = cur_n.child[0].N

        return cur_n.item

    def display(self):
        def display_rec(cur_n):
            print(cur_n)
            if cur_n.child[0].item is not None:
                display_rec(cur_n.child[0])
            if cur_n.child[1].item is not None:
                display_rec(cur_n.child[1])

        display_rec(self.__head.child[0])
        print("")
