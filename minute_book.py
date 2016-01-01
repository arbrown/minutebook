import nltk
import codecs
import pandas as pd
import company 
from os import listdir
from os.path import isfile, join


class minute_book(object):

    docs = []

    def __init__(self):
        pass

    def pdf_to_text(self):
        pass

    def load_docs(self, path):

        # this makes the ascii erros get replaced with a space
        def handler(e): 
            return (u' ',e.start + 1) 
        codecs.register_error('mine', handler) 

        # reads in the files
        data_files = [f for f in listdir(path) if isfile(join(path, f))]

        for f in data_files:
            with open(path + f, 'r') as reader:
                text = unicode(reader.read(), 'utf-8')

            # converts to ascii and does a little cleaning
            text = text.encode('ascii', 'mine') # converts to ascii and puts spaces for things it can't decode
            text = text.replace(',', '') # removes commas
            text = ' '.join(text.split()) # removes extra white space
            text = nltk.sent_tokenize(text) # tokenizes into sentences
            text = [nltk.word_tokenize(s) for s in text] # tokenizes the sentences into words

            # converts it to a doc object
            self.docs.append(self.doc(f, text))

    def company_extraction(self):
        self.docs = company.extraction(self.docs)

    def date_extraction(self):
        pass

    def save_minute_book(self, path):
        res = []
        for d in self.docs:
            print(d.file_name)
            for c in d.company_names:
                res.append([d.file_name, c])

        res = pd.DataFrame(res)
        res.columns = ['file', 'company_names']
        res.to_csv(path, index = False)

    def print_summary(self):
        for d in self.docs:
            for cn in d.company_names:
                print(d.file_name + ': ' + cn)


    class doc(object):

        company_names = ''    

        def __init__(self, file_name, text):
            self.file_name = file_name
            self.text = text 