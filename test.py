# from algorithms.machine_learning import GuessSentence
# from nltk.tokenize import word_tokenize
#
# query = "co le pham chat kho ren luyen nhat ma cung la mau chot de quyet dinh thanh bai do la su kien tri"
# list_inputs = list(set(word_tokenize(query)))
# guesser = GuessSentence()#datadir=None, list_words=list_inputs)
# guesser.learning()#list_inputs)
# guesser.score(None, "./results/scores.txt")
#
# result = guesser.guess(query)
# print(result)
#
# guesser.save_all("./data/models/") #_all("./data/models/")


# from algorithms.machine_learning import GuessOne
#
# guesser = GuessOne("co", "./data/words/")
# guesser.get_bow_vectors()
# guesser.add_dict_feature()
# guesser.train_test_split()
# guesser.load()
# print(guesser.guess("sao lai co the pham chat kho"))
#
# from controller.data import DataManager
# from controller.model import Modeler
#
# manager = DataManager()
#
# modeler = Modeler(manager)
#
# while True:
#     sentence = input("Enter your sentence: ")
#     result = modeler.guess(sentence)
#     print(result)

# from kernel.kernel import Kernel
#
# kn = Kernel()
# kn.add_document("thằng chó đẻ mặt lồn. đụ má mày!!! thằng lồn chó")
# while True:
#     sentence = input("Enter your sentence: ")
#     result = kn.guess(sentence)
#     print(result)








