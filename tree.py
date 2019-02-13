class Node(object):
	_instances_ = -1
	def __init__(self, parent, *children):
		self._parent_ = parent
		parent.children.append(self)
		self._setChildren_(*children)
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
	def __delitem__(self, key: int):
		del self[key]
	def __contains__(self, node):
		return node in self.children

	def __str__(self):
		return self.getPath()
	def __len__(self):
		return len(self.children)
	def __del__(self):
		self._resetParent_()
		self._resetChildren_()
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
		node._children_ += self
	def _setChildren_(self, *nodes):
		for c in self.children: c._setParent_(orphanage)
		self._children_ = list(nodes) or []
		for n in nodes: n._setParent_(self)

	def _resetParent_(self):
		self.parent = orphanage
	def _resetChildren_(self):
		self.children = []


	def getDegree(self):
		return len(self)
	def getValency(self):
		self.getDegree()
	def getPath(self):
		ptr = self
		ascendance = ""
		while not isinstance(ptr.parent, Root):
			ascendance = f".{ptd_node.parent.index(ptd_node)}" + ascendance
			ptd_node = ptr.parent
		return ptr.name + ascendance
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
		return progeny
	def getLeaves(self):
		return [p for p in self.progeny if p.path.count(".") == self.depth]

	def totalProgeny(self):
		return len(self.progeny)
	def totalLeaves(self):
		return len(self.leaves)
	def totalPossibleCuts(self):
		return self.totalProgeny() - 1

	def display(self):
		root_sign = "# " if self.parent.isRoot() else ""
		print(root_sign + self.path)
	def displayRoot(self):
		print("# " + self.root.path)
		print("\t... " + self.path)
	def displayParent(self):
		root_sign = "# " if self.parent.isRoot() else ""
		print(root_sign + self.parent.path)
		print("\t" + self.path)
	def displayChildren(self):
		root_sign = "# " if self.isRoot() else ""
		print(root_sign + self.name)
		for c in self: print("\t" + c.name)
	def displayProgeny(self):
		print(self)
	def displayLeaves(self):
		print(self)

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
		return all(int(p.path.split(".")[-1]) < 2 for p in self.progeny)
	def isFanShaped(self):
		results = []
		for c in self: results.append(True if c.isLeaf() else False)
		return False not in results
	def isLeaf(self):
		return not len(self)

	def addChildren(self, *nodes):
		self._setChildren(*self.children, *nodes)
	def removeChildren(self, *children):
		new_children = [c for c in self.children if c not in children]
		self._setChildren(*new_children)


	clsInstances = classmethod(clsInstances)

	parent = property(_getParent_, _setParent_, _resetParent_)
	children = property(_getChildren_, _setChildren_, _resetChildren_)



class Root(Node):
	_instances_ = -1
	def __init__(self, name=None, *children):
		Node.__init__(self, None, *children)
		self._name = f"<{name}>" if name else f"<r{Root._instances}>"
		Root._instances_ += 1
	def __getattr__(self, attr):
		if attr is "path": return self.name
		elif attr in {"degree", "valency"}: return self.getDegree()
		elif attr is "path": return self.getPath()
		elif attr is "height": return self.getHeight()
		elif attr is "depth": return self.getDepth()
		elif attr is "root": return self.getRoot()
		elif attr is "progeny": return self.getProgeny()
		elif attr is "leaves": return self.getLeaves()
		else: raise AttributeError("No such attribute for Node instances exists")

	def clsInstances(cls):
		return Root._instances

	def _getName_(self):
		return self._name_
	def _setName_(self, name):
		self._name_ = f"<{name}>"

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
