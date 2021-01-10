import wikipedia
import requests
from typing import Union
from PIL import Image, ImageFilter, ImageDraw
from json import loads, dumps
import logging


#Text for the logging module
#You can change the format of the information
text_info_for_logging = '[%(levelname)s | %(asctime)s | %(message)s]'

#A list with a value to be removed when searched in the Wiki class.
#You can add a value to this list.
delete_character_list = ['(', ')', '[', ']', '.', ',', '!', '?', ':', ';', '"', "'", '»', '«']

#Tree knowledge list.
#You can add a value to this list.
list_knowledge = []


class _TextError:
	"""The kind and text of errors that can return.
	"""

	def _ValueError0(value:Union[str, int]) -> str:
		return f'there is no "{value}" meaning in the tree.'


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


class Wiki:


	def __init__(self, seed:str=None, lang:str='en', quantity:int=None, replacement_seed:bool=False, lower:bool=True, remove_numbers:bool=False, deletion_with_a_certain_amount:int=0) -> None:
		self.__lang = lang
		self.__quantity = quantity
		self.__replacement = replacement_seed
		self.__lower = lower
		self.__remove_numbers = remove_numbers
		self.__deletion_with_a_certain_amount = deletion_with_a_certain_amount
		if seed != None:
			self.search(seed)


	def __str__(self) -> str:
		return ','.join(self.__list)


	def search(self, seed:str) -> None:
		b = []
		c = seed
		self.__replacement_seed = False
		self.__old_seed = None
		while True:
			try:
				wikipedia.set_lang(self.__lang)
				con, con2 = wikipedia.summary(seed).split(), []
				for i in range(len(con)):
					try:
						if self.__lower == True:
							con[i] = con[i].lower()
						for j in delete_character_list:
							con[i] = con[i].replace(j, '')
						if self.__remove_numbers == True:
							try:
								int(con[i])
								del con[i]
							except ValueError:
								pass
						if (con[i] == '' or len(con[i]) <= self.__deletion_with_a_certain_amount):
							del con[i]
						elif len(con2) == self.__quantity:
							break
						elif not(con[i] in con2):
							con2.append(con[i])
					except IndexError:
						break
				break
			except (wikipedia.exceptions.PageError, requests.exceptions.ConnectionError):
				con2 = None
				break
			except wikipedia.exceptions.DisambiguationError:
				if self.__replacement == True:
					a = wikipedia.search(c)
					if a != b:
						if self.__old_seed == None:
							self.__old_seed = seed
						self.__replacement_seed = True
						for i in a:
							if not(i in b):
								b.append(i)
								seed = i.lower()
								break
						continue
				con2 = None
				seed = c
				break
		self.__list = con2
		self.__seed = seed


	@property
	def list(self) -> list:
		if self.__list != None:
			return self.__list.copy()


	@property
	def seed(self) -> str:
		if self.__seed != None:
			return f'{self.__seed}'


	@property
	def replacement_seed(self) -> bool:
		return True if self.__replacement_seed == True else False


	@property
	def old_seed(self) -> Union[str, None]:
		if self.__old_seed != None:
			return f'{self.__old_seed}'


