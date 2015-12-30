import data_prep
import Levenshtein as lv

docs_path = 'C:/Users/Matt/Dropbox (MinuteBook)/MinuteBook Team Folder/Development/Proof of Concepts/Document Classification/data/documents'
save_path = 'C:/Users/Matt/Dropbox (MinuteBook)/MinuteBook Team Folder/Development/Proof of Concepts/Document Classification/data'
tdm = data_prep.create_tdm(docs_path)
tdm.to_csv(save_path + '/tdm.csv')