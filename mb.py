import nltk
import codecs
from os import listdir
from os.path import isfile, join

class file_data(object):

    text = ''
    company_names = ''    

    def __init__(self, file_name):
        self.file_name = file_name


class company_extraction(object):

    docs = []

    def __init__(self, data_path):

        # this makes the ascii erros get replaced with a space
        def handler(e): 
            return (u' ',e.start + 1) 
        codecs.register_error('mine', handler) 

        # reads in the files
        data_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]

        for f in data_files:
            this_file = file_data(f)
            with open(data_path + f, 'r') as reader:
                text = unicode(reader.read(), 'utf-8')

            # converts to ascii and does a little cleaning
            text = text.encode('ascii', 'mine') # converts to ascii and puts spaces for things it can't decode
            text = text.replace(',', '') # removes commas
            text = ' '.join(text.split()) # removes extra white space
            text = nltk.sent_tokenize(text) # tokenizes into sentences
            text = [nltk.word_tokenize(s) for s in text] # tokenizes the sentences into words
            this_file.text = text

            # finds the company names
            company_tags = ['L.L.C', 'Inc', 'Inc.']
            company_names = []
            # loops through words looking for copany tags and then backtracks to add words to the company name
            for s in text:
                for w in range(len(s)):
                    if s[w] in company_tags:
                        # as long as the first letter of the previous word is capitalized
                        back_i = 1
                        company_name = s[w]
                        while w - back_i >= 0 and s[w - back_i][0] == s[w - back_i][0].upper() and s[w - back_i] != ':':
                            company_name = s[w - back_i] + ' ' + company_name
                            back_i += 1
                        company_names.append(company_name)
            
            company_names = self.clean_company_names(company_names) # removes erronious names
            this_file.company_names = company_names # adds the company names to the file object
            self.docs.append(this_file) # appends the completed file object to the docs list

 
    # cleans up the company names
    def clean_company_names(self, company_names):
        company_names = list(set(company_names)) # removes duplicates
        # removes all caps entrees
        new_cn = []
        for company_name in company_names:
            if company_name != company_name.upper():
                new_cn.append(company_name)

        return(new_cn)


    def udpate_sentences(self):
        pass