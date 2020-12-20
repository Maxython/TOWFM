import towfm

b = towfm.CreateTree('sd', [0,1], error=False)
b.add(0, list(range(12)))
b.add(1, list(range(2,14)))
b.add('0:0:2', list(range(10)), type='index')
print(b.tree)
c2 = b.tree_NLT()
c = towfm.ParserTreeNLT(c2)
print(c.nodes_by_index('0:1'))
#print(c.tree_continuation_by_index('1:0'))
