class Node(object):
	_instances_ = -1
	def __init__(self, parent, *children):
		self._parent_ = parent
		self._children_ = list(children) or []
		if parent is not None: parent.children.append(self)
		for n in children: n._setParent_(self)
		Node._instances_ += 1

	def __getattr__(self, attr):
		if attr in {"degree", "valency"}: return self.getDegree()
		elif attr is "path": return self.getPath()
		elif attr is "height": return self.getHeight()
		elif attr is "depth": return self.getDepth()
		elif attr is "root": return self.getRoot()
		elif attr is "progeny": return self.getProgeny()
		elif attr is "leaves": return self.getLeaves()
		else: raise AttributeError("No such attribute for Node instances exists")
	def __getitem__(self, key: int):
		return self.children[key]
	def __setitem__(self, key: int, node):
		self.removeChildren(self.getChild(key))
		if node not in self.children: self.children.insert(key, node)
		else: raise ValueError("Cannot have a node child several times!")
		node._setParent_(self)
	def __contains__(self, node):
		return node in self.children

	def __str__(self):
		return self.getPath()
	def __len__(self):
		return len(self.children)
	def __add__(self, node):
		return self.addChildren(node)
	def __sub__(self, node):
		return self.removeChildren(node)
	def __iadd__(self, node):
		self.addChildren(node)
	def __isub__(self, node):
		self.removeChildren(node)


	def clsInstances(cls):
		return Node._instances_

	def _getParent_(self):
		return self._parent_
	def _getChildren_(self):
		return self._children_

	def _setParent_(self, node):
		self._parent_.children.remove(self)
		self._parent_ = node
		node._children_.append(self)
	def _setChildren_(self, *nodes):
		for c in self.children: c._setParent_(orph)
		self._children_ = list(nodes) or []
		for n in nodes: n._setParent_(self)


	def getParent(self):
		self._getParent_()
	def getChildren(self):
		self._getChildren_()
	def getDegree(self):
		return len(self)
	def getValency(self):
		self.getDegree()
	def getPath(self):
		ptr = self
		path = ""
		while not isinstance(ptr, Root):
			path = f".{ptr.parent.children.index(ptr)}" + path
			ptr = ptr.parent
		return ptr.name + path
	def getHeight(self):
		return self.path.count(".")
	def getDepth(self):
		heights = []
		for p in self.progeny:
			heights.append(p.path.count("."))
		return max(heights)
	def getRoot(self):
		ptr = self
		while not ptr.isRoot(): ptr = ptr.parent
		return ptr
	def getProgeny(self):
		progeny = self.children
		while not all(p.isParent() for p in progeny):
			progeny.extend([p for p in progeny if p.isParent()])
		return sorted(progeny)
	def getLeaves(self):
		return sorted([p for p in self.progeny if p.path.count(".") == self.depth])

	def setParent(self, node):
		self._setParent_(node)
	def setChildren(self, *nodes):
		self._setChildren_(*nodes)

	def cut(self):
		self._setParent_(orph)
	def resetParent(self):
		self.cut()
	def resetChildren(self):
		self._setChildren_()

	def totalProgeny(self):
		return len(self.progeny)
	def totalLeaves(self):
		return len(self.leaves)
	def totalPossibleCuts(self):
		return self.totalProgeny() - 1

	def display(self):
		print(self)
	def displayRoot(self):
		print(self.root.path)
		print("┊\n└───" + self.path)
	def displayParent(self):
		print(self.parent.path)
		print("└───" + self.path)
	def displayChildren(self):
		print(self.path)
		if self.isParent():
			for c in self[:-1]: print("├───" + c.path)
			print("└───" + self[-1].path)
	def displayProgeny(self):
		print(self.path)
		for p in self.progeny:
			print("\t" * (p.path.count(".") - self.path.count(".")) + ("├───" if p is p.parent.child[-1] else "└───") + p.path)


	def displayLeaves(self):
		print(self)
	def displayTree(self):
		pass

	def isRoot(self):
		return isinstance(self, Root)
	def isEven(self):
		return not bool(len(self) % 2)
	def isOdd(self):
		return bool(len(self) % 2)
	def isParent(self, child=None):
		return child in self if child else not self.isLeaf()
	def isChild(self, parent=None):
		return self in parent if parent else not self.isRoot()
	def isSymmetric(self):
		pass
	def isBinary(self):
		return all(int(p.path.split(".")[-1]) == 1 for p in self.progeny)
	def isFanShaped(self):
		results = []
		for c in self: results.append(True if c.isLeaf() else False)
		return False not in results
	def isLeaf(self):
		return not len(self)

	def addChildren(self, *nodes):
		self._setChildren_(*self.children, *nodes)
	def removeChildren(self, *children):
		new_children = [c for c in self.children if c not in children]
		self._setChildren_(*new_children)


	clsInstances = classmethod(clsInstances)

	parent = property(_getParent_, _setParent_)
	children = property(_getChildren_, _setChildren_)



class Root(Node):
	_instances_ = -1
	def __init__(self, name=None, *children):
		Node.__init__(self, None, *children)
		self._name_ = f"<{name}>" if name else f"<r{Root._instances_}>"
		Root._instances_ += 1

	def __getattr__(self, attr):
		if attr is "path": return self.name
		elif attr in {"degree", "valency"}: return self.getDegree()
		elif attr is "height": return self.getHeight()
		elif attr is "depth": return self.getDepth()
		elif attr is "root": return self.getRoot()
		elif attr is "progeny": return self.getProgeny()
		elif attr is "leaves": return self.getLeaves()
		else: raise AttributeError("No such attribute for Root instances exists")

	def clsInstances(cls):
		return Root._instances

	def _getName_(self):
		return self._name_
	
	def _setName_(self, name):
		self._name_ = f"<{name}>"
	def _setParent_(self, node):
		pass

	def getName(self):
		self._getName_()
	def getPath(self):
		return self.name
	def getHeight(self):
		return 0
	def getRoot(self):
		return self

	def displayRoot(self):
		print(self)
	def displayParent(self):
		pass

	def isChild(self, parent=None):
		return False

	clsInstances = classmethod(clsInstances)
	name = property(_getName_, _setName_)

orph = Root("orph")
