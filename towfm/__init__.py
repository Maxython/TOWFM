from typing import Union
from PIL import Image, ImageFilter, ImageDraw
from json import loads, dumps
import logging


__version__ = '0.1.1'


#Text for the logging module
#You can change the format of the information
text_info_for_logging = '[%(levelname)s | %(asctime)s | %(message)s]'

#Tree knowledge list.
#You can add a value to this list.
list_knowledge = []


class _TextError:
	"""The kind and text of errors that can return.
	"""

	def _ValueError0(value:Union[str, int]) -> str:
		return f'there is no "{value}" meaning in the tree.'


	def _ValueError1(value:Union[str, int]) -> str:
		return f'the value "{value}" contains a prohibited character. Check if there are any ";" and ":".'


	def _BufferError0(value:Union[str, int]) -> str:
		return f'in node "{value}" there is an extension of the tree or is positive.'


	def _BufferError1(value:Union[str, int]) -> str:
		return f'in node "{value}" you cannot change the seed or index, because it has an extension of the tree.'


	def _BufferError2(value:Union[str, int]) -> str:
		return f'no access to delete positive node "{value}".'


	def _BufferError3() -> str:
		return 'you cannot delete the root seed of the tree.'


	def _BufferError4(value:Union[str, int]) -> str:
		return f'seed "{value}" is already in the binary tree.'


	def _BufferError5(value:Union[str, int]) -> str:
		return f'you cannot change the logic at node "{value}".'


class Subtraction:


	def logic_listIDT(self, nodesIDT:dict) -> list:
		return [i.split('.')[-1] if '.' in i else None for i in list(nodesIDT.keys())]


	def nodes_without_logicIDT(self, nodesIDT:dict) -> dict:
		a = {}
		for i in nodesIDT:
			a[i.split('.')[0]] = nodesIDT[i]
		return a


	def type_translation_coordNDT(self, coordNDT:str, separators:str='/') -> Union[str, int]:
		coordNDT = str(coordNDT).split(separators)
		try:
			return int(coordNDT[0]) if coordNDT[-1] == 'int' else coordNDT[0]
		except ValueError:
			return coordNDT[0]


	def list_coord_from_coordNDT(self, coordNDT:str, separators:str='/') -> list:
		coordNDT = coordNDT.split(separators*2)
		for i in range(len(coordNDT)):
			coordNDT[i] = self.type_translation_coordNDT(coordNDT[i], separators)
		return coordNDT


