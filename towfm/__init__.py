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

	def _ValueError0(value:str) -> str:
		return f'there is no "{value}" meaning in the tree.'


	def _BufferError0(value:str) -> str:
		return f'in node "{value}" there is an extension of the tree or is positive.'


	def _BufferError1(value:str) -> str:
		return f'in node "{value}" you cannot change the seed, because it has an extension of the tree.'


	def _BufferError2(value:str) -> str:
		return f'no access to delete positive node "{value}".'


	def _BufferError3() -> str:
		return 'you cannot delete the root seed of the tree.'


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


	def index_from_indexIDT(self, indexIDT:Union[str, int]) -> Union[str, None]:
		try:
			indexIDT = [int(x) for x in str(indexIDT).split('.')[0].split(':')]
			if len(indexIDT) > 1:
				indexIDT[0] += 1
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


	def type_translation_coordNDT(self, coordNDT:str, separators:str='/') -> Union[str, int]:
		coordNDT = str(coordNDT).split(separators)
		try:
			return int(coordNDT[0]) if coordNDT[-1] == 'int' else coordNDT[0]
		except ValueError:
			return coordNDT[0]


	def list_coord_from_coordNDT(self, coordNDT:str, separators:str='/') -> list:
		coordNDT = coordNDT.split(separators+separators)
		for i in range(len(coordNDT)):
			coordNDT[i] = self.type_translation_coordNDT(coordNDT[i], separators)
		return coordNDT


class ParserTreeIDT(Subtraction):


	def __init__(self, tree_idt:dict) -> None:
		self.__tree = tree_idt
		self.__s = Subtraction


	def nodes_from_contin_growth(self, logic:Union[bool, int, str, None]) -> dict:
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
		return list


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


	def nodes_by_level(self, level:Union[int, str], sort:bool=False) -> dict:
		a = {}
		for i in self.__tree:
			if len(i.split('.')[0].split(':')) == int(level):
				a[i] = self.__tree[i]
		return self.sorting_node(a) if sort else a


	def nodes_by_index(self, index:Union[str, int], sort:bool=False) -> Union[dict, None]:
		a, index, b = {}, str(index).split('.')[0], 0
		for i in self.__tree:
			if len(i.split(':')) == len(index.split(':'))+1 and index+':' in i:
				a[i] = self.__tree[i]
				b += 1
		return (self.sorting_node(a) if sort else a) if len(a) != 0 else None


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
		b, h, g = self.logic_from_index(0), 0, []
		a, b = '{"%s": %s' % (self.__tree[f'0{"."+str(int(b)) if b != None else ""}'], '{' if self.tree_extension(0) == True else 'null'), list(self.nodes_by_index(0))
		while True:
			if b[h] not in g:
				c = self.tree_extension(b[h])
				a = a + f'"{self.__tree[b[h]]}": {"null" if c == False else "{"}{", " if len(b)-1 != h and c == False else ""}'
				g.append(b[h])
				if c == True:
					b, h = list(self.nodes_by_index(b[h])), 0
					continue
			if h == len(b)-1:
				c = self.root_index_by_index(b[h])
				b = list(self.nodes_from_index(c))
				if len(b) == 1:
					a = a + '}}'
					return loads(a) if js == True else a
				a, h = a + '}%s' % ('' if c == max(b) else ', '), 0
			h += 1


	def tree_NLT(self) -> list:
		a = [self.seed(0)]
		if a[0] != None:
			b = ['0']
			while len(b) != len(self.__tree):
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
					for i in range(len(a.copy())-1):
						if int(a[i].split('.')[0].split(':')[0]) != root_seed_index:
							del a[i]
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


	def sorting_node(self, nodes:dict) -> dict:
		index = self.root_index_by_index(list(nodes.keys())[0])
		b, c, i = 0, {}, 0
		while len(nodes) != len(c):
			f = index+':'+str(b)
			d = self.logic_from_index(f)
			d = '.'+str(int(d)) if d != None else ''
			f = f+d
			if f in nodes:
				c[index+f':{i}{d}'] = nodes[f]
				i += 1
			b += 1
		return c


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


	def root_node(self) -> dict:
		return self.node_by_index(0)


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


	def __init__(self, tree:dict) -> None:
		self.__tree = tree
		self.__s = Subtraction


	def nodes(self, coord:Union[int, str], separators:str='/') -> Union[list, None]:
		a = self.__tree
		for i in coord.split(separators+separators):
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
			return (separators+separators).join(b) if len(b) != 0 else None
		except (IndexError, ValueError):
			return None


	def root_node(self) -> str:
		a = list(self.__tree.keys())
		return a[0] if len(a) != 0 else None


