def multidim_accessor(multilist: list, *indexes: int):
	return multilist if not len(indexes) else multidim_accessor(multilist[indexes[0]], *indexes[1:])

class Node(object):
	_instances_ = -1
	def __init__(self, parent, *children):
		self._parent_ = parent
		self._children_ = list(children) or []
		if parent is not None: parent.children.append(self)
		for n in children: n.setParent(self)
		Node._instances_ += 1

	def __getattr__(self, attr):
			if attr in {"path", "name"}: return self.getPath()
			elif attr is "indexes": return self.getIndexes()
			elif attr is "struct": return self.getStruct()
			elif attr is "ancestors": return self.getAncestors()
			elif attr is "progeny": return self.getProgeny()
			elif attr is "siblings": return self.getSiblings()
			elif attr is "niblings": return self.getNiblings()
			elif attr is "piblings": return self.getPiblings()
			elif attr is "cousins": return self.getCousins()
			elif attr is "degree": return self.getDegree()
			elif attr is "height": return self.getHeight()
			elif attr is "depth": return self.getDepth()
			elif attr is "root": return self.getRoot()
			elif attr is "leaves": return self.getLeaves()
			elif attr is "tree_name": return self.getTreeName()
			elif attr is "tree_struct": return self.getTreeStruct()
			elif attr is "tree_nodes": return self.getTreeNodes()
			elif attr is "tree_leaves": return self.getTreeLeaves()
			else: raise AttributeError(f"Attribute \"{attr}\" not found for Node instance")
	def __getitem__(self, key: int):
		return self.children[key]
	def __setitem__(self, key: int, node):
		self.removeChildren(self.getChild(key))
		if node not in self.children: self.children.insert(key, node)
		else: raise ValueError("Cannot contains the same node several times")
		node.setParent(self)
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

	def getPath(self):
		ptr = self
		path = ""
		while not isinstance(ptr, Root):
			path = f".{ptr.parent.children.index(ptr)}" + path
			ptr = ptr.parent
		return ptr.name + path
	def getName(self):
		return self.path
	def getIndexes(self):
		indexes = self.name[self.name.rfind(">.") + 2:].split(".")
		for i in range(len(indexes)): indexes[i] = int(indexes[i])
		return tuple(indexes)
	def getStruct(self):
		struct = []
		for p in self.progeny: multidim_accessor(struct, *p.indexes[:-1]).append([])
		return struct
	def getParent(self):
		return self._parent_
	def getChildren(self):
		return self._children_
	def getSiblings(self):
		return sorted([s for s in self.parent.children if s is not self], key=lambda node: node.path)
	def getAncestors(self):
		ancestors = []
		ptr = self
		while not ptr.isRoot():
			ancestors.append(ptr.parent)
			ptr = ptr.parent
		return sorted(ancestors, key=lambda node: node.path)
	def getProgeny(self):
		progeny = self.children
		ptrs = self.children
		while not all(n.isLeaf() for n in ptrs):
			children = []
			for n in ptrs:
				for i in range(len(n)): children.append(n[i])
			progeny.extend(children)
			ptrs = children
		return sorted(list(set(progeny)), key=lambda node: node.path)
	def getDegree(self):
		return len(self)
	def getHeight(self):
		return self.path.count(".")
	def getDepth(self):
		heights = []
		for p in self.progeny: heights.append(p.path.count("."))
		return max(heights)
	def getRoot(self):
		ptr = self
		while not ptr.isRoot(): ptr = ptr.parent
		return ptr
	def getLeaves(self):
		return sorted([p for p in self.progeny if p.path.count(".") == self.depth], key=lambda node: node.path)

	def setParent(self, node):
		self._parent_.children.remove(self)
		self._parent_ = node
		node._children_.append(self)
	def setChildren(self, *nodes):
		for c in self._children_: c.setParent(orph)
		self._children_ = list(nodes) or []
		for n in nodes: n.setParent(self)
	def setStruct(self, struct: list):  # TODO: write method
		pass

	def resetParent(self):
		self.cutBefore()
	def resetChildren(self):
		self.cutAfter()

	def totalChildren(self):
		return len(self)
	def totalSiblings(self):
		return len(self.siblings)
	def totalAncestors(self):
		return len(self.ancestors)
	def totalProgeny(self):
		return len(self.progeny)
	def totalLeaves(self):
		return len(self.leaves)
	def totalPossibleCuts(self):
		return self.totalProgeny() - 1

	def display(self, tabs=3):
		self.displayProgeny(tabs)
	def displayStruct(self): # TODO: write method
		pass
	def displayParent(self):
		print(self.parent.path)
		print("\t└───" + self.path)
	def displayChildren(self):
		print(self.path)
		if self.isParent():
			for c in self[:-1]: print("├───" + c.path)
			print("└───" + self[-1].path)
		else:
			print("\t└───╳")
	def displaySiblings(self):
		self.parent.displayChildren()
	def displayAncestors(self, tabs=3):
		depth = 0
		print(self.root)
		for a in self.ancestors[1:] + [self]:
			print("\t" + "\t" * tabs * depth + "└───" + a.path)
			depth += 1
	def displayProgeny(self, tabs=3): # TODO: upgrade method
		print(self.path)
		for p in self.progeny:
			print(" \t" + "\t" * tabs * (p.path.count(".") - self.path.count(".") - 1) + ("└───" if p is p.parent.children[-1] else "├───") + p.path)
	def displayRoot(self):
		print(self.root.path)
		print("\t┊\n\t└───" + self.path)
	def displayLeaves(self): # TODO: continue method
		print(self)
	def displayTree(self, tabs=3):
		self.root.displayProgeny(tabs)

	def isRoot(self):
		return isinstance(self, Root)
	def isEven(self):
		return not bool(len(self) % 2)
	def isOdd(self):
		return bool(len(self) % 2)
	def isParent(self, *children):
		results = []
		for c in children: results.append(c in self.children)
		return False not in results and self.children
	def isChild(self, parent=None):
		return self in parent if parent else not self.isRoot()
	def isOrphan(self):
		return self.root.isOrphanage()
	def isSymmetric(self): # TODO: write method
		pass
	def isBinary(self): # TODO: fix method
		return all(int(p.path.split(".")[-1]) == 1 for p in self.progeny)
	def isFanShaped(self):
		results = []
		for c in self: results.append(True if c.isLeaf() else False)
		return False not in results
	def isLeaf(self):
		return not len(self)

	def hasParent(self, parent=None):
		return self.isChild(parent)
	def hasChildren(self, min=None, max=None, *children):
		results = []
		if min is not None: results.append(len(self.children) >= min)
		if max is not None: results.append(len(self.children) <= max)
		results.append(self.isParent(*children))
		return False not in results
	def hasSiblings(self, min=None, max=None, *siblings):
		results = []
		if min is not None: results.append(len(self.siblings) >= min)
		if max is not None: results.append(len(self.siblings) <= max)
		for s in siblings: results.append(s in self.siblings)
		return False not in results and self.siblings
	def hasAncestors(self, min=None, max=None, *ancestors):
		results = []
		if min is not None: results.append(len(self.ancestors) >= min)
		if max is not None: results.append(len(self.ancestors) <= max)
		for a in ancestors: results.append(a in self.ancestors)
		return False not in results and not self.isRoot()
	def hasProgeny(self, min=None, max=None, *progeny):
		results = []
		if min is not None: results.append(len(self.progeny) >= min)
		if max is not None: results.append(len(self.progeny) <= max)
		for p in progeny: results.append(p in self.progeny)
		return False not in results and not self.isLeaf()

	def grow(self, count: int):
		for _ in range(count): Node(self)
	def cutBefore(self):
		self.setParent(orph)
	def cutAfter(self):
		self.setChildren()

	def addChildren(self, *nodes):
		self.setChildren(*self.children, *nodes)
	def removeChildren(self, *children):
		new_children = [c for c in self.children if c not in children]
		self.setChildren(*new_children)

	def extend(self, struct: list): # TODO: write method
		pass
	def shrink(self, struct: list): # TODO: write method
		pass
	def restrain(self, struct: list): # TODO: write method
		pass

	clsInstances = classmethod(clsInstances)

	parent = property(getParent, setParent)
	children = property(getChildren, setChildren)


