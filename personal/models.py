from django.db import models
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Create your models here.
from SentimentAnalysis.settings import WordVec
from django import forms
import numpy as np
from SentimentAnalysis.settings import model,graph


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class Sentence(models.Model):

    def __init__(self,Sent):
        self.Sent = Sent

    def RegExpTokenizer(self,Sentence):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(Sentence)

    def Lemmatizing_Words(self,Words):
        Lm = WordNetLemmatizer()
        Lemmatized_Words = []
        for m in Words:
            Lemmatized_Words.append(Lm.lemmatize(m))
        return Lemmatized_Words

    def Eliminate_Stop_Word(self,Words):
        stop_words = set(stopwords.words("english"))
        filtered_words = []
        for w in Words:
            if w not in stop_words:
                filtered_words.append(w)
        return filtered_words

    def eliminate_irrelevent_Word(self,Words):
        #print(ListWords)
        #elimnate words
        Word = self.RegExpTokenizer(Words)
        Word = [item.lower() for item in Word]
        for m in Word:
            if len(m) <=3:
                Word.remove(m)
            if m == 'this':
                Word.remove(m)
        return Word
    def Word_Prep(self):
        Words =  self.RegExpTokenizer(self.Sent)
        Words =  self.Eliminate_Stop_Word(Words)
        Words = self.Lemmatizing_Words(Words)
        #print(Words)
        Words = self.eliminate_irrelevent_Word(' '.join(Words))
        #print(Words)
        return Words

    def get_Embedding_one_sent(self,Words):
        SentsEmb = []
        listWords = list(WordVec.wv.vocab)
        # on Va récuperer l'embeding de chaque sentence avec l'average des vecteur qui le compose
        for word in Words:  # S est la phrase , t est la class
            # Average of embeding of all words in sentence
            if word not in listWords:
                listzeros = [0] * 100
                SentsEmb.append(listzeros)
            elif word in listWords:
                SentsEmb.append(WordVec[word])
            else:
                print('word prob !!!!')

        return SentsEmb

    def fix_sentence_length(self,length,exemple):
        if len(exemple) > length:
            exemple = exemple[:length]
        elif len(exemple) < length:
            for i in range(length - len(exemple)):
                listzeros = [0] * 100
                exemple.append(listzeros)
        return exemple

    def predection(self):
        ex = self.Word_Prep()
        ex = self.get_Embedding_one_sent(ex)
        ex = self.fix_sentence_length(100, ex)
        ex = np.reshape(ex, (1, 100, 100))
        with graph.as_default():
            return model.predict(np.array(ex))

