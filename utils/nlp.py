from collections import defaultdict
from nltk.tokenize.regexp import RegexpTokenizer
from random import choice

class NLPCorpus(object):

    def __init__(self, name, corpus, tokenize_str, delimiter, n, max_length):
        self.name = name
        self.corpus = corpus
        self.tokenizer = RegexpTokenizer(tokenize_str)
        self.delimiter = delimiter
        self.n = n
        self.max_length = max_length

        # use set methods to set these variables
        self.tokenized_corpus = []
        self.startList = []
        self.ngramDict = defaultdict(list)
        self.unigramDict = defaultdict(list)
        self.set_tokenized_corpus()
        self.set_ngrams()

    def set_tokenized_corpus(self):
        self.tokenized_corpus = [self.tokenizer.tokenize(sentence) for sentence in self.corpus.split(self.delimiter)]
        # the last member is always empty, so remove it
        self.tokenized_corpus.pop()

    def set_ngrams(self):
        for sentence in self.tokenized_corpus:
            length = len(sentence)
            #append empty string to indicate the end of a tweet
            sentence.append('')
            if(length >= self.n):
                self.startList.append(tuple(sentence[0:self.n]))
                for i in range(length):
                    self.unigramDict[sentence[i]].append(sentence[i+1])
                    if i <= (length - self.n):
                        self.ngramDict[tuple(sentence[i:i+self.n])].append(sentence[i+self.n])
            else:
                self.startList.append(tuple(sentence))
                [self.unigramDict[sentence[j]].append(sentence[j+1]) for j in range(length)]
                self.ngramDict[tuple(sentence)].append('')

    def generate_sentence(self):
        # the start of a generated tweet is always the start of a tweet from the corpus
        key = choice(self.startList)
        sentence = list(key)
        sentence_length = len(" ".join(sentence))

        # keep track of how many n-grams only have a single choice as the following word
        single_choice = 0

        while True:
            if len(self.ngramDict[key]) == 1:
                single_choice += 1
            # use a unigram to select the next word to make it more likely that it's not a retweet
            if single_choice != 3:
                # select one of the words mapped to the current ngram key
                word = choice(self.ngramDict[key])
            else:
                word = choice(self.unigramDict[key[1]])
                single_choice = 0
            sentence_length += len(word) + 1
            if sentence_length <= self.max_length and word:
                sentence.append(word)
                key = key[1:] + (word,)
            else:
                break
        return " ".join(sentence)