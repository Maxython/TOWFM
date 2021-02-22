# Test function to create a binary tree.

from random import randint
from .__init__ import BinaryTree, ParserTreeIDT, text_info_for_logging, dumps
import logging


logging.basicConfig(format=text_info_for_logging, level=logging.DEBUG)


def run(rand_range:int=25, rand_seed:int=100, print_tree:bool=True, save_tree:bool=False, name_file:str=None, information:bool=False, return_tree:bool=False) -> None:
	logging.debug(f'Random range = {rand_range}')
	if not isinstance(rand_range, int) or rand_range <= 0:
		logging.critical('Error in rand_range value.')
		return
	logging.debug(f'Random seed = {rand_seed}')
	if not isinstance(rand_seed, int) or rand_seed <= 0:
		logging.critical('Error in rand_seed value.')
		return
	logging.debug(f'Additional Information = {information}')
	a = BinaryTree()
	logging.info('A binary tree was created.')
	a.rsp(rsp=False)
	for i in range(randint(int(rand_range*0.4), rand_range)):
		try:
			b = randint(0, rand_seed//2 if i == 0 else rand_seed)
			a.append(b)
			logging.info(f'The number {b} has been added.')
		except BufferError as er:
			logging.error(er)
	a.rsp(rsp=True)


	if print_tree:
		print()
		logging.info('Binary tree output')
		a.pt(information)
		print()


	if save_tree:
		logging.info('The process of saving the binary tree is in progress.')
		b = ParserTreeIDT(a.processed_tree)
		file = open(name_file if name_file != None else 'test_tree.js', 'w')
		file.write('{\n')
		file.write(f'    "tree":{dumps(a.tree)},\n    "processed_tree":{a.processed_tree},\n    "NDT":{b.tree_NDT(False)},\n    "NLT":{dumps(b.tree_NLT())}')
		if information:
			file.write(f',\n    "root_seed":"{a.root_seed}",\n    "seed_amount":"{len(a.processed_tree)}",\n    "max_index":"{a.max_index()}",\n    "max_level":"{a.max_level()}"')
		file.write('\n}')
		file.close()
		logging.info('The binary tree is saved in test_tree.js file.')


	logging.info('End of function.')


	if return_tree:
		return a.processed_tree


if __name__ == '__main__':
	run()
else:
	logging.info('You have imported module for the binary tree test.')
