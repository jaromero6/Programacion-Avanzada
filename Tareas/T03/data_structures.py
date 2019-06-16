# Este codigo se hizo con ayuda del codigo de la semana 6


class Node:
    def __init__(self, value):
        self.value = value
        self.next_node = None

    def __repr__(self):
        return f"{self.value}"


class List:
    def __init__(self, *args):
        self.head = None
        self.tail = None
        for i in args:
            self.append(i)
        self.current_node = self.head
        self.iterable = self.head

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.head.first_node = self.head
            self.tail = self.head
            return
        new_node.first_node = self.head
        self.tail.next_node = new_node
        self.tail = self.tail.next_node

    def insert(self, value, position):
        new_node = Node(value)
        current_node = self.head
        if position == 0:
            new_node.next_node = self.head
            self.head = new_node
            if new_node.next_node is None:
                self.tail = new_node
            return
        for i in range(position - 1):
            if current_node is not None:
                current_node = current_node.next_node
            else:
                raise ValueError("Index out of range")
        if current_node is not None:
            new_node.next_node = current_node.next_node
            current_node.next_node = new_node
            if new_node.next_node is None:
                self.tail = new_node

    def remove(self, id_node):
        if id_node > len(self) - 1:
            raise ValueError("Index out of range")
        if id_node == 0:
            if self.head is not None:
                self.head = self.head.next_node
            return
        previous_node = self[id_node - 1]
        remove_node = previous_node.next_node
        previous_node.next_node = remove_node.next_node

    def __getitem__(self, item):
        current_node = self.head
        for i in range(item):
            if current_node is not None:
                current_node = current_node.next_node
            else:
                raise ValueError("Index out of range")
        return current_node

    def __iter__(self):
        current_node = self.head
        while current_node is not None:
            yield current_node
            current_node = current_node.next_node

    def __len__(self):
        large = 0
        current_node = self.head
        while current_node is not None:
            large += 1
            current_node = current_node.next_node
        return large

    def __contains__(self, item):
        if type(item) is not Node:
            item_node = Node(item)
        else:
            item_node = item
        for i in self:
            if i.value == item_node.value and type(i.value) == type(
                    item_node.value):
                return True
        return False

    def __repr__(self):
        string = "["
        current_node = self.head
        while current_node is not None:
            string = f"{string}{current_node.value},"
            current_node = current_node.next_node
        return string.strip(",") + "]"


class GraphNode:
    def __init__(self, id_node, value):
        self.id_node = id_node
        self.value = value
        self.children = List()

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        index_child = 0
        for i in self.children:
            if i.value == child:
                break
            index_child += 1
        self.children.remove(index_child)

    def __repr__(self):
        return f"{self.value}"


"""
Este grafo funciona con un nodo principal que une hijos, solo se pueden 
agregar conexiones entre el nodo principal y los hijos, pero no entre hijos
Funcionamiento: 
      nodes es una lista de instancias de Node
      value de cada nodo es un graph_node
      value de cada graph_node es la instancia
"""


class Graph:
    def __init__(self, id_main, main_node):
        self.main_node = GraphNode(id_main, main_node)
        self.nodes = List()

    def get_node(self, id_node):
        for i in self.nodes:
            if i.value.id_node == id_node:
                return i.value

    def exist_path(self, to):
        return Node(self.get_node(to)) in self.main_node.children

    def add_node(self, node_id, value):
        added_node = GraphNode(node_id, value)
        self.nodes.append(added_node)

    def add_connection(self, to_id):
        self.main_node.add_child(self.get_node(to_id))

    def remove_connection(self, to_id):
        if self.exist_path(to_id):
            self.main_node.remove_child(self.get_node(to_id))
            return
        raise ValueError  # Se levanta un error que luego "se reemplaza" al
        # ejecutar este metodo en entities

    def __iter__(self):
        for i in self.main_node.children:
            yield i.value.value

    def __contains__(self, item):
        for i in self:
            if item == i and type(item) == type(i):
                return True
        return False

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        return f"{self.nodes}"


"""
Funciona igual que una lista solo que le asigna un id a casa elemento, 
lo que permite acceder de forma más comoda a estos
"""


class IdNode:
    def __init__(self, id_node, value):
        self.id_node = id_node
        self.value = value
        self.next_node = None

    def __repr__(self):
        return f"{self.value}"


class IdList:
    def __init__(self, *args):
        self.head = None
        self.tail = None
        cont = 0
        for i in args:
            self.append(cont, i)
            cont += 1

    def append(self, id_, value):
        new_node = IdNode(id_, value)
        if self.head is None:
            self.head = new_node
            self.tail = self.head
            return
        self.tail.next_node = new_node
        self.tail = self.tail.next_node

    def remove(self, id_node):
        previous_node = None
        for i in self:
            if i.id_node == id_node:
                break
            if previous_node is None:
                previous_node = self.head
            else:
                previous_node = previous_node.next_node
        if previous_node is None:  # Si se trato de sacar el primer nodo
            if self.head is not None:
                self.head = self.head.next_node
            return
        remove_node = previous_node.next_node
        if remove_node is None:  # El ultimo elemento de la lista
            self.tail = previous_node
        else:
            previous_node.next_node = remove_node.next_node

    def __getitem__(self, id_item):
        for i in self:
            if i.id_node == id_item:
                return i

    def __iter__(self):
        current_node = self.head
        while current_node is not None:
            yield current_node
            current_node = current_node.next_node

    def __len__(self):
        large = 0
        current_node = self.head
        while current_node is not None:
            large += 1
            current_node = current_node.next_node
        return large

    def __contains__(self, item):
        for i in self:
            if i.id_node == item:
                return True
        return False

    def __repr__(self):
        string = "["
        current_node = self.head
        while current_node is not None:
            string = f"{string}{current_node.value},"
            current_node = current_node.next_node
        return string.strip(",") + "]"
