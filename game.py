from tree import *

class Player:
	def __init__(self, name):
		self.name = name

	def play(self, node):
		node.cutBefore()


class Game:
	def __init__(self, root, p0, p1):
		self.root = root
		self.p0 = p0
		self.p1 = p1