class Root(Node):
	_instances_ = -1
	def __init__(self, name=None, *children):
		Node.__init__(self, None, *children)
		self._name_ = f"<{name}>"  if name is not None else f"<root{Root._instances_}>"
		Root._instances_ += 1
	def __getattr__(self, attr):
		if attr is "path": return self.name
		elif attr is "struct": return self.getStruct()
		elif attr is "progeny": return self.getProgeny()
		elif attr is "degree": return self.getDegree()
		elif attr is "height": return self.getHeight()
		elif attr is "depth": return self.getDepth()
		elif attr is "root": return self.getRoot()
		elif attr is "leaves": return self.getLeaves()
		elif attr is "tree_name": return self.getName()
		elif attr is "tree_struct": return self.getStruct()
		elif attr is "tree_nodes": return self.getNodes()
		elif attr is "tree_leaves": return self.getLeaves()
		else: raise AttributeError(f"Attribute \"{attr}\" not found for Root instance")

	def clsInstances(cls):
		return Root._instances_

	def getName(self):
		return self._name_
	def getPath(self):
		return self.name
	def getIndexes(self):
		return []
	def getHeight(self):
		return 0
	def getRoot(self):
		return self
	def getNodes(self):
		return self.getProgeny()

	def totalNodes(self):
		return self.totalTreeNodes()

	def setName(self, name):
		self._name_ = f"<{name}>"
	def setParent(self, node=None):
		if node is not None: raise ValueError("Root instances cannot have a parent, it must be None")
		pass

	def displayRoot(self):
		print(self)
	def displayParent(self):
		print("╳\n └───" + self.name)

	def isChild(self, parent=None):
		return False
	def isOrphanage(self):
		return isinstance(self, Orph)

	name = property(getName, setName)


class Orph(Root):
	_instances_ = -1
	def __init__(self, name=None, *children):
		Root.__init__(self, name=None, *children)
		self._name_ = f"<{name}>"  if name is not None else f"<orph{Orph._instances_}>"
		Orph._instances_ += 1
	def __getattr__(self, attr):
		try: return Root.__getattr__(self, attr)
		except AttributeError:
			raise AttributeError(f"Attribute \"{attr}\" not found for Orph instance")

	def clsInstances(cls):
		return Orph._instances_


orph = Orph("orph")
