import nltk
import codecs
import pandas as pd
import company
import date
from os import listdir
from os.path import isfile, join


class minute_book(object):

    docs = []

    class doc(object):

        def __init__(self, file_name, text, raw_text):
            self.info = {}
            self.info['file_name'] = file_name
            self.info['text'] = text
            self.info['raw_text'] = raw_text
            self.info['company_names'] = ''
            self.info['dates'] = ''
            self.info['doc_date'] = ''

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
            text = ' '.join(text.split()) # removes extra white space
            raw_text = text # saves the raw text
            text = text.replace(',', '') # removes commas
            text = nltk.sent_tokenize(text) # tokenizes into sentences
            text = [nltk.word_tokenize(s) for s in text] # tokenizes the sentences into words

            # converts it to a doc object
            self.docs.append(self.doc(f, text, raw_text))

    def update_sentences(self):
        # this updates the sentences so that the company names appear as 
        # a single entry and not split by words
        pass


    def get_companies(self):
        return_list = []
        for d in self.docs:
            return_list.append(d.info['company_names'])
        return(return_list)


    def get_sentences(self):
        # returns a list of all sentences from all docs    
        return_sent = []
        for d in self.docs:
            return_sent.append(d.info['text'])
        return(return_sent)


    def company_extraction(self):
        self.docs = company.extraction(self.docs)


    def date_extraction(self):
        self.docs = date.extraction(self.docs)


    def mb_to_csv(self, path):
        res = []
        for d in self.docs:
            for c in d.info['company_names']:
                res.append([d.info['file_name'], c, d.info['doc_date']])

        res = pd.DataFrame(res)
        res.columns = ['file', 'company_names', 'date']
        res.to_csv(path, index = False)


    def print_summary(self):
        for d in self.docs:
            for cn in d.info['company_names']:
                print(d.file_name + ': ' + cn)

