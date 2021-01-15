# Test function to create a binary tree.

from random import randint
from .__init__ import BinaryTree, ParserTreeIDT, text_info_for_logging
import logging


logging.basicConfig(format=text_info_for_logging, level=logging.DEBUG)


def run():
	a = BinaryTree()
	logging.info('A binary tree was created.')
	a.rsp(rsp=False)
	for i in range(randint(10, 25)):
		try:
			b = randint(0, 50 if i == 0 else 100)
			a.append(b)
			logging.info(f'The number {b} has been added.')
		except BufferError as er:
			logging.error(er)
	a.rsp(rsp=True)


	logging.info('The process of saving the binary tree is in progress.')
	a = ParserTreeIDT(a.processed_tree)
	file = open('test_tree.js', 'w')
	file.write(f'{a.tree_NLT()}')
	file.close()
	logging.info('The binary tree is saved in test_tree.js file.')


	logging.info('End of function.')

if __name__ == '__main__':
	run()