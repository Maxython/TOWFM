![Logo](https://raw.githubusercontent.com/Maxython/TOWFM/main/IMG_GIF/4995c55f-8b54-438f-bdc2-5bc179fc0e4a.png)

# TOWFM

## What is TOWFM?
TOWFM is a flexible and convenient Python module for creating various tree data structures.

## Installing TOWFM
The module supports the latest python version (3.9).
#### Command:
```
pip3 install TOWFM
```
  
## Test run
After installing the module, you can start generating the Binary Tree.
#### Command:
```Python
from towfm.BTT import run

run()
```
The result will be saved in the test_tree.js file.

## Create WikiTree
```Python
from towfm.WT import CreateWT

a = CreateWT('hello world')
a.handle()
```

## Create binary search tree
```Python
from towfm import BinaryTree

a = BinaryTree(5, [2, 6, 3]) #1 way

a = BinaryTree(5) #2 way
a.append([2, 6, 3])

a = BinaryTree() #3 way
a.append(5)
a.append(2)
a.append(6)
a.append(3)

a.processed_tree #Returns a tree without extra nodes
```

## Create your own tree
```Python
from towfm import CreateTree

a = CreateTree('a', list(range(10))) #1 way

a = CreateTree('a') #2 way
a.add(0, list(range(10)))

a = CreateTree() #3 way
a.add_root_node('a', list(range(10)))

a = CreateTree() #4 way
a.add_root_node('a')
a.add(0, list(range(10)))

a = CreateTree('a') #5 way
for i in range(10):
    a.add(0, i)
```

## Tree output

### First way:
Outputs the tree dictionary (main).
```Python
a = CreateTree('a', list(range(10)))
print(a.tree)
```

### Second way:
Output of the CreateTree class.
```Python
a = CreateTree('a', list(range(10)))
print(a)
```
This method displays only part of the tree and additional information.

### Third way:
Prints the tree in an understandable format.
```Python
a = CreateTree('a', list(range(10)))
a.pt()
```

## [Telegram Bot Test](https://github.com/Maxython/TOWFM/tree/main/bot)
