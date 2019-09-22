from controller.manual import DataManager
from algorithms.machine_learning import *
manager = DataManager()
# manager.read_data()
manager.load_data(['full'])
manager.preprocessing({
    'full' : ['enterdel']
})
sentences = manager._data['full']
# print(manager.get_window_item('anh yêu em nhiều lắm', 5))
data = manager.create_window_items(sentences, 5)

summary_data = {
    'refer' : './data/runtime/refer_dict.json',
}
_data = manager.load_json_files(summary_data)
_data = _data['refer']

#print(data)
start_dir = './data/runtime/words/'
list_dirs = set(os.listdir(start_dir))
for word in data:
    cur_dir = start_dir + word
    if word not in list_dirs:
        os.mkdir(cur_dir)

    window_words = data[word]
    f = open(cur_dir + "/sentences.txt", "w")
    for X, y in window_words:
        f.write("%s\t%s\n" % (X, y))
    f.close()

    cur_data = []
    if word in _data:
        cur_data = set(_data[word])
    f = open(cur_dir + "/refer.txt", "w")
    for word_dict in cur_data:
        f.write("%s\n" % word_dict)
    f.close()

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

#
# refer_dict = dict()
# for words in data.keys():
#     for word in words.split():
#         if word not in refer_dict:
#             refer_dict[word] = []
#         refer_dict[word].append(words)
#
# manager.save_indices_as_json(refer_dict, './data/runtime/refer_dict.json')



#data = manager.create_window_items(sentences, 5, data)
