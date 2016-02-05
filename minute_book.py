import pandas as pd
from os import listdir
from os.path import isfile, join
import nltk
import codecs
import company
import date
import grading


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
            if f[len(f) - 4:] == '.txt':
                with open(path + f, 'r') as reader:
                    text = reader.read()
                    text = ' '.join(text.split()) # removes extra white space
                    raw_text = text # saves the raw text
                    text = text.replace(',', '') # removes commas
                    text = nltk.sent_tokenize(text) # tokenizes into sentences
                    text = [nltk.word_tokenize(s) for s in text] # tokenizes the sentences into words
      
                    self.docs.append(self.doc(f, text, raw_text)) # converts it to a doc object


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
    
    def grade_results(self, answer_path, results_path):
        grading.grade(self.docs, answer_path, results_path)