import wikipedia
import requests
from typing import Union
from PIL import Image, ImageFilter, ImageDraw
from json import loads, dumps
import logging


text_info_for_logging = '[%(levelname)s | %(asctime)s | %(message)s]'
delete_character_list = ['(', ')', '[', ']', '.', ',', '!', '?', ':', ';', '"', "'", '»', '«']
list_knowledge = []


class _TextError:


	def _ValueError0(value:str) -> str:
		return f'there is no "{value}" meaning in the tree.'


	def _BufferError0(value:str) -> str:
		return f'in seed "{value}" there is an extension of the tree or is positive.'


	def _BufferError1(value:str) -> str:
		return f'in seed "{value}" you cannot change the seed, because it has an extension of the tree.'


	def _BufferError2(value:str) -> str:
		return f'no access to delete positive seed "{value}".'


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
				con = wikipedia.summary(seed).split()
				con2 = []
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
			return loads(dumps(self.__list))


	@property
	def seed(self) -> str:
		if self.__seed != None:
			return f'{self.__seed}'


	@property
	def replacement_seed(self) -> bool:
		if self.__replacement_seed == True:
			return True
		else:
			return False


	@property
	def old_seed(self) -> Union[str, None]:
		if self.__old_seed != None:
			return f'{self.__old_seed}'


class ParserTreeIDT:


	def __init__(self, tree_idt:dict) -> None:
		self.__tree = tree_idt


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
					c = int(b[level-1])
					h = ':'.join(b)
		try:
			return h
		except UnboundLocalError:
			return None


	def max_index_by_index(self, index:str) -> Union[str, None]:
		a = 0
		index = str(index).split('.')[0]
		while True:
			if self.seed(f'{index}:{a}') == None:
				if a != 0:
					b = self.logic_from_index(f'{index}:{a-1}')
					c = f'{index}:{a-1}{"."+str(int(b)) if b != None else ""}'
					if c in self.__tree:
						return c
					return None
				else:
					if self.max_index_by_level(len(index.split(':'))+1) == None:
						return None
			a += 1


	def seed(self, index:Union[str, int]) -> Union[str, None]:
		try:
			a = self.logic_from_index(index)
			return self.__tree[f'{index}{"."+str(int(a)) if a != None else ""}']
		except (KeyError, TypeError):
			try:
				return self.__tree[index]
			except KeyError:
				return None


	def nodes_by_level(self, level:int) -> dict:
		a = {}
		for i in self.__tree:
			if len(i.split('.')[0].split(':')) == level:
				a[i] = self.__tree[i]
		return a


	def nodes_by_index(self, index:Union[str, int]) -> Union[dict, None]:
		a = {}
		index = str(index).split('.')[0]
		try:
			for i in range(int(self.max_index_by_index(index).split('.')[0].split(':')[-1])+1):
				try:
					b = self.logic_from_index(f'{index}:{i}')
					a[f'{index}:{i}{"."+str(int(b)) if b != None else ""}'] = self.__tree[f'{index}:{i}{"."+str(int(b)) if b != None else ""}']
				except KeyError:
					continue
			return a
		except AttributeError:
			return None


	def node_by_index(self, index:Union[str, int]) -> Union[dict, None]:
		a = self.logic_from_index(index)
		b = f'0{"."+str(int(a)) if a != None else ""}'
		return {b:self.__tree[b]} if b in self.__tree else None


	def logic_from_index(self, index:Union[str, int]) -> Union[bool, None]:
		index = str(index).split('.')[0]
		if f'{index}.1' in self.__tree.keys():
			return True
		elif f'{index}.0' in self.__tree.keys():
			return False
		else:
			return None


	def logic_from_seed(self, seed:Union[str, int]) -> Union[dict, None]:
		a = {}
		b = self.index(seed)
		if b != None:
			for i in self.index(seed):
				a[i] = self.logic_from_index(i)
			return a
		return None


	def tree_extension(self, seed_or_index:Union[str, int]) -> Union[bool, None]:
		a = self.type(seed_or_index)
		if a == 'seed':
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
		index = index.split('.')[0]
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
					b = list(self.nodes_by_index(b[h]))
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


	def index_certain_type(self, seed_or_index:Union[str, int], type:str='seed') -> Union[list, None]:
		if type == 'seed':
			return self.index(seed_or_index)
		else:
			seed_or_index = seed_or_index.split('.')[0]
			a = self.logic_from_index(seed_or_index)
			b = f'{seed_or_index}{"."+str(int(a)) if a != None else ""}'
			if b in self.__tree:
				return [b]
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