class Subtraction:


	def logic_listIDT(self, nodesIDT:dict) -> list:
		return [i.split('.')[-1] if '.' in i else None for i in list(nodesIDT.keys())]


	def nodes_without_logicIDT(self, nodesIDT:dict) -> dict:
		a = {}
		for i in nodesIDT:
			a[i.split('.')[0]] = nodesIDT[i]
		return a


	def sorting_nodeIDT(self, nodesIDT:dict) -> dict:
		index, b, c, i, d, f = list(nodesIDT.keys())[0].split('.')[0].split(':'), 0, {}, 0, self.nodes_without_logicIDT(nodesIDT), self.logic_listIDT(nodesIDT)
		del index[-1]
		index = ':'.join(index)
		d2 = list(d)
		while len(d) != 0:
			a = index+':'+str(b)
			if a in d:
				b2 = f[d2.index(a)]
				c[index+f':{i}{"."+b2 if b2 != None else ""}'] = d[a]
				del d[a]
				i += 1
			b += 1
		return c


	def sort_by_seed_min_or_maxIDT(self, nodesIDT:dict, max_or_min:str='min') -> dict:
		a, b, c = {}, 0, list(nodesIDT.keys())
		index = c[0].split('.')[0].split(':')
		del index[-1]
		index, list_log, c = ':'.join(index), self.logic_listIDT(nodesIDT), [[i if 'int' in str(type(i)) else id(i), i] for i in list(nodesIDT.values())]
		while len(c) != 0:
			d = min(c) if max_or_min == 'min' else max(c)
			h = c.index(d)
			i = list_log[h]
			a[f'{index}:{b}{"."+i if i != None else ""}'] = d[1]
			del c[h], list_log[h]
			b += 1
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


	def index(self, seed:Union[str, int]) -> Union[list, None]:
		a = self.__tree
		b = []
		for i in a:
			if ((isinstance(a[i], str) or isinstance(a[i], int)) and a[i] == seed) or (isinstance(a[i], list) and seed in a[i]):
				b.append(i)
		if len(b) != 0:
			return b
		else:
			return None


	def max_index_by_level(self, level:int) -> Union[str, None]:
		c = 0
		for i in self.__tree:
			b = i.split('.')[0].split(':')
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
				c = int(i.split('.')[0].split(':')[-1])
				if a <= c:
					a, b = c, i
		except TypeError:
			pass
		return b


	def seed(self, index:Union[str, int]) -> Union[str, None]:
		try:
			a = self.logic_from_index(index)
			return self.__tree[f'{index}{"."+str(int(a)) if a != None else ""}']
		except (KeyError, TypeError):
			try:
				return self.__tree[index]
			except KeyError:
				return None


	def nodes_by_level(self, level:Union[int, str], sort:bool=False, binary_sort:bool=False) -> dict:
		a = {}
		for i in self.__tree:
			if len(i.split('.')[0].split(':')) == int(level):
				a[i] = self.__tree[i]
		return ((self.sorting_nodeIDT(a) if sort else a) if not binary_sort else self.sort_by_seed_min_or_maxIDT(a)) if len(a) != 0 else None


	def nodes_by_index(self, index:Union[str, int], sort:bool=False, binary_sort:bool=False) -> Union[dict, None]:
		a, index = {}, str(index).split('.')[0].split(':'),
		for i in self.__tree:
			b = i.split(':')
			if len(b) == len(index)+1 and ':'.join(index)+':' in i:
				del b[-1]
				if len(''.join(b)) == len(''.join(index)):
					a[i] = self.__tree[i]
		return ((self.sorting_nodeIDT(a) if sort else a) if not binary_sort else self.sort_by_seed_min_or_maxIDT(a)) if len(a) != 0 else None


	def node_by_index(self, index:Union[str, int]) -> Union[dict, None]:
		a = self.logic_from_index(index)
		b = f'0{"."+str(int(a)) if a != None else ""}'
		return {b:self.__tree[b]} if b in self.__tree else None


	def logic_from_index(self, index:Union[str, int]) -> Union[bool, None]:
		index = str(index).split('.')[0]
		return True if f'{index}.1' in self.__tree.keys() else False if f'{index}.0' in self.__tree.keys() else None


	def logic_from_seed(self, seed:Union[str, int]) -> Union[dict, None]:
		a, b = {}, self.index(seed)
		if b != None:
			for i in self.index(seed):
				a[i] = self.logic_from_index(i)
			return a
		return None


	def tree_extension(self, seed_or_index:Union[str, int]) -> Union[bool, None]:
		if self.type(seed_or_index) == 'seed':
			h = self.index(seed_or_index)
			if h == None:
				return None
			seed_or_index = h[0]
		else:
			b = self.logic_from_index(seed_or_index)
			seed_or_index = f'{str(seed_or_index).split(".")[0]}{"."+str(int(b)) if b != None else ""}'
			if not(seed_or_index in self.__tree):
				return None
		b = self.nodes_by_index(seed_or_index)
		if b == None:
			return False
		elif len(b) != 0:
			return True


	def tree_continuation_by_index(self, index:Union[str, int]) -> Union[dict, None]:
		index = str(index).split('.')[0]
		b = self.logic_from_index(index)
		c = f'{index}{"."+str(int(b)) if b != None else ""}'
		if c in self.__tree:
			b = []
			a = {c:self.__tree[c]}
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
		a = '{'
		d = list(self.root_nodes())
		for i in range(len(d)):
			b, h, g = self.logic_from_index(d[i]), 0, []
			a += '"%s": %s' % (self.__tree[f'{i}{"."+str(int(b)) if b != None else ""}']+' '+str(i), '{' if self.tree_extension(0) == True else 'null')
			b = list(self.nodes_by_index(d[i]))
			while True:
				if b[h] not in g:
					c = self.tree_extension(b[h])
					a += f'"{self.__tree[b[h]]}": {"null" if c == False else "{"}{", " if len(b)-1 != h and c == False else ""}'
					g.append(b[h])
					if c == True:
						b, h = list(self.nodes_by_index(b[h])), 0
						continue
				if h == len(b)-1:
					c = self.root_index_by_index(b[h])
					b = list(self.nodes_from_index(c))
					if len(b) == len(d):
						a += '}%s' % ('' if str(c) == max(b) else ', ')
						if i == len(d)-1:
							a += '}'
							return loads(a) if js == True else a
						break
					h = 0
				h += 1


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
						if int(a[0].split('.')[0].split(':')[0]) != root_seed_index:
							del a[0]
					return a if len(a) != 0 else None
			elif type == 'index':
				seed_or_index = str(seed_or_index).split('.')[0]
				a = self.logic_from_index(seed_or_index)
				b = f'{seed_or_index}{"."+str(int(a)) if a != None else ""}'
				if b in self.__tree:
					return [b] if root_seed_index == None else [b] if int(b.split('.')[0].split(':')[0]) == root_seed_index else None
			else:
				type = self.type(seed_or_index)
				continue
			return None


	def type(self, value:Union[str, int]) -> str:
		try:
			int(f'{value}'.replace('.', '').replace(':', ''))
			a = self.logic_from_index(value)
			if f'{str(value).split(".")[0]}{"."+str(int(a)) if a != None else ""}' in self.__tree:
				return 'index'
			else:
				return 'seed'
		except ValueError:
			return 'seed'


	def max_level(self) -> int:
		a = 0
		for i in self.__tree:
			b = i.split('.')[0].split(':')
			a = len(b) if len(b) > a else a
		return a


	def max_index(self) -> str:
		c = 0
		for i in self.__tree:
			b = i.split('.')[0].split(':')
			if c <= int(b[-1]):
				c, h = int(b[-1]), ':'.join(b)
		return h


	def max_node(self) -> Union[dict, None]:
		return self.node_by_index(self.max_index())


	def root_nodes(self) -> dict:
		return self.nodes_by_level(1)


	def root_index_by_index(self, index:Union[str, int]) -> Union[str, None]:
		index = str(index).split('.')[0].split(':')
		del index[-1]
		index = ':'.join(index)
		a = self.logic_from_index(index)
		b = f'{index}{"."+str(int(a)) if a != None else ""}'
		if b in self.__tree:
			return b
		return None


	def nodes_from_index(self, index:Union[str, int]) -> Union[dict, None]:
		index = str(index).split('.')[0].split(':')
		del index[-1]
		index = ':'.join(index)
		a = {}
		b = 0
		while True:
			h = f'{index}{":" if index != "" else ""}{b}'
			c = self.logic_from_index(h)
			h = f'{h}{"."+str(int(c)) if c != None else ""}'
			if h in self.__tree:
				a[h] = self.__tree[h]
				b += 1
				continue
			return a if len(a) != 0 else None


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
							text = text + ('|' if k == 0 else 'o' if (i.split('.')[1] if '.' in i else '1') == '1' else 'x')
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
				coord, coord2 = coord2[j].split('.')[0], coord2[j]
				list_seed_or_seed = self.__list_seed if list_seed_or_seed == None and len(self.__list_seed) != 0 else list_seed_or_seed
				if not isinstance(list_seed_or_seed, list) and list_seed_or_seed != None:
					list_seed_or_seed = [list_seed_or_seed]
				elif list_seed_or_seed != None and len(list_seed_or_seed) == 0:
					list_seed_or_seed = None
				if list_seed_or_seed != None:
					for i in range(len(list_seed_or_seed)):
						self.__tree[f'{coord}:{(len(b) if b != None else 0)+i}.{0 if list_seed_or_seed[i] in self.__knowledge else 1}'] = list_seed_or_seed[i]
						self.__value_knowledge = list_seed_or_seed[i]
						self.update_knowledge(False)
						if i+1 == self.__node_quantity:
							break
					if len(self.__new_knowledge) != 0:
						self.__history_of_knowledge.append(self.__new_knowledge.copy())
				else:
					self.__tree[f'{coord}.0'] = self.__tree.pop(coord2)
				self.rsp()
				break
			else:
				if j == a-1:
					if self.__error:
						raise BufferError(self.__te._BufferError0(seed_or_index))
					self.__log.error(f'BufferError: {self.__te._BufferError0(seed_or_index)}')


	def add_root_node(self, seed:Union[str, int], list_seed:Union[list, str, int, None]=None, type_knowledge_creation:Union[str, None]=None, automatic_movement:bool=True) -> None:
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
				coord, coord2 = coord2[i].split('.')[0], coord2[i]
				if logic and self.__tree[coord2] not in list(self.nodes_from_logic(1).values()):
					self.__tree[f'{coord}.1'] = self.__tree.pop(coord2)
				elif not logic:
					self.__tree[f'{coord}.0'] = self.__tree.pop(coord2)
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
		a = len(coord2)
		for j in range(a):
			if self.tree_extension(coord2[j]) == False:
				self.__new_knowledge.clear()
				coord, coord2 = coord2[j].split('.')[0], coord2[j]
				self.__tree[f'{coord}{".1" if self.__pt.index(self, new_seed) == None else ".0"}'] = self.__tree.pop(coord2)[0] if new_seed == None else [self.__tree.pop(coord2), new_seed] if isinstance(self.__tree[coord2], list) == False else [self.__tree.pop(coord2)[0], new_seed]
				self.__value_knowledge = list_seed[i]
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
					if a-1 == i and rsp == True:
						if self.__error:
							raise BufferError(self.__te._BufferError2(coord[i]))
						self.__log.error(f'BufferError: {self.__te._BufferError2(coord[i])}')
						return
					continue
			c = self.logic_from_index(coord[i])
			if coord[i] not in self.__pt.nodes_by_level(self, ):
				for j in self.tree_continuation_by_index(coord[i]):
					del self.__tree[j]
				self.rsp()
				break
			else:
				if a-1 == i:
					if self.__error:
						raise BufferError(self.__te._BufferError3())
					self.__log.error(f'BufferError: {self.__te._BufferError3()}')


	def delete_duplicates(self) -> None:
		for i in self.__knowledge:
			a = self.index(i)
			if a != None and len(a) > 1:
				for j in a:
					if not self.tree_extension(j) and not bool(self.logic_from_index(j)):
						del self.__tree[j]


	def sort(self) -> None:
		a = {}
		k = 0
		for d in range(len(self.__root_seed_list)):
			a[list(self.nodes_by_level(1))[d]] = self.__root_seed_list[d]
			b, c = self.nodes_by_index(d, True, self.__binary_sort), []
			if b != None:
				for i in b:
					a[i] = b[i]
					c.append(i.split('.')[0])
				k += len(self.tree_continuation_by_index(d))
				while len(a) != k:
					for i in c:
						b = self.nodes_by_index(i, True)
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
				self.__tree[i.split('.')[0]] = self.__tree.pop(i)


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


	def _general_knowledge(self) -> list:
		return self.__general_knowledge.copy()


