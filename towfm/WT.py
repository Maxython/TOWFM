# Test function to create a wiki tree.

import wikipedia
import requests
from .__init__ import CreateTree, Union


#A list with a value to be removed when searched in the Wiki class.
#You can add a value to this list.
delete_character_list = ['(', ')', '[', ']', '.', ',', '!', '?', ':', ';', '"', "'", '»', '«']


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
		b, c = [], seed
		self.__replacement_seed = False
		self.__old_seed = None
		while True:
			try:
				wikipedia.set_lang(self.__lang)
				con, con2 = wikipedia.summary(seed).split(), []
				for i in range(len(con)):
					try:
						if self.__lower:
							con[i] = con[i].lower()
						for j in delete_character_list:
							con[i] = con[i].replace(j, '')
						if self.__remove_numbers:
							try:
								int(con[i])
								del con[i]
							except ValueError:
								pass
						if (con[i] == '' or len(con[i]) <= self.__deletion_with_a_certain_amount):
							del con[i]
						elif len(con2) == self.__quantity:
							break
						elif con[i] not in con2:
							con2.append(con[i])
					except IndexError:
						break
				break
			except (wikipedia.exceptions.PageError, requests.exceptions.ConnectionError):
				con2 = None
				break
			except wikipedia.exceptions.DisambiguationError:
				if self.__replacement:
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
				con2, seed = None, c
				break
		self.__list = con2
		self.__seed = seed


	@property
	def list(self) -> Union[list, None]:
		return self.__list.copy() if self.__list != None else None


	@property
	def seed(self) -> Union[str, None]:
		return f'{self.__seed}' if self.__seed != None else None


	@property
	def replacement_seed(self) -> bool:
		return True if self.__replacement_seed == True else False


	@property
	def old_seed(self) -> Union[str, None]:
		return f'{self.__old_seed}' if self.__old_seed != None else None


	def _list(self) -> list:
		return self.__list.copy() if self.__list != None else None


	def _seed(self) -> str:
		return f'{self.__seed}' if self.__seed != None else None


class CreateWT(CreateTree, Wiki):


    def __init__(self, word:str, lang:str='en', handle:bool=True, remove_numbers:bool=False, quantity:int=None) -> None:
        self.__wiki = Wiki
        self.__ct = CreateTree
        self.__wiki.__init__(self,
                             lang=lang,
                             remove_numbers=remove_numbers,
                             quantity=quantity)
        self.__ct.__init__(self, word)
        if handle:
            self.handle()


    def handle(self) -> None:
        for i in self._tree():
            if not self.tree_extension(i) and self.logic_from_index(i):
                self.search(self.seed(i))
                self.add(i, self._list())
