class Node(object):
	"""Node, a.k.a vertex, of a tree."""
	def __init__(self, parent=None, name=None, *children):
		self.parent, self.children = None, []
		self.setParent(parent)
		self.setChildren(*children)
		self.name = self.parent.name + "." + (name or str(len(self.parent) - 1)) if self.isChild() else name or "r"

	def __getitem__(self, index: int):
		return self.children[index]
	def __setitem__(self, index: int, node):
		self.children[index] = node
	def __delitem__(self, index: int):
		del self[index]
	def __str__(self):
		return self.name
	def __len__(self):
		return len(self.children)
	def __del__(self):
		self.resetParent()
		self.resetChildren()
		del self

	def getName(self):
		return str(self)
	def getDegree(self):
		return len(self)
	def getParent(self):
		return self.parent
	def getChild(self, index: int):
		return self[index]
	def getChildren(self):
		return self.children

	def isRoot(self):
		return not self.getParent()
	def isParent(self, child=None):
		return child in self if child else not self.isLeaf()
	def isChild(self, parent=None):
		return self in parent if parent else not self.isRoot()
	def isLeaf(self):
		return not len(self)

	def setName(self, name):
		self.name = name
	def setParent(self, parent=None):
		if self.isChild(): self.getParent().children.remove(self)
		self.parent = parent
		if parent is not None:
			if self not in parent.getChildren(): parent.children.append(self)
	def setChildren(self, *children):
		for c in self: c.setParent(None)
		self.children = list(children) or []
		for c in children:
			if self != c.getParent(): c.setParent(self)

	def rename(self, name):
		self.setName(name)
	def resetParent(self):
		self.setParent()
	def resetChildren(self):
		self.setChildren()

	def addChildren(self, *children):
		for c in children:
			if c not in self.children: self.children.append(children)
			c.setParent(self)
	def removeChildren(self, *children):
		for c in children: c.setParent(None)
		self.children = [n for n in self if n not in children]

	def recursiveDel(self):
		if self.isLeaf():
			del self
		else:
			for c in self: c.recursiveDel()