class ParserTreeNLT(Subtraction):


	def __init__(self, tree:list) -> None:
			self.__tree = tree
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


	def nodes_by_indexIDT(self, indexIDT:Union[str, int]) -> Union[str, int, None]:
		return self.node(self.__s.index_from_indexIDT(self, indexIDT))


	def index_from_coordNDT(self, coordNDT:str, separators:str='/') -> Union[str, None]:
		try:
			coordNDT = coordNDT.split(separators+separators)
			a = self.index_by_index(self.index(self.__s.type_translation_coordNDT(self, coordNDT[0]))[0])
			for i in range(len(coordNDT)):
				if i != 0:
					b = f'{a}:{self.__tree[a].index(self.__s.type_translation_coordNDT(self, coordNDT[i]))}'
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


	def tree_IDT(self) -> dict:
		a = {}
		return a


	def tree_NDT(self) -> dict:
		a = {}
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


	def root_node(self) -> str:
		return f'{self.__tree[0]}'


class CreateTree(ParserTreeIDT, _TextError):


	def __init__(self, seed:Union[str, int, None]=None, list_seed:Union[list, None]=None, specific_type:str=None, type_knowledge_creation:str='list_knowledge', sort:bool=True, removing_logic:bool=True, error:bool=True, node_quantity:int=None, rsp:bool=True, delete_duplicates:bool=False, duplicate_root_node:bool=True) -> None:
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
		if seed != None:
			self.add_root_node(seed, list_seed)


	def __str__(self) -> str:
		text = '\n'
		try:
			c = self.__pt.logic_from_index(self, self.__index_print)
			a, h = {f'{self.__index_print}{"."+str(int(c)) if c != None else ""}':f'{self.__pt.seed(self, self.__index_print)}'}, self.__pt.nodes_by_index(self, self.__index_print)
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
				text = text + self.__pt.seed(self, self.__index_print) + '\n|\n' + ('o' if str(int(c)) == '1' else 'x') + '\n\n'
		except TypeError:
			pass
		text = text + f'root seed: {self.__root_seed_list[self.__root_seed_index]}\nmax level: {self.__pt.max_level(self)}\nmax index: {self.__pt.max_index(self)}\namount of knowledge: {len(self.__knowledge)}\nword count: {len(self.__tree)}\n'
		return text


	def add(self, seed_or_index:Union[str, int], list_seed:Union[list, None]=None, type:str=None) -> None:
		coord2 = self.__pt.index_certain_type(self, seed_or_index, type if type != None else self.__specific_type, self.__root_seed_index)
		if coord2 == None:
			if self.__error:
				raise ValueError(self.__te._ValueError0(seed_or_index))
			self.__log.error(f'ValueError: {self.__te._ValueError0(seed_or_index)}')
			return
		a = len(coord2)
		for j in range(a):
			if self.__pt.tree_extension(self, coord2[j]) == False and self.__pt.logic_from_index(self, coord2[j]) == True:
				self.__new_knowledge.clear()
				coord, coord2 = coord2[j].split('.')[0], coord2[j]
				list_seed = self.__list_seed if list_seed == None and len(self.__list_seed) != 0 else list_seed
				if list_seed != None:
					for i in range(len(list_seed)):
						self.__tree[f'{coord}:{i}.{0 if list_seed[i] in self.__knowledge else 1}'] = list_seed[i]
						self.__value_knowledge = list_seed[i]
						self.update_knowledge(False)
						if i+1 == self.__node_quantity:
							break
					if len(self.__new_knowledge) != 0:
						self.__history_of_knowledge.append(self.__new_knowledge.copy())
				else:
					self.__tree[f'{coord}.0'] = self.__tree.pop(coord2)
					self.__value_knowledge = list_seed[i]
					self.update_knowledge()
				self.rsp()
				break
			else:
				if j == a-1:
					if self.__error:
						raise BufferError(self.__te._BufferError0(seed_or_index))
					self.__log.error(f'BufferError: {self.__te._BufferError0(seed_or_index)}')


	def add_root_node(self, seed:str, list_seed:Union[list, None]=None, type_knowledge_creation:str=None, automatic_movement:bool=True) -> None:
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
			self.add(0, list_seed, type='index')


	def replacement(self, seed_or_index:Union[str, int], new_seed:Union[str, None], type:str=None) -> None:
		coord2 = self.__pt.index_certain_type(self, seed_or_index, type if type != None else self.__specific_type, self.__root_seed_index)
		if coord2 == None:
			if self.__error:
				raise ValueError(self.__te._ValueError0(seed_or_index))
			self.__log.error(f'ValueError: {self.__te._ValueError0(seed_or_index)}')
			return
		a = len(coord2)
		for j in range(a):
			if self.__pt.tree_extension(self, coord2[j]) == False:
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


	def delete(self, seed_or_index:str, type:str='seed', positive_seeds:bool=False) -> None:
		coord = self.__pt.index_certain_type(self, seed_or_index, type if type != None else self.__specific_type, self.__root_seed_index)
		if coord == None:
			if self.__error:
				raise ValueError(self.__te._ValueError0(seed_or_index))
			self.__log.error(f'ValueError: {self.__te._ValueError0(seed_or_index)}')
			return
		a = len(coord)
		for i in range(a):
			if positive_seeds == False:
				if self.__pt.tree_extension(self, coord[i]) == True or self.__pt.logic_from_index(self, coord[i]) != False:
					if a-1 == i and rsp == True:
						if self.__error:
							raise BufferError(self.__te._BufferError2(coord[i]))
						self.__log.error(f'BufferError: {self.__te._BufferError2(coord[i])}')
						return
					continue
			c = self.__pt.logic_from_index(self, coord[i])
			if coord[i] != f'0{"."+str(int(c)) if c != None else ""}':
				for j in self.__pt.tree_continuation_by_index(self, coord[i]):
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
			a = self.__pt.index(self, i)
			if a != None and len(a) > 1:
				for j in a:
					if not self.__pt.tree_extension(self, j) and not bool(self.__pt.logic_from_index(self, j)):
						del self.__tree[j]


	def sort(self) -> None:
		a = {}
		k = 0
		for d in range(len(self.__root_seed_list)):
			a[min(self.__pt.index(self, self.__root_seed_list[d]))] = self.__root_seed_list[d]
			b, c = self.__pt.nodes_by_index(self, d, True), []
			if b != None:
				for i in b:
					a[i] = b[i]
					c.append(i.split('.')[0])
				k += len(self.__pt.tree_continuation_by_index(self, d))
				while len(a) != k:
					for i in c:
						b = self.__pt.nodes_by_index(self, i, True)
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
			if self.__pt.tree_extension(self, i):
				self.__tree[i.split('.')[0]] = self.__tree.pop(i)


	def index_print(self, index:Union[str, int]) -> None:
		self.__index_print = index


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


	def rsp(self) -> None:
		if self.__rsp:
			if self.__delete_duplicates:
				self.delete_duplicates()
			if self.__removing_logic:
				self.removing_logic()
			if self.__sort:
				self.sort()
			self.update_pt()


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


class TreeIDT(CreateTree):


	def __init__(self) -> None:
		pass


class TreeNDT(CreateTree):


	def __init__(self, tree_ndt:dict, sort:bool=True, removing_logic:bool=True, error:bool=True, node_quantity:int=None) -> None:
		b = list(tree_ndt.keys())[0]
		a = CreateTree
		a.__init__(self, b, list(tree_ndt[b].keys()), sort, removing_logic, error, node_quantity)


class TreeNLT(CreateTree):


	def __init__(self, tree_nlt:list, sort:bool=True, removing_logic:bool=True, error:bool=True, node_quantity:int=None) -> None:
		pass


class SaveImage(ParserTreeIDT):


	def __init__(self, tree:dict, name_image:str='tree_image', background:str='white', occupy_px:int=20, space_px:int=5) -> None:
		tp = ParserTree
		tp.__init__(self, tree)
		a = sum([int(i) for i in tp.max_index(self).split('.')[0].split(':')])
		img = Image.new('RGBA', ((a+1)*occupy_px+a*space_px, 100), background)
		img.save(f'{name_image}.png')


	def __str__(self) -> str:
		pass


class SaveFileJS():


	pass
