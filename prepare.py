from controller.manual import DataManager
from algorithms.machine_learning import *
manager = DataManager()
#manager.read_data()
manager.load_data(['vocab', 'full'])
manager.preprocessing({
    'vocab' : ['enterdel', "lower"],
    'full' : ['enterdel']
})
sentences = manager._data['full']
#
# vocab_indices = manager.get_indices('vocab')
# noa_vocab_indices = manager.get_indices(vocab_indices.keys(), False, 1, 'line', ' ', 'accentdel')
# full_indices = manager.get_indices('full', True, 1, 'word')
# noa_words = manager.get_noa_words(full_indices.keys()) # no accent word which get from full data (it has accent word is children)
# noa_indices = manager.get_indices(noa_words.keys()) # no accent word which get from full data
#
# # save all indices, then only load
# #manager.save_indices_as_json(vocab_indices, './data/runtime/vocab_indices.json')
# manager.save_indices_as_json(noa_vocab_indices, './data/runtime/noa_vocab_indices.json')
# manager.save_indices_as_json(full_indices, './data/runtime/full_indices.json')
# manager.save_indices_as_json(noa_words, './data/runtime/noa_words.json')
# manager.save_indices_as_json(noa_indices, './data/runtime/noa_indices.json')
#
# summary_data = {
#     'vocab_indices' : './data/runtime/noa_vocab_indices.json',
#     'full_indices' : './data/runtime/full_indices.json',
#     'noa_words' : './data/runtime/noa_words.json',
#     'noa_indices' : './data/runtime/noa_indices.json'
# }
#
# data = manager.load_json_files(summary_data)

#manager.get_window_item('môi trường trong sáng', 5, {'noa_indices' : noa_indices, 'vocab_indices' : noa_vocab_indices, 'full_indices' : full_indices})
#print(manager.get_window_item('anh yêu em nhiều lắm', 5, data))

#data = manager.create_window_items(sentences, 5, data)
description = {
    'data' : './data/runtime/fulldata.json'
}

data = manager.load_json_files(description)
data = data['data']

mlearner = GuessSentence(data)
mlearner.learning(["anh", "nho", "em", "nhieu", "lam"])
print(mlearner.guess("anh nho em nhieu lam"))
#manager.save_indices_as_json(data, './data/runtime/fulldata.json')