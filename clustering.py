import gensim, logging
import nltk
import codecs
import pandas as pd

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
# this makes the erros get a space
def handler(e): 
    return (u' ',e.start + 1) 
codecs.register_error('mine', handler) 

# read in the data
data_path = '/home/matt/minutebook/Entity Extraction/data/txt/'
files = ['99CentsOnlyStoresLlc_20131108_10-Q_EX-3.2.txt', 'AcadiaHealthcareCompanyInc_20140306_S-4_EX-3.6.txt']
# files = ['AcadiaHealthcareCompanyInc_20140306_S-4_EX-3.6.txt']
docs = []
for f in files:
    with open(data_path + f, 'r') as reader:
        # docs.append(reader.read())
        docs.append(unicode(reader.read(), 'utf-8'))

# cleans the text
for i in range(len(docs)):
    docs[i] = docs[i].encode('ascii', 'mine') # converts to ascii and puts spaces for things it can't decode
    docs[i] = ' '.join(docs[i].split()) # removes extra white space
    docs[i] = docs[i].replace(':', '')
    docs[i] = docs[i].lower()

# tokenizes the sentenses and words
sents = []
for d in docs:
    sent = nltk.sent_tokenize(d)
    sents += [nltk.word_tokenize(s) for s in sent]

# min_count is the cutoff for the number of occurances a word
# has to have for it to be included in the output, default is 5
# size is the number of NN layers or dimentions default is 100
# window is the maximum distance between the current and predicted word within a sentence
# workers is the number of cores

# iterates over the model parameters
windows = [2, 3, 4, 5, 6, 7, 8, 9, 10]
sizes = range(20, 500, 20)
hit = False
res = []

for w in windows:
    for s in sizes:
        model = gensim.models.Word2Vec(sents, min_count = 2, window = w, size = s)
        similar = model.most_similar('abilene')

        for sim in similar:
            res.append([sim[0], sim[1], w, s])


        # top_words = [sim[0] for sim in similar]

        # if '99' in top_words:
        #     hit = True
        #     hit_w = w
        #     hit_s = s
        #     break

res = pd.DataFrame(res)
res.columns = ['word', 'prox', 'window', 'layers']
res.to_csv(data_path + 'output.csv', index = False)



