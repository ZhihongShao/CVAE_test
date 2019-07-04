'''
A module for GloVe
'''
import os.path
import numpy as np

from .wordvector import WordVector
from .._utils.file_utils import get_resource_file_path

class Glove(WordVector):
	r'''GloVe is pre-trained word vectors from
	Jeffrey Pennington, Richard Socher, and Christopher D. Manning. 2014.
	GloVe: Global Vectors for Word Representation.

	Arguments:
		file_id (str): a str indicates the source of GloVe word vectors. If it is local file,
			it can be a directory contains 'glove.txt' or a text file.
		file_type (str): a str indicates the type of GloVe word vectors. Default: Glove300d
	'''
	def __init__(self, file_id):
		super().__init__()
		if file_id is not None:
			self.file_id = file_id
			self.file_path = get_resource_file_path(file_id)
		else:
			self.file_id = self.file_path = None

	def load(self, n_dims, vocab_list):
		r'''
		Refer to :meth:`.WordVector.load`.
		'''
		raw_word2vec = {}
		if self.file_path:
			file_path = self.file_path
			if os.path.isdir(file_path):
				file_path = "%s/glove.txt" % (file_path)
			with open(file_path, 'r') as glove_file:
				lines = glove_file.readlines()
			for line in lines:
				word, vec = line.split(" ", 1)
				raw_word2vec[word] = vec

		wordvec = []
		oov_cnt = 0
		for vocab in vocab_list:
			str_vec = raw_word2vec.get(vocab, None)
			vec = np.random.randn(n_dims) * 0.1
			if str_vec is None:
				oov_cnt += 1
			else:
				tmp = np.fromstring(str_vec, sep=" ")
				now_dims = min(len(tmp), n_dims)
				vec[:now_dims] = tmp[:now_dims]
			wordvec.append(vec)
		print("wordvec cannot cover %f vocab" % (float(oov_cnt)/len(vocab_list)))
		return np.array(wordvec)
