# Test function to create a wiki tree.

from .__init__ import Wiki, CreateTree


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