class ParserTreeIDT(Subtraction):


	def __init__(self, treeIDT:dict) -> None:
		self.__tree = treeIDT
		self.__s = Subtraction


	def nodes_from_logic(self, logic:Union[bool, int, str, None]) -> dict:
		if isinstance(logic, bool):
			logic = str(int(logic))
		elif isinstance(logic, str) or logic == None:
			pass
		elif isinstance(logic, int):
			logic = str(logic)
		if logic != '0' and logic != '1' and logic != None:
			return None
		list = {}
		for i in self.__tree:
			if logic != None and f'.{logic}' in i:
				list[i] = self.__tree[i]
			elif logic == None and not('.' in i):
				list[i] = self.__tree[i]
		return list if len(list) != 0 else None


	def index(self, seed:Union[str, int], nodes:Union[dict, None]=None) -> Union[list, None]:
		a, b = self.__tree if nodes == None else nodes, []
		for i in a:
			if ((isinstance(a[i], str) or isinstance(a[i], int)) and a[i] == seed) or (isinstance(a[i], list) and seed in a[i]):
				b.append(i)
		return b if len(b) != 0 else None


	def max_index_by_level(self, level:int) -> Union[str, None]:
		c = 0
		for i in self.__tree:
			b = i.split(';')[0].split('.')[0].split(':')
			if len(b) == level:
				if c <= int(b[level-1]):
					c, h = int(b[level-1]), ':'.join(b)
		try:
			return h
		except UnboundLocalError:
			return None


	def max_index_by_index(self, index:str) -> Union[str, None]:
		a, b = 0, None
		try:
			for i in self.nodes_by_index(index):
				c = int(i.split(';')[0].split('.')[0].split(':')[-1])
				if a <= c:
					a, b = c, i
		except TypeError:
			pass
		return b


	def seed(self, index:Union[str, int]) -> Union[str, None]:
		try:
			index = str(index)
			if not('.' in index and ';' in index):
				index = index.split(';')[0].split('.')[0]
				a, b = self.logic_from_index(index), self.linked_seed_by_index(index)
				index = f'{index}{"."+str(int(a)) if a != None else ""}{";"+b if b != None else ""}'
			c = self.__tree[index]
			return c[1] if isinstance(c, list) else c
		except (KeyError, TypeError):
			return None


	def nodes_by_level(self, level:Union[int, str], sort:bool=False, binary_sort:bool=False, index_only:bool=False, nodes:Union[dict, None]=None) -> dict:
		a = {}
		for i in self.__tree:
			b = i.split(';')[0].split('.')[0]
			if len(b.split(':')) == int(level):
				a[b if index_only else i] = self.__tree[i]
		return ((self.sorting_node(a, tree_nodes=nodes) if sort else a) if not binary_sort else self.sort_by_seed_min_or_max(a, tree_nodes=nodes)) if len(a) != 0 else None


	def nodes_by_index(self, index:Union[str, int], sort:bool=False, binary_sort:bool=False, index_only:bool=False, nodes:Union[dict, None]=None) -> Union[dict, None]:
		a, index = {}, str(index).split(';')[0].split('.')[0].split(':'),
		for i in self.__tree:
			b = i.split(':')
			if len(b) == len(index)+1 and ':'.join(index)+':' in i:
				del b[-1]
				if len(''.join(b)) == len(''.join(index)):
					a[i.split(';')[0].split('.')[0] if index_only else i] = self.__tree[i]
		return ((self.sorting_node(a, tree_nodes=nodes) if sort else a) if not binary_sort else self.sort_by_seed_min_or_max(a, tree_nodes=nodes)) if len(a) != 0 else None


	def node_by_index(self, index:Union[str, int], index_only:bool=False) -> Union[dict, None]:
		a, b = self.logic_from_index(index), self.linked_seed_by_index(index)
		c = f'{index.split(";")[0].split(".")[0]}{"."+str(int(a)) if a != None else ""}{";"+b if b != None else ""}'
		return {c.split(';')[0].split('.')[0] if index_only else c:self.__tree[c]} if c in self.__tree else None


	def logic_from_index(self, index:Union[str, int]) -> Union[bool, None]:
		a = str(index).split(';')[0].split('.')[0]
		b = self.nodes_by_level(len(a.split(':')))
		if b != None:
			for i in b:
				c = i.split(';')[0].split('.')
				if a == c[0]:
					return bool(int(c[-1])) if len(c) == 2 else None


	def logic_from_seed(self, seed:Union[str, int]) -> Union[dict, None]:
		a, b = {}, self.index(seed)
		if b != None:
			for i in self.index(seed):
				a[i] = self.logic_from_index(i)
			return a
		return None


	def linked_seed_by_index(self, index:Union[str, int]) -> Union[str, None]:
		index = str(index)
		index2 = index.split(';')[0].split('.')[0].split(':')
		a = self.nodes_by_level(len(index2))
		if a != None:
			for i in a:
				if index in i and ';' in i:
					return i.split(';')[-1]


	def tree_extension(self, seed_or_index:Union[str, int]) -> Union[bool, None]:
		if self.type(seed_or_index) == 'seed':
			a = self.index(seed_or_index)
			if a == None:
				return None
			seed_or_index = a[0]
		else:
			seed_or_index = str(seed_or_index).split(';')[0].split('.')[0]
			a, b = self.logic_from_index(seed_or_index), self.linked_seed_by_index(seed_or_index)
			seed_or_index = f'{seed_or_index}{"."+str(int(a)) if a != None else ""}{";"+b if b != None else ""}'
			if not(seed_or_index in self.__tree):
				return None
		a = self.nodes_by_index(seed_or_index)
		if a == None:
			return False
		elif len(a) != 0:
			return True


	def tree_continuation_by_index(self, index:Union[str, int]) -> Union[dict, None]:
		index = str(index).split(';')[0].split('.')[0]
		b, h = self.logic_from_index(index), self.linked_seed_by_index(index)
		c = f'{index}{"."+str(int(b)) if b != None else ""}{";"+h if h != None else ""}'
		if c in self.__tree:
			b, a = [], {c:self.__tree[c]}
			while True:
				for i in list(a):
					if not(i in b):
						c = self.nodes_by_index(i)
						b.append(i)
						if c != None:
							for j in c:
								a[j] = c[j]
				if len(a) == len(b):
					break
			return a
		return None


	def tree_NDT(self, js:bool=True) -> dict:
		a, d = '{', list(self.root_nodes())
		for i in range(len(d)):
			b, h, g = self.logic_from_index(d[i]), 0, []
			a += '"%s": %s' % (str(self.__tree[f'{i}{"."+str(int(b)) if b != None else ""}'])+' '+str(i), '{' if self.tree_extension(d[i]) else 'null')
			b = list(self.nodes_by_index(d[i]))
			while len(g) != len(self.tree_continuation_by_index(d[i]))-1:
				if b[h] not in g:
					c = self.tree_extension(b[h])
					a += f'"{self.__tree[b[h]]}": {"null" if not c else "{"}{", " if not c and max(b) != b[h] else ""}'
					g.append(b[h])
					if c == True:
						b, h = list(self.nodes_by_index(b[h])), 0
						continue
				if len(b)-1 <= h:
					c = self.root_index_by_index(b[h])
					b = self.nodes_from_index(c)
					b = list(self.nodes_by_index(c)) if b == None else list(b)
					if len(g) != len(self.tree_continuation_by_index(d[i]))-1 or len(d)-1 != i:
						a += '}%s' % ('' if str(c) == max(b) else ', ')
					h = 0
				else:
					h += 1
		a += '}' * (a.count('{')-a.count('}'))
		return loads(a) if js == True else a


	def tree_NLT(self) -> list:
		a = []
		for h in list(self.root_nodes()):
			a.append(self.seed(h))
			if a[0] != None:
				b = [h]
				while len(b) != len(self.tree_continuation_by_index(h)):
					for i in b:
						c = self.nodes_by_index(i)
						a.append(list(c.values()) if c != None else c)
						if c != None:
							for j in c:
								b.append(j)
		return a


	def index_certain_type(self, seed_or_index:Union[str, int], type:str=None, root_seed_index:Union[int, None]=None) -> Union[list, None]:
		while True:
			if type == 'seed':
				a = self.index(seed_or_index)
				if root_seed_index == None or a == None:
					return a
				else:
					for i in range(len(a)-1):
						if int(a[0].split(';')[0].split('.')[0].split(':')[0]) != root_seed_index:
							del a[0]
					return a if len(a) != 0 else None
			elif type == 'index':
				seed_or_index = str(seed_or_index).split(';')[0].split('.')[0]
				a, h = self.logic_from_index(seed_or_index), self.linked_seed_by_index(seed_or_index)
				b = f'{seed_or_index}{"."+str(int(a)) if a != None else ""}{";"+h if h != None else ""}'
				if b in self.__tree:
					return [b] if root_seed_index == None else [b] if int(b.split('.')[0].split(':')[0]) == root_seed_index else None
			else:
				type = self.type(seed_or_index)
				continue
			return None


	def type(self, value:Union[str, int]) -> str:
		try:
			int(f'{value}'.split(';')[0].split('.')[0].replace(':', ''))
			if self.seed(value) != None:
				return 'index'
			else:
				return 'seed'
		except ValueError:
			return 'seed'


	def max_level(self) -> int:
		a = 0
		for i in self.__tree:
			b = i.split(';')[0].split('.')[0].split(':')
			a = len(b) if len(b) > a else a
		return a


	def max_index(self) -> str:
		c = 0
		for i in self.__tree:
			b = i.split(';')[0].split('.')[0].split(':')
			if c <= int(b[-1]):
				c, h = int(b[-1]), ':'.join(b)
		return h


	def max_node(self) -> Union[dict, None]:
		return self.node_by_index(self.max_index())


	def root_nodes(self) -> dict:
		return self.nodes_by_level(1)


	def root_index_by_index(self, index:Union[str, int], nodes:Union[dict, None]=None) -> Union[str, None]:
		index = str(index)
		index2 = self.nodes_from_index(index)
		if index2 != None:
			for i in list(index2.keys()):
				if ';' in i and len(i.split(':')) > 1:
					index2 = i.split(';')[-1]
					for h in range(2):
						try:
							for j in self.index(index2 if h == 0 else int(index2), nodes=nodes):
								if '.0' not in j and index.split(';')[0].split('.')[0].split(':')[0] == j.split(';')[0].split('.')[0].split(':')[0]:
									return j
						except (ValueError, TypeError):
							pass


	def nodes_from_index(self, index:Union[str, int], index_only:bool=False) -> Union[dict, None]:
		index = str(index).split('.')[0].split(':')
		del index[-1]
		return self.nodes_by_index(':'.join(index), index_only=index_only)


	def sorting_node(self, nodes:dict, tree_nodes:Union[dict, None]=None) -> dict:
		ind_t = min(list(nodes.keys()))
		index, b, c, i = self.root_index_by_index(ind_t, nodes=tree_nodes).split(';')[0].split('.')[0], 0, {}, 0
		d, ind_t = self.nodes_from_index(ind_t, index_only=True), ind_t.split(';')[0].split('.')[0].split(':')
		del ind_t[-1]
		while len(c) != len(nodes):
			a = ':'.join(ind_t)+':'+str(b)
			if a in d:
				b2, b3 = self.logic_from_index(a), self.linked_seed_by_index(a)
				c[index+f':{i}{"."+str(int(b2)) if b2 != None else ""}{";"+b3 if b3 != None else ""}'] = d[a]
				i += 1
			b += 1
		return c


	def sort_by_seed_min_or_max(self, nodes:dict, max_or_min:str='min', tree_nodes:Union[dict, None]=None) -> dict:
		a, b, c = {}, 0, list(nodes.keys())
		index, c2 = self.root_index_by_index(min(c), nodes=tree_nodes).split(';')[0].split('.')[0], [[id(i)+(0 if i == False else 1000000) if isinstance(i, bool) else i if isinstance(i, int) else id(i), i] for i in list(nodes.values())]
		while len(c2) != 0:
			d = min(c2) if max_or_min == 'min' else max(c2)
			b1, ind = self.logic_from_index(c[c2.index(d)]), f'{index}:{b}'
			a[f'{ind}{"."+str(int(b1)) if b1 != None else ""}{";"+self.linked_seed_by_index(min(c)) if b == 0 else ""}'] = d[1]
			del c2[c2.index(d)]
			b += 1
		return a


