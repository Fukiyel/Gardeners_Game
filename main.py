from game import *

root = Root()

root.grow(3)
root[1].grow(2)
root[1][1].grow(3)
root[2].grow(1)

root.display()