class ParserTreeNDT:


	def __init__(self, tree:dict) -> None:
		self.__tree = tree
		print(tree)


	def nodes(self, coord:Union[int, str]) -> Union[list, None]:
		coord, a = coord.split('/'), self.__tree
		for i in coord:
			try:
				a = a[i]
			except KeyError:
				return None
		a = list(a.keys()) if a != None else 'no continue'
		return a


	def root_node(self) -> str:
		a = list(self.__tree.keys())
		return a[0] if len(a) != 0 else None


class ParserTreeNLT:


	def __init__(self, tree:list) -> None:
			self.__tree = tree


	def index(self, node:Union[str, int]) -> Union[list, None]:
		a, b = [], self.__tree
		for i in range(len(b)):
			if b[i] != self.root_node() and b[i] != None:
				for j in range(len(b[i])):
					if b[i][j] == node:
						a.append(f'{i}:{j}')
		return a if len(a) != 0 else None


	def node(self, index:Union[str, int]) -> Union[str, int, None]:
		index, a = str(index).split(':'), self.__tree
		for i in index:
			try:
				a = a[int(i)]
			except (IndexError, ValueError, TypeError):
				return None
		return a


	def nodes_by_index(self, index:Union[str, int]) -> Union[list, None]:
		try:
			return self.__tree[sum([int(i) for i in str(index).split(':')])+1]
		except (ValueError, IndexError):
			return None


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


	def tree_continuation_by_index(self, index:Union[str, int]) -> Union[list, None]:
		a, c, b, g  = [self.node(index)], [index], 0, int(str(index).split(':')[0])
		while True:
			print(a)
			print(c[b])
			e = self.nodes_by_index(c[b])
			if g <= int(c[b].split(':')[0]):
				a.append(e)
				try:
					for i in e:
						for j in self.index(i):
							if g == int(j.split(':')[0]) and j not in c:
								c.append(j)
				except TypeError:
					pass
				g += self.__tree.index(c[b])
				b += 1
				if b == 10:
					break
		return a


	def index_from_indexIDT(self, indexIDT:Union[str, int]) -> Union[str, int, None]:
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


	def indexIDT_from_index(self, index:Union[str, int]) -> Union[str, int, None]:
		a = '0'
		index = str(index).split(':')


	def node_by_indexIDT(self, indexIDT:Union[str, int]) -> Union[str, int, None]:
		return self.node(self.index_from_indexIDT(indexIDT))


	def root_node(self) -> str:
		return f'{self.__tree[0]}'