class ParserTreeNDT(Subtraction):


	def __init__(self, treeNDT:dict) -> None:
		self.__tree = treeNDT
		self.__s = Subtraction


	def nodes(self, coord:Union[int, str], separators:str='/') -> Union[list, None]:
		a = self.__tree
		for i in coord.split(separators*2):
			try:
				a = a[i]
			except KeyError:
				return None
		return list(a.keys()) if a != None else 'no continue'


	def coord_from_indexIDT(self, indexIDT:Union[str, int], separators:str='/') -> Union[str, None]:
		a, b = self.__tree, []
		try:
			for i in indexIDT.split('.')[0].split(':'):
				c = list(a.keys())[int(i)]
				a = a[c]
				b.append(c)
			return (separators*2).join(b) if len(b) != 0 else None
		except (IndexError, ValueError):
			return None


	def root_node(self) -> str:
		a = list(self.__tree.keys())
		return a[0] if len(a) != 0 else None


class ParserTreeNLT(Subtraction):


	def __init__(self, treeNLT:list) -> None:
			self.__tree = treeNLT
			self.__s = Subtraction


	def index(self, node:Union[str, int]) -> Union[list, None]:
		a, b = [], self.__tree
		for i in range(len(b)):
			if b[i] != None:
				for j in range(len(b[i])):
					if b[i][j] == node:
						if i != 0:
							a.append(f'{i}:{j}')
						else:
							a.append(str(i))
		return a if len(a) != 0 else None


	def node(self, index:Union[str, int]) -> Union[str, int, None]:
		a = self.__tree
		for i in str(index).split(':'):
			try:
				a = a[int(i)]
			except (IndexError, ValueError, TypeError):
				return None
		return a


	def index_by_index(self, index:Union[str, int]) -> Union[str, None]:
		try:
			index, a, c = [int(i) for i in str(index).split(':')], 0, 0
			for i in range(index[0]):
				if i != 0:
					try:
						b = len(self.__tree[i])
						a += b
						if b/2 != b//2:
							a -= c
						c += 2
					except TypeError:
						a -= 1
			return sum(index)+(1 if a == 0 else a)
		except (IndexError, ValueError):
			return None


	def nodes_by_index(self, index:Union[str, int]) -> Union[list, None]:
		return self.node(self.index_by_index(index))


	def positive_nodes(self, internal_lists:bool=True) -> list:
		a = []
		for i in self.__tree:
			if i != None:
				if self.root_node == i or internal_lists == True:
					a.append(i)
				elif isinstance(i, list):
					for j in i:
						a.append(j)
		return a


	def index_from_indexIDT(self, indexIDT:Union[str, int]) -> Union[str, None]:
		try:
			indexIDT = [int(x) for x in str(indexIDT).split('.')[0].split(':')]
			if indexIDT[0] > 0:
				for i in range(indexIDT[0]):
					indexIDT[0] += len(self.dividing_tree_by_root_node()[i])-(1 if i != 0 else 0)
			else:
				indexIDT[0] += 1
			if len(indexIDT) > 1:
				a, b = 1, 1
				while len(indexIDT) != 2:
					indexIDT[0] = indexIDT[0] * a
					indexIDT[1] += 1 if a == 1 else b+1 if indexIDT[0] / 2 == indexIDT[0] // 2 else b
					indexIDT[0] += indexIDT[1]
					del indexIDT[1]
					a += 1
					b += 2
			return ':'.join([str(x) for x in indexIDT])
		except ValueError:
			return None


	def nodes_by_indexIDT(self, indexIDT:Union[str, int]) -> Union[str, int, None]:
		return self.node(self.index_from_indexIDT(indexIDT))


	def index_from_coordNDT(self, coordNDT:str, separators:str='/') -> Union[str, None]:
		try:
			coordNDT = coordNDT.split(separators*2)
			a = self.index_by_index(self.index(self.type_translation_coordNDT(coordNDT[0]))[0])
			for i in range(len(coordNDT)):
				if i != 0:
					b = f'{a}:{self.__tree[a].index(self.type_translation_coordNDT(coordNDT[i]))}'
					a = self.index_by_index(b) if i != len(coordNDT)-1 else b
			return a
		except (TypeError, ValueError):
			return None


	def nodes_by_coordNDT(self, coordNDT:str, separators:str='/') -> Union[str, None]:
		a = self.index_from_coordNDT(coordNDT, separators)
		return self.node(a.split(':')[0]) if a != None else None


	def tree_extension(self, node_or_index:Union[str, int]) -> Union[bool, None]:
		if self.type(node_or_index) == 'node':
			b = self.index(node_or_index)
			if b == None:
				return None
			node_or_index = b[0]
		else:
			b = str(node_or_index).split(':')
			if len(b) > 2 or len(b) == 0:
				return None
			elif len(b) == 1:
				b.append('0')
			node_or_index = ':'.join(b)
		b = self.nodes_by_index(node_or_index)
		return False if b == None else True if len(b) != 0 else None


	def dividing_tree_by_root_node(self) -> list:
		a = []
		b = -1
		for i in self.__tree:
			if isinstance(i, str):
				a.append([i])
				b += 1
			else:
				a[b].append(i)
		return a


	def type(self, value:Union[str, int]) -> str:
		try:
			b = [int(i) for i in str(value).split(':')]
			if len(b) <= 2 and self.node(value) != None:
				a = self.__tree
				for i in b:
					a = a[i]
				return 'index'
			return 'node'
		except (ValueError, IndexError):
			return 'node'


	def root_nodes(self) -> list:
		a = []
		for i in self.__tree:
			if isinstance(i, str):
				a.append(i)
		return a if len(a) != 0 else None


