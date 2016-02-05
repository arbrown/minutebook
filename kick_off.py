import minute_book
import os

# data locations

train_path = os.getenv('HOME') + '/GitHub/minutebook/Data/upload_folder/'
# test_path = '/home/matt/MinuteBook/Data/Test/'

# runs the minute book functions
mb = minute_book.minute_book() # creating a minute_book object
mb.load_docs(train_path) # loads the documents
# mb.document_type() # classifies the documents
mb.company_extraction() # extracts the company names (CORPORATION WILL NOT BE CAPITALIZED)
mb.grade_results(train_path + 'answer_key.csv', train_path + 'results.csv')
print(mb.docs[15].info['company_names'])
# print(mb.docs[1].info['file_name'])
# print(mb.docs[1].info['company_names'])
# print(mb.docs[1].info.keys())
# mb.date_extraction() # finds the date of the document
# mb.mb_to_csv(results_path)

# mb.mb_to_csv(results_path) # saves the minute book

# grades the results
# company_extract(answer_path, results_path)

# from gensim import corpora, models, similarities
# from gensim.models import Word2Vec
# model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)

# llc 'acadia management company llc'
# member 'acadia healthcare company inc'

# test = mb.docs[6]
# sentences = test.info['text']

# test = mb.docs[7]
# sentences = sentences + test.info['text']

# from gensim import corpora, models, similarities
# from gensim.models import Word2Vec
# model = Word2Vec(sentences, size=1000, window=2, min_count=1, workers=4)

# print(sentences[0])

# print(model.similarity('berry petroleum company llc', 'brookstone holdings inc'))
# print(model.similarity('berry petroleum company llc', 'big blue audio llc'))