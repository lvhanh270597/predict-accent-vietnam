from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from system.helpers import file as fman
from system.helpers import data as dman
from models.model import Model
from os import path
import numpy as np
import pickle

class VectorGenerator(Model):

    def __init__(self, name="vectorgen", max_syl=5):
        super().__init__(name)
        self.name = name
        self.max_syl = max_syl
        self.vectorizer = CountVectorizer()
        self.scaler = StandardScaler()
        self.pca = PCA()

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
        X = self.vectorizer.fit_transform(self.sentences)
        X = X.toarray()

        features_vectors = self.feature_extraction()
        features_vectors = np.array(features_vectors)
        
        X = np.concatenate((X, features_vectors), axis=1)
        X = self.scaler.fit_transform(X)
        pca = PCA() # (n_components=10)
        X = self.pca.fit_transform(X)
        
        return X
    
    def run_for_test(self, sentences):
        X = self.vectorizer.transform(sentences)
        X = X.toarray()

        features_vectors = self.feature_extraction()
        features_vectors = np.array(features_vectors)
        
        X = np.concatenate((X, features_vectors), axis=1)
        X = self.scaler.transform(X)
        pca = PCA() # (n_components=10)
        X = self.pca.transform(X)
        
        return X

    def save_model(self, config):        
        model_path = config["model_path"]
        model_ext = config["model_ext"]
        vector_config = config["save_vectors"]
        model_path = path.join(model_path, vector_config["dir"])
        model_path = path.join(model_path, self.name)
        fman.make_dir(model_path)
        if vector_config["scaler"] is True:
            filename = config["format"] % self.name
            fullpath = path.join(model_path, "scaler.%s" % model_ext)
            fman.save_object(self.scaler, fullpath)
        if vector_config["pca"] is True:
            filename = config["format"] % self.name
            fullpath = path.join(model_path, "pca.%s" % model_ext)
            fman.save_object(self.pca, fullpath)
        if vector_config["vectorizer"] is True:
            filename = config["format"] % self.name
            fullpath = path.join(model_path, "vector.%s" % model_ext)
            fman.save_object(self.vectorizer, fullpath)
    
    def load_model(self, config):
        model_path = config["model_path"]
        model_ext = config["model_ext"]
        vector_config = config["load_vectors"]
        model_path = path.join(model_path, vector_config["dir"])
        model_path = path.join(model_path, self.name)
        if vector_config["scaler"] is True:
            filename = config["format"] % self.name
            fullpath = path.join(model_path, "scaler.%s" % model_ext)
            self.scaler = fman.load_object(fullpath)
        if vector_config["pca"] is True:
            filename = config["format"] % self.name
            fullpath = path.join(model_path, "pca.%s" % model_ext)
            self.pca = fman.load_object(fullpath)
        if vector_config["vectorizer"] is True:
            filename = config["format"] % self.name
            fullpath = path.join(model_path, "vector.%s" % model_ext)
            self.vectorizer = fman.load_object(fullpath)
        