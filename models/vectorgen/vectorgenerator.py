from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
from system.helpers import data as dman
from models.model import Model

class VectorGenerator(Model):

    def __init__(self, name="vectorgen", max_syl=5):
        super().__init__(name)
        self.name = name
        self.max_syl = max_syl

    def set_data(self, sentences, refer):
        self.sentences = sentences
        self.refer = refer

    def feature_extraction(self):
        features_vectors = []
        for i, sentence in enumerate(self.sentences):
            features_vectors.append([])
            refer_dict_feature = dman.get_dict_feature(sentence, self.refer, self.max_syl)
            features_vectors[i].extend(refer_dict_feature)
        return features_vectors

    def run(self):
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(self.sentences)
        X = X.toarray()

        features_vectors = self.feature_extraction()
        features_vectors = np.array(features_vectors)
        
        X = np.concatenate((X, features_vectors), axis=1)
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        pca = PCA() # (n_components=10)
        X = pca.fit_transform(X)
        
        return X
    
    def save(self, filedir):
        self.vocab.save(filedir, self.word)
        