class Node(object):
	"""
	A node, a.k.a vertex, of a tree in graph theory.

	Nodes are the base of what's called a tree.
	They are linked together with edges, with exaclty one path between all nodes.
	This class has many methods to set up arborescence and get information about it.

	:param parent: The node which preceed this one.
	:param name: The name of the node.
	:param *children: Nodes whose descend from it.
	:type parent: Node
	:type name: str
	:type *children: Node

	.. seealso:: class Tree(Node)
	"""
	def __init__(self, parent=None, name=None, *children):
		self._parent, self._name, self._children = None, None, []
		self._parent = parent
		self._setChildren(*children)
		self._setName(name)

	def __getitem__(self, key: int):
		return self.children[key]
	def __setitem__(self, key: int, node):
		self.removeChildren(self.getChild(key))
		if node not in self.children: self.children.insert(key, node)
		else: raise ValueError("Cannot have a node child several times!")
		node.setParent(self)
	def __delitem__(self, key: int):
		del self[key]
	def __contains__(self, node):
		return node in self.children

	def __str__(self):
		return self.name
	def __len__(self):
		return len(self.children)
	def __del__(self):
		del self.parent
		del self.children
		del self

	def __add__(self, node):
		return self.addChildren(node)
	def __sub__(self, node):
		return self.removeChildren(node)
	def __iadd__(self, node):
		self.addChildren(node)
	def __isub__(self, node):
		self.removeChildren(node)


	def _getParent(self):
		return self._parent
	def _getName(self):
		return self._name
	def _getChildren(self):
		return self._children

	def _setParent(self, node=None):
		if self.isChild(): self.parent.children.remove(self)
		self._parent = node
		if node is not None:
			self._name = self.parent.name + "." + self.name
			if self not in node.getChildren(): node.children.append(self)
	def _setName(self, name=None):
		self._name = self.parent.name + "." + (name or str(len(self.parent) - 1)) if self.isChild() else name or "r"
	def _setChildren(self, *nodes):
		for c in self: c.parent = None
		self._children = list(nodes) or []
		for c in nodes:
			if self != c.parent: c.parent = self

	def _resetParent(self):
		self.parent = None
	def _resetName(self):
		self.name = None
	def _resetChildren(self):
		self._children = []


	def getDegree(self):
		return len(self)
	def getHeight(self):
		return self.name.count(".")
	def getLevel(self):
		pass

	def totalDescendents(self):
		pass
	def totalLeaves(self):
		pass

	def isRoot(self):
		return not self.parent
	def isParent(self, child=None):
		return child in self if child else not self.isLeaf()
	def isChild(self, parent=None):
		return self in parent if parent else not self.isRoot()
	def isSymmetric(self):
		results = []
		for n in self: results.append(True if n == self[0] else False)
		return False not in results
	def isBinary(self):
		pass
	def isFanShaped(self):
		results = []
		for c in self.children: results.append(True if c.isLeaf() else False)
		return False not in results
	def isLeaf(self):
		return not len(self)

	def addChildren(self, *nodes):
		for n in nodes:
			if n not in self.children: self.children.append(nodes)
			n.parent = self
	def removeChildren(self, *children):
		for c in children: c.parent = None
		self._children = [n for n in self if n not in children]

	def displayStruct(self):
		print(self)

	def recursiveDel(self):
		if self.isLeaf():
			del self
		else:
			for c in self: c.recursiveDel()


	parent = property(_getParent, _setParent, _resetParent)
	name = property(_getName, _setName, _resetName)
	children = property(_getChildren, _setChildren, _resetChildren)
