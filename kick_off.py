import minute_book
from grading import company_extract

# data locations
text_path = '/home/matt/MinuteBook/Data/Extraction/'
results_path = '/home/matt/MinuteBook/Data/extract_results.csv'
answer_path = '/home/matt/MinuteBook/Data/answer_key.csv'

text_path = '/home/matt/MinuteBook/Data/Extraction_select/'
results_path = '/home/matt/MinuteBook/Data/extract_results_select.csv'
answer_path = '/home/matt/MinuteBook/Data/answer_key_select.csv'


# runs the minute book functions
mb = minute_book.minute_book() # creating a minute_book object
# mb.pdf_to_text(pdf_path, text_path) # converts the pdfs to text
mb.load_docs(text_path) # loads the documents
mb.company_extraction() # extracts the company names
# mb.print_summary()
# mb.date_extraction() # finds the date of the document
mb.save_minute_book(results_path) # saves the minute book 

# grades the results
company_extract(answer_path, results_path)