class BinaryTree(CreateTree):


	def __init__(self, root_seed:Union[str, int], seed:Union[str, int, None]=None) -> None:
		self.__bt = CreateTree
		self.__bt.__init__(self, root_seed, binary_sort=True, node_quantity=2)
		self.__te = _TextError
		if seed != None:
			self.append(seed)


	def append(self, seed:Union[str, int]) -> None:
		a = self._general_knowledge()
		if seed not in a:
			for i in a:
				pass
		else:
			raise BufferError(self.__te._BufferError4(seed))


class TreeNLT(CreateTree, ParserTreeNLT):


	def __init__(self, treeNLT, specific_type:Union[str, None]=None, type_knowledge_creation:str='list_knowledge', sort:bool=True, binary_sort:bool=False, removing_logic:bool=True, error:bool=True, node_quantity:Union[int, None]=None, rsp:bool=True, delete_duplicates:bool=False, duplicate_root_node:bool=True) -> None:
		self.__pt = ParserTreeNLT
		self.__pt.__init__(self, treeNLT)
		self.__t = CreateTree
		self.__t.__init__(self, specific_type=specific_type,
						  type_knowledge_creation=type_knowledge_creation,
						  sort=sort, binary_sort=binary_sort,
						  removing_logic=removing_logic,
						  error=error, node_quantity=node_quantity,
						  rsp=rsp,
						  delete_duplicates=delete_duplicates,
						  duplicate_root_node=duplicate_root_node)
		a = self.dividing_tree_by_root_node()
		for i in range(len(a)):
			self.add_root_node(a[i][0], a[i][1])
			b = a[i][1]


class TreeIDT(TreeNLT, ParserTreeIDT):


	def __init__(self, treeIDT, specific_type:Union[str, None]=None, type_knowledge_creation:str='list_knowledge', sort:bool=True, binary_sort:bool=False, removing_logic:bool=True, error:bool=True, node_quantity:Union[int, None]=None, rsp:bool=True, delete_duplicates:bool=False, duplicate_root_node:bool=True) -> None:
		pass


class SaveImage(ParserTreeIDT):


	def __init__(self, treeIDT:dict, name_image:str='tree_image', background:str='white', occupy_px:int=20, space_px:int=5) -> None:
		tp = ParserTree
		tp.__init__(self, tree)
		a = sum([int(i) for i in tp.max_index(self).split('.')[0].split(':')])
		img = Image.new('RGBA', ((a+1)*occupy_px+a*space_px, 100), background)
		img.save(f'{name_image}.png')


	def __str__(self) -> str:
		pass


class SaveFileJS():


	pass