class CreateTree(ParserTreeIDT):


	def __init__(self, root_seed:Union[str, int, None]=None, list_seed_or_seed:Union[list, str, int, None]=None, specific_type:Union[str, None]=None, type_knowledge_creation:str='list_knowledge', sort:bool=True, binary_sort:bool=False, removing_logic:bool=True, error:bool=True, node_quantity:Union[int, None]=None, rsp:bool=True, delete_duplicates:bool=False, duplicate_root_node:bool=True) -> None:
		self.__tree = {}
		self.__root_seed_list = []
		self.__root_seed_index = 0
		self.__knowledge_list = []
		self.__general_knowledge = list_knowledge.copy()
		self.__new_knowledge = []
		self.__history_of_knowledge_list = []
		self.__index_print = '0'
		self.__specific_type = specific_type
		self.__type_knowledge_creation = type_knowledge_creation
		self.__sort = sort
		self.__binary_sort = binary_sort
		self.__removing_logic = removing_logic
		self.__node_quantity = node_quantity
		self.__rsp = rsp
		self.__run_rsp_in_delete = True
		self.__error = error
		self.__delete_duplicates = delete_duplicates
		self.__duplicate_root_node = duplicate_root_node
		self.__list_seed = []
		self.__te = _TextError
		self.__pt = ParserTreeIDT
		self.update_pt()
		if not error:
			self.__log = logging
			self.__log.basicConfig(format=text_info_for_logging)
		if root_seed != None:
			self.add_root_node(root_seed, list_seed_or_seed)


	def __str__(self) -> str:
		text = '\n'
		try:
			c = self.logic_from_index(self.__index_print)
			a, h = {f'{self.__index_print}{"."+str(int(c)) if c != None else ""}':f'{self.seed(self.__index_print)}'}, self.nodes_by_index(self.__index_print)
			if h != None:
				for i in h:
					a[i] = f'{h[i]}'
				b = 0
				for i in a:
					text = text + a[i]
					text += '\n|\n' if b == 0 else '\n' if b == len(a)-1 else '--'
					b += 1
				b = 0
				for k in range(2):
					for i in a:
						if b != 0:
							text = text + ('|' if k == 0 else 'o' if (i.split(';')[0].split('.')[1] if '.' in i else '1') == '1' else 'x')
							for j in range(len(a[i])-1):
								text = text + ' '
							text = text + ('  ' if len(a)-1 != b else '\n' if k == 0 else '\n\n')
						b += 1
					b = 0
			else:
				text = text + self.seed(self.__index_print) + '\n|\n' + ('o' if str(int(c)) == '1' else 'x') + '\n\n'
		except TypeError:
			pass
		text = text + f'root seed: {self.__root_seed_list[self.__root_seed_index]}\nmax level: {self.max_level()}\nmax index: {self.max_index()}\namount of knowledge: {len(self.__knowledge)}\nword count: {len(self.__tree)}\n'
		return text


	def add(self, seed_or_index:Union[str, int], list_seed_or_seed:Union[list, str, int, None]=None, type:str=None) -> None:
		coord2 = self.index_certain_type(seed_or_index, type if type != None else self.__specific_type, self.__root_seed_index)
		if coord2 == None:
			if self.__error:
				raise ValueError(self.__te._ValueError0(seed_or_index))
			self.__log.error(f'ValueError: {self.__te._ValueError0(seed_or_index)}')
			return
		a = len(coord2)
		for j in range(a):
			b = self.nodes_by_index(coord2[j])
			if self.logic_from_index(coord2[j]) != False and ((len(b) < self.__node_quantity) if self.__node_quantity != None and b != None else True):
				self.__new_knowledge.clear()
				coord, coord2 = coord2[j].split(';')[0].split('.')[0], coord2[j]
				list_seed_or_seed = self.__list_seed if list_seed_or_seed == None and len(self.__list_seed) != 0 else list_seed_or_seed
				if not isinstance(list_seed_or_seed, list) and list_seed_or_seed != None:
					list_seed_or_seed = [list_seed_or_seed]
				elif list_seed_or_seed != None and len(list_seed_or_seed) == 0:
					list_seed_or_seed = None
				if list_seed_or_seed != None:
					for i in range(len(list_seed_or_seed)):
						seed = list_seed_or_seed[i]
						if not(';' in str(seed) or ':' in str(seed)):
							h = (len(b) if b != None else 0)+i
							c = f'{coord}:{h}.{0 if list_seed_or_seed[i] in self.__knowledge else 1}'
							self.__tree[f'{c};{self.seed(coord)}' if h == 0 else c] = list_seed_or_seed[i]
							self.__value_knowledge = list_seed_or_seed[i]
							self.update_knowledge(False)
							if i+1 == self.__node_quantity:
								break
						else:
							if i == len(list_seed_or_seed)-1:
								raise ValueError(self.__te._ValueError1(seed))
							self.__log.error(f'ValueError: {self.__te._VallueError1(seed)}')
					if len(self.__new_knowledge) != 0:
						self.__history_of_knowledge.append(self.__new_knowledge.copy())
				else:
					c = self.linked_seed_by_index(coord)
					self.__tree[f'{coord}.0{";"+c if c != None else ""}'] = self.__tree.pop(coord2)
				self.rsp()
				break
			else:
				if j == a-1:
					if self.__error:
						raise BufferError(self.__te._BufferError0(seed_or_index))
					self.__log.error(f'BufferError: {self.__te._BufferError0(seed_or_index)}')


	def add_root_node(self, seed:Union[str, int], list_seed:Union[list, str, int, None]=None, type_knowledge_creation:Union[str, None]=None, automatic_movement:bool=True) -> None:
		if ';' in str(seed) or ':' in str(seed):
			if self.__error:
				raise ValueError(self.__te._ValueError1(seed))
			self.__log.error(f'ValueError: {self.__te._ValueError1(seed)}')
			return
		type_knowledge_creation = self.__type_knowledge_creation if type_knowledge_creation == None else type_knowledge_creation
		self.__knowledge_list.append(list_knowledge.copy() if type_knowledge_creation == 'list_knowledge' else self.__knowledge.copy() if type_knowledge_creation == 'root_list_knowledge' else []) #list_knowledge root_list_knowledge new_list_knowledge
		a = len(self.__root_seed_list)
		if seed in (self.__knowledge_list[a] if self.__duplicate_root_node else self.__root_seed_list):
			self.__tree[f'{a}.0'] = seed
		else:
			self.__tree[f'{a}.1'] = seed
			self.__knowledge_list[a].append(seed)
		if seed not in self.__general_knowledge:
			self.__general_knowledge.append(seed)
		self.__root_seed_list.append(seed)
		self.__history_of_knowledge_list.append([])
		if automatic_movement:
			self.__root_seed_index = a
		self.update_knowledge_list()
		if list_seed != None:
			self.add(seed, list_seed, type='seed')


	def change_logic(self, seed_or_index:Union[str, int], logic:bool, type:Union[str, None]=None) -> None:
		coord2 = self.index_certain_type(seed_or_index, type if type != None else self.__specific_type, self.__root_seed_index)
		if coord2 == None:
			if self.__error:
				raise ValueError(self.__te._ValueError0(seed_or_index))
			self.__log.error(f'ValueError: {self.__te._ValueError0(seed_or_index)}')
			return
		a = len(coord2)
		for i in range(a):
			if not self.tree_extension(coord2[i]):
				coord, coord2, c = coord2[i].split('.')[0], coord2[i], self.linked_seed_by_index(coord2[i])
				if logic and self.__tree[coord2] not in list(self.nodes_from_logic(1).values()):
					self.__tree[f'{coord}.1{";"+c if c != None else ""}'] = self.__tree.pop(coord2)
				elif not logic:
					self.__tree[f'{coord}.0{";"+c if c != None else ""}'] = self.__tree.pop(coord2)
				else:
					if self.__error:
						raise BufferError(self.__te._BufferError5(seed_or_index))
					self.__log.error(f'BufferError: {self.__te._BufferError5(seed_or_index)}')
					return
				self.rsp()
				break
			else:
				if i == a-1:
					if self.__error:
						raise BufferError(self.__te._BufferError1(seed_or_index))
					self.__log.error(f'BufferError: {self.__te._BufferError1(seed_or_index)}')


	def replacement(self, seed_or_index:Union[str, int], new_seed:Union[str, None]=None, type:Union[str, None]=None) -> None:
		coord2 = self.index_certain_type(seed_or_index, type if type != None else self.__specific_type, self.__root_seed_index)
		if coord2 == None:
			if self.__error:
				raise ValueError(self.__te._ValueError0(seed_or_index))
			self.__log.error(f'ValueError: {self.__te._ValueError0(seed_or_index)}')
			return
		if ';' in str(new_seed) or ':' in str(new_seed):
			if self.__error:
				raise ValueError(self.__te._ValueError1(new_seed))
			self.__log.error(f'ValueError: {self.__te._ValueError1(new_seed)}')
			return
		a = len(coord2)
		for j in range(a):
			if self.tree_extension(coord2[j]) == False:
				self.__new_knowledge.clear()
				coord, coord2 = coord2[j].split(';')[0].split('.')[0], coord2[j]
				c = self.linked_seed_by_index(coord2)
				self.__tree[f'{coord}{".1" if self.index(new_seed) == None else ".0"}{";"+c if c != None else ""}'] = self.__tree.pop(coord2)[0] if new_seed == None else [self.__tree.pop(coord2), new_seed] if isinstance(self.__tree[coord2], list) == False else [self.__tree.pop(coord2)[0], new_seed]
				self.__value_knowledge = new_seed
				self.update_knowledge()
				self.rsp()
				break
			else:
				if j == a-1:
					if self.__error:
						raise BufferError(self.__te._BufferError1(seed_or_index))
					self.__log.error(f'BufferError: {self.__te._BufferError1(seed_or_index)}')


	def delete(self, seed_or_index:str, type:Union[str, None]=None, positive_seeds:bool=False) -> None:
		coord = self.index_certain_type(seed_or_index, type if type != None else self.__specific_type, self.__root_seed_index)
		if coord == None:
			if self.__error:
				raise ValueError(self.__te._ValueError0(seed_or_index))
			self.__log.error(f'ValueError: {self.__te._ValueError0(seed_or_index)}')
			return
		a = len(coord)
		for i in range(a):
			if positive_seeds == False:
				if self.tree_extension(coord[i]) == True or self.logic_from_index(coord[i]) != False:
					if a-1 == i:
						if self.__error:
							raise BufferError(self.__te._BufferError2(coord[i]))
						self.__log.error(f'BufferError: {self.__te._BufferError2(coord[i])}')
						return
					continue
			c = self.logic_from_index(coord[i])
			if coord[i] not in self.nodes_by_level(1):
				for j in self.tree_continuation_by_index(coord[i]):
					h = self.linked_seed_by_index(j)
					if h != None:
						try:
							b = self.nodes_from_index(j)
						except TypeError:
							b = self.nodes_from_index(self.root_index_by_index(j))
						b = list(b)
						if len(b) > 1:
							i2 = b.index(j)
							i2 = i2+1 if i2 != len(b)-1 else 0
							self.__tree[b[i2]+f';{h}'] = self.__tree.pop(b[i2])
					del self.__tree[j]
				if self.__run_rsp_in_delete:
					self.rsp()
				else:
					self.update_pt()
					self.__run_rsp_in_delete = True
				break
			else:
				if a-1 == i:
					if self.__error:
						raise BufferError(self.__te._BufferError3())
					self.__log.error(f'BufferError: {self.__te._BufferError3()}')


	def delete_duplicates(self) -> None:
		a = self.nodes_from_logic(0)
		if a != None:
			for i in a:
				self.__run_rsp_in_delete = False
				self.delete(i, 'index')


	def sort(self) -> None:
		a, k = {}, 0
		for d in range(len(self.__root_seed_list)):
			a[list(self.nodes_by_level(1))[d]] = self.__root_seed_list[d]
			b, c = self.nodes_by_index(d, True, self.__binary_sort, nodes=a), []
			if b != None:
				for i in b:
					a[i] = b[i]
					c.append(i.split('.')[0])
				k += len(self.tree_continuation_by_index(d))
				while len(a) != k:
					for i in c:
						b = self.nodes_by_index(i, True, self.__binary_sort, nodes=a)
						if b != None:
							for j in b:
								h = j.split('.')[0]
								if h not in c:
									a[j] = b[j]
									c.append(h)
		self.__tree = a


	def removing_logic(self) -> None:
		a = self.__tree.copy()
		for i in a:
			if self.tree_extension(i):
				self.__tree[i.split(';')[0].split('.')[0]+(';'+i.split(';')[-1] if ';' in i else '')] = self.__tree.pop(i)


	def index_print(self, index:Union[str, int]) -> None:
		self.__index_print = index


	def root_seed_index(self, index:Union[str, int]) -> None:
		index = int(index)
		a = len(self.__root_seed_list)-1
		index = a if index >= a else index if index >= 0 else 0
		self.__root_seed_index = int(index)
		self.update_knowledge_list()


	def specific_type(self, type:str) -> None:
		self.__specific_type = type


	def update_pt(self) -> None:
		self.__pt.__init__(self, self.__tree)


	def update_knowledge(self, save_history:bool=True) -> None:
		if self.__value_knowledge != None:
			if self.__value_knowledge not in self.__knowledge:
				self.__knowledge.append(self.__value_knowledge)
				self.__new_knowledge.append(self.__value_knowledge)
				if len(self.__new_knowledge) != 0 and save_history == True:
					self.__history_of_knowledge.append(self.__new_knowledge.copy())
			if self.__value_knowledge not in self.__general_knowledge:
				self.__general_knowledge.append(self.__value_knowledge)
			self.__value_knowledge = None


	def update_knowledge_list(self) -> None:
		self.__knowledge = self.__knowledge_list[self.__root_seed_index]
		self.__history_of_knowledge = self.__history_of_knowledge_list[self.__root_seed_index]


	def rsp(self, rsp:Union[None, bool]=None, sort:Union[None, bool]=None, removing_logic:Union[None, bool]=None, delete_duplicates:Union[None, bool]=None, save_setting:bool=True, run:bool=True) -> None:
		rspf = rsp if rsp != None else self.__rsp
		sortf = sort if sort != None else self.__sort
		removing_logicf = removing_logic if removing_logic != None else self.__removing_logic
		delete_duplicatesf = delete_duplicates if delete_duplicates != None else self.__delete_duplicates
		self.update_pt()
		if rspf and run:
			if delete_duplicatesf:
				self.delete_duplicates()
			if removing_logicf:
				self.removing_logic()
			if sortf:
				self.sort()
			self.update_pt()
		if save_setting:
			self.__rsp = rspf
			self.__sort = sortf
			self.__removing_logic = removing_logicf
			self.__delete_duplicates = delete_duplicatesf


	def list_seed(self, value:Union[str, int, None]=None) -> Union[None, list]:
		if value == None:
			return self.__list_seed.copy()
		self.__list_seed.append(value)


	def pt(self, information:bool=False) -> Union[None, str]:
		for i in self.__root_seed_list:
			h = self.index(i)[0]
			a, b, c, d = 0, list(self.nodes_by_index(h)), 0, []
			print(str(i))
			while len(self.tree_continuation_by_index(h))-1 != len(d):
				try:
					if b[c] not in d:
						f = self.__tree[b[c]]
						print('| '+' | '*a, f[-1] if isinstance(f, list) else f, (b[c], self.linked_seed_by_index(b[c]), self.logic_from_index(b[c])) if information else '', end='')
						d.append(b[c])
						if self.logic_from_index(b[c]) == None:
							print()
							a += 1
							c, b = 0, list(self.nodes_by_index(b[c]))
							continue
						else:
							print()
					c += 1
				except IndexError:
					a -= 1
					c, b = 0, list(self.nodes_from_index(self.root_index_by_index(b[0])))


	@property
	def tree(self) -> dict:
		return self.__tree.copy()


	@property
	def knowledge(self) -> list:
		return self.__knowledge.copy()


	@property
	def knowledge_list(self) -> list:
		return self.__knowledge_list.copy()


	@property
	def general_knowledge(self) -> list:
		return self.__general_knowledge.copy()


	@property
	def new_knowledge(self) -> list:
		return self.__new_knowledge.copy()


	@property
	def history_of_knowledge(self) -> list:
		return self.__history_of_knowledge.copy()


	@property
	def history_of_knowledge_list(self) -> list:
		return self.__history_of_knowledge_list.copy()


	@property
	def root_seed(self) -> str:
		return f'{self.__root_seed_list[self.__root_seed_index]}'

	@property
	def root_seed_list(self) -> list:
		return self.__root_seed_list.copy()


	def _tree(self) -> dict:
		return self.__tree.copy()


	def _general_knowledge(self) -> list:
		return self.__general_knowledge.copy()


	def _root_seed_list(self) -> list:
		return self.__root_seed_list.copy()