class CreateTree(ParserTreeIDT, _TextError):


	def __init__(self, seed:Union[str, int], list_seed:Union[list, None]=None, sort:bool=True, removing_logic:bool=True, error:bool=True, node_quantity:int=None) -> None:
		self.__tree = {}
		self.__tree[f'0.{0 if seed in list_knowledge else 1}'] = seed
		self.__knowledge = list_knowledge
		self.__knowledge.append(seed)
		self.__new_knowledge = []
		self.__history_of_knowledge = []
		self.__root_seed = seed
		self.__index_print = '0'
		self.__sort = sort
		self.__removing_logic = removing_logic
		self.__node_quantity = node_quantity
		self.__error = error
		self.__list_seed = []
		self.__te = _TextError
		self.__pt = ParserTreeIDT
		self.update_pt()
		if error == False:
			self.__log = logging
			self.__log.basicConfig(format=text_info_for_logging)
		if list_seed != None:
			self.add(self.__root_seed, list_seed)


	def __str__(self) -> str:
		text = '\n'
		try:
			c = self.__pt.logic_from_index(self, self.__index_print)
			a = {f'{self.__index_print}{"."+str(int(c)) if c != None else ""}':f'{self.__pt.seed(self, self.__index_print)}'}
			h = self.__pt.nodes_by_index(self, self.__index_print)
			if h != None:
				for i in h:
					a[i] = f'{h[i]}'
				b = 0
				for i in a:
					text = text + a[i]
					if b == 0:
						text = text + '\n|\n'
					elif b == len(a)-1:
						text = text + '\n'
					else:
						text = text + '--'
					b += 1
				b = 0
				for k in range(2):
					for i in a:
						if b != 0:
							c = i.split('.')[1] if '.' in i else '1'
							text = text + ('|' if k == 0 else 'o' if c == '1' else 'x')
							for j in range(len(a[i])-1):
								text = text + ' '
							text = text + ('  ' if len(a)-1 != b else '\n' if k == 0 else '\n\n')
						b += 1
					b = 0
			else:
				text = text + self.__pt.seed(self, self.__index_print) + '\n|\n' + ('o' if str(int(c)) == '1' else 'x') + '\n\n'
		except TypeError:
			pass
		text = text + f'seed: {self.__root_seed}\nmax level: {self.__pt.max_level(self)}\nmax index: {self.__pt.max_index(self)}\namount of knowledge: {len(self.__knowledge)}\nword count: {len(self.__tree)}\n'
		return text


	def add(self, seed_or_index:Union[str, int], list_seed:Union[list, None]=None, type:str='seed') -> None:
		coord2 = self.__pt.index_certain_type(self, seed_or_index, type)
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
						if list_seed[i] not in self.__knowledge:
							self.__knowledge.append(list_seed[i])
							self.__new_knowledge.append(list_seed[i])
						if i+1 == self.__node_quantity:
							break
					if len(self.__new_knowledge) != 0:
						self.__history_of_knowledge.append(self.__new_knowledge.copy())
				else:
					self.__tree[f'{coord}.0'] = self.__tree.pop(coord2)
					if list_seed not in self.__knowledge:
						self.__knowledge.append(list_seed)
						self.__new_knowledge.append(list_seed)
						if len(self.__new_knowledge) != 0:
							self.__history_of_knowledge.append(self.__new_knowledge.copy())
				self.rsp()
				break
			else:
				if j == a-1:
					if self.__error:
						raise BufferError(self.__te._BufferError0(seed_or_index))
					self.__log.error(f'BufferError: {self.__te._BufferError0(seed_or_index)}')


	def replacement(self, seed_or_index:Union[str, int], new_seed:Union[str, None], type:str='seed') -> None:
		coord2 = self.__pt.index_certain_type(self, seed_or_index, type)
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
				if new_seed not in self.__knowledge:
					self.__knowledge.append(new_seed)
					self.__new_knowledge.append(new_seed)
					if len(self.__new_knowledge) != 0:
						self.__history_of_knowledge.append(self.__new_knowledge.copy())
				self.rsp()
				break
			else:
				if j == a-1:
					if self.__error:
						raise BufferError(self.__te._BufferError1(seed_or_index))
					self.__log.error(f'BufferError: {self.__te._BufferError1(seed_or_index)}')


	def delete(self, seed_or_index:str, type:str='seed', positive_seeds:bool=False) -> None:
		coord = self.__pt.index_certain_type(self, seed_or_index, type)
		if coord == None:
			if self.__error:
				raise ValueError(self.__te._ValueError0(seed_or_index))
			self.__log.error(f'ValueError: {self.__te._ValueError0(seed_or_index)}')
			return
		a = len(coord)
		for i in range(a):
			if positive_seeds == False:
				if self.__pt.tree_extension(self, coord[i]) == True or self.__pt.logic_from_index(self, coord[i]) != False:
					if a-1 == i:
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


	def sort(self) -> None:
		a = {min(self.__pt.index(self, self.__root_seed)):self.__root_seed}
		b = self.__pt.nodes_by_index(self, '0')
		c = []
		if b != None:
			for i in b:
				a[i] = b[i]
				c.append(i.split('.')[0])
			while len(a) != len(self.__tree):
				for i in c:
					b = self.__pt.nodes_by_index(self, i)
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
			if self.__pt.tree_extension(self, i) == True:
				self.__tree[i.split('.')[0]] = self.__tree.pop(i)


	def index_print(self, index:Union[str, int]) -> None:
		self.__index_print = index


	def update_pt(self) -> None:
		self.__pt.__init__(self, self.__tree)


	def rsp(self) -> None:
		if self.__removing_logic == True:
			self.removing_logic()
		if self.__sort == True:
			self.sort()
		self.update_pt()


	def list_seed(self, value:Union[str, int, None]=None) -> Union[None, list]:
		if value == None:
			return loads(dumps(self.__list_seed))
		self.__list_seed.append(value)


	@property
	def tree(self) -> dict:
		return loads(dumps(self.__tree))


	@property
	def knowledge(self) -> list:
		return loads(dumps(self.__knowledge))


	@property
	def new_knowledge(self) -> list:
		return loads(dumps(self.__new_knowledge))


	@property
	def history_of_knowledge(self) -> list:
		return loads(dumps(self.__history_of_knowledge))


	@property
	def root_seed(self) -> str:
		return f'{self.__root_seed}'


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
