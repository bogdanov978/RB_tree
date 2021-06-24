# RB_tree
Красно-Черное дерево
Функция, задающая способ сортировки задается аргументом конструктора predicate
Объектам класса доступны следующие операции:
  * insert(val) - вставка 
  * remove(val) - удаление
  * find(val) - поиск
  * min() / max() - получение минимального/максимального элемента в дереве, с учетом отношения порядка, задаваемого функцией predicate
  * upper_bound(val) - получение элемента, ближайшего слева от val (само значение val может и не присутствовать в дереве) 
  * lower_bound(val) - получение элемента, ближайшего справа от val 
  * get(index) - получение элемента, находящегося в позиции index, если представить содержимое дерева как массив, отсортированный с учетом отношения порядка, задаваемого функцией predicate
Сложность всех представленных операций - O(log(N)), где N-число элементов в дереве