class BinaryTree(CreateTree):


	def __init__(self, root_seed:Union[str, int, list]=None, seed:Union[str, int, list, None]=None) -> None:
		self.__bt = CreateTree
		self.__bt.__init__(self, root_seed, node_quantity=2)
		self.__te = _TextError
		self.form_empty_nodes()
		if seed != None:
			self.append(seed)


	def append(self, seed:Union[str, int, list], seed_or_index:Union[str, int, None]=None, type:Union[str, None]=None) -> None:
		seed = seed if isinstance(seed, list) else [seed]
		c = len(seed)
		for j in range(c):
			if len(self._root_seed_list()) != 0:
				if seed[j] not in self._general_knowledge():
					if seed_or_index == None:
						seed_int, a = seed[j] if isinstance(seed[j], int) else id(seed[j]), 0
						while not isinstance(self.seed(a), bool):
							b = self.nodes_by_index(a)
							c, b1, b2 = self.seed(a), list(b), [i if isinstance(i, bool) else i[0] for i in list(b.values())]
							c = c[1] if isinstance(c, list) else c
							a = b1[b2.index(True)] if seed_int > (c if isinstance(c, int) else id(c)) else b1[b2.index(False)]
					self.replacement(a, seed[j], type=type if type != None else 'index')
				else:
					if c == 1:
						raise BufferError(self.__te._BufferError4(seed[0]))
			else:
				self.add_root_node(seed[j])
			self.form_empty_nodes()


	def form_empty_nodes(self) -> None:
		a = self._tree()
		for i in a:
			if not isinstance(a[i], bool) and not self.tree_extension(i):
				self.add(i, [False, True])


	def processed_logic_by_index(self, index:Union[str, int]) -> Union[bool, None]:
		b = self.nodes_by_index(index)
		if b != None:
			for i in list(b.values()):
				if not isinstance(i, bool):
					return None
			return True


	@property
	def processed_tree(self) -> dict:
		a, b = {}, self._tree()
		for i in b:
			g = self.nodes_from_index(i)
			c, h = self.processed_logic_by_index(i), self.linked_seed_by_index(min(g) if g != None else i)
			if isinstance(b[i], list):
				a[f'{i.split(";")[0].split(".")[0]}{"."+str(int(c)) if c != None else ""}{";"+h if h != None else ""}'] = b[i][1]
			elif isinstance(b[i], bool):
				pass
			else:
				a[f'{i.split(";")[0].split(".")[0]}{"."+str(int(c)) if c != None else ""}{";"+h if h != None else ""}'] = b[i]
		return a


