


# from models.machine_learning import MachineLearner
# learner = MachineLearner()
# data, models = learner.build()
# learner.test(data, models)
#
# from data_structures.sentence import  Sentence
# sentence = Sentence('1 năm bản quyền miễn phí phần mềm bảo mật hàng đầu - Thủ thuật - Dân trí Báo điện tử của báo khuyến học & Dân Trí Giao diện PDA Mua chung Blog Tấm lòng nhân ái Tuần báo Mua bán Bé xinh Diễn đàn dân trí English Sự kiện Xã hội Thế giới Thể thao Giáo dục Nhân ái Kinh doanh Văn hóa Pháp luật Nhịp sống trẻ Tình yêu Sức khỏe Sức mạnh số Ô tô - Xe máy Chuyện lạ Bạn đọc Vi tính Điện thoại Thủ thuật "Bom tấn" tại hội nghị di động thế giới MWC 2012 Tranh chấp bản quyền thương hiệu iPad tại Trung Quốc Triển lãm CES 2012 CEO Facebook đến Việt Nam Thứ Bẩy, 25/02/2012 - 15:47 1 năm bản quyền miễn phí phần mềm bảo mật hàng đầu (Dân trí) - Bài viết dưới đây sẽ giúp bạn tận dụng cơ hội để sở hữu bản quyền của Trend Micro Titanium 2012, một trong những phần mềm bảo mật mạnh mẽ nhất hiện nay, với hạn dùng lên đến tận 1 năm.')
# sentence.set_vocab(["tấm lòng"])
# print(sentence.detect_name())
#
# print(sentence.restore())
# from underthesea import sent_tokenize
# f = open("./data/raw/VNESEcorpus.txt")
# data = f.read()
# f.close()
#
# data = sent_tokenize(data)
#
# f = open("./data/raw/sentences.txt", "w")
# for line in data:
#     f.write("%s\n" % line)
# f.close()
# from data_structures.sentence import Sentence
# from helpers import file as fman
# from nltk.tokenize import word_tokenize
# data = fman.load_text("./data/Viet74K.txt")
# instance = Sentence()
# vocab = set()
# for word in data:
#     for item in word_tokenize(word):
#         if item.isalpha():
#             item = item.lower()
#             instance.set_sentence(item)
#             item = instance.remove_accents()
#             vocab.add(item)
#
# fman.save_text(vocab, "./data/listwords.txt")
