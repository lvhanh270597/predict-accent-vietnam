
from helpers import file as fman

class Vocabulary:

	EXT_NAME = ".vocab"
	DELIMITER = "\t"

	def __init__(self, data=[], start=1, thresmin=0.0, thresmax=1.0):
		self.vocabulary = dict()
		self.freq = dict()
		self.start = start
		self.total = 0
		self.roundnum = 2
		self.data = data
		self.thresmin = thresmin
		self.thresmax = thresmax

	def set_threshold(self, thresmin=0.0, thresmax=1.0):
		self.thresmin = thresmin
		self.thresmax = thresmax

	def set_data(self, data):
		self.data = data

	def get_index(self, word, default=0):
		if word not in self.vocabulary:
			return default
		return self.vocabulary[word]

	def get_freq(self, word, default=0):
		if word not in self.freq:
			return default
		return self.freq[word]

	def length(self):
		return len(self.vocabulary)

	def build(self):
		for sentence in self.data:
			for word in set(sentence.split()):
				self.add(word)
		self.remove_items()

	def add(self, word):
		if word not in self.vocabulary:
			self.vocabulary[word] = self.start
			self.freq[word] = 1
			self.start += 1
			self.cnt += 1
			return True
		self.freq[word] += 1
		return False

	def remove_items(self):
		items = []
		if self.total > 0:
			for word in self.vocabulary:
				cur_freq = self.freq[word]
				v_test = round(cur_freq / self.total, self.roundnum)
				if (v_test < self.thresmin) or (v_test > self.thresmax):
					del self.vocabulary[word]
					del self.freq[word]
					items.append(word)
		return items

	def get_vector_indices_by_list(self, list_words, default=0):
		vector = []
		for word in list_words:
			index = self.get_index(word, default)
			vector.append(index)
		return vector

	def save(self, filedir, name):
		encoded_data = []
		for word in self.vocabulary:
			feature = "%s%s%d%s%d" % (word, self.DELIMITER, self.vocabulary[word], self.DELIMITER, self.freq[word])
			encoded_data.append(feature)
		fullpath = fman.join_path(filedir, name + self.EXT_NAME)
		fman.save_text(encoded_data, fullpath)

	def load(self, filedir, name):
		fullpath = fman.join_path(filedir, name + self.EXT_NAME)
		data = fman.load_text(fullpath)
		for line in data:
			word, index, freq = line.split(self.DELIMITER)
			self.vocabulary[word] = int(index)
			self.freq[word] = int(freq)