#class TreeNLT(CreateTree, ParserTreeNLT):


	#def __init__(self, treeNLT, specific_type:Union[str, None]=None, type_knowledge_creation:str='list_knowledge', sort:bool=True, binary_sort:bool=False, removing_logic:bool=True, error:bool=True, node_quantity:Union[int, None]=None, rsp:bool=True, delete_duplicates:bool=False, duplicate_root_node:bool=True) -> None:
		#self.__pt = ParserTreeNLT
		#self.__pt.__init__(self, treeNLT)
		#self.__t = CreateTree
		#self.__t.__init__(self, specific_type=specific_type,
						  #type_knowledge_creation=type_knowledge_creation,
						  #sort=sort,
						  #binary_sort=binary_sort,
						  #removing_logic=removing_logic,
						  #error=error,
						  #node_quantity=node_quantity,
						  #rsp=rsp,
						  #delete_duplicates=delete_duplicates,
						  #duplicate_root_node=duplicate_root_node)
		#a = self.dividing_tree_by_root_node()
		#for i in range(len(a)):
			#self.add_root_node(a[i][0], a[i][1])
			#b = a[i][1]


#class TreeIDT(TreeNLT, ParserTreeIDT):


	#def __init__(self, treeIDT, specific_type:Union[str, None]=None, type_knowledge_creation:str='list_knowledge', sort:bool=True, binary_sort:bool=False, removing_logic:bool=True, error:bool=True, node_quantity:Union[int, None]=None, rsp:bool=True, delete_duplicates:bool=False, duplicate_root_node:bool=True) -> None:
		#pass


#class SaveImage(ParserTreeIDT):


	#def __init__(self, treeIDT:dict, name_image:str='tree_image', background:str='white', occupy_px:int=20, space_px:int=5) -> None:
		#tp = ParserTree
		#tp.__init__(self, tree)
		#a = sum([int(i) for i in tp.max_index(self).split('.')[0].split(':')])
		#img = Image.new('RGBA', ((a+1)*occupy_px+a*space_px, 100), background)
		#img.save(f'{name_image}.png')


	#def __str__(self) -> str:
		#pass


#class SaveFileJS():


	#pass
