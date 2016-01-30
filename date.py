import dateutil.parser as dparser
import nltk
import operator
import re

def extraction(docs):

    # months
    months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'October', 'November', 'December']
    months_short = ['Jan', 'Feb', 'March', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Oct', 'Nov', 'Dec']
    months_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    months_num_short = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    # days
    days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
    '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    days_short = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
    '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

    # years
    years = [str(i) for i in range(1800, 2100)]
    years_short = [str(y)[2:] for y in range(1900, 2000)]

    # dividers
    dividers = ['-', '/']

    # constructs the regular expressions
    reg_ex_num = '(?:' + '|'.join(months_num + months_num_short) + ')(?:' + '|'.join(dividers) + ')(?:' + '|'.join(days + days_short) + ')(?:' + '|'.join(dividers) + ')(?:' + '|'.join(years + years_short) + ')'
    reg_ex_words = '(?:' + '|'.join(months + months_short) + ')\W(?:' + '|'.join(days + days_short) + ')\,\W(?:' + '|'.join(years) + ')'

    reg_ex = re.compile('(?:' + reg_ex_num + ')|(?:' + reg_ex_words + ')')
    test_text = 'just a test 01/01/2010, just a test 2/2/2002 just a test 3/3/03 just a test 01-01-2010, Nov 20, 1985, January 03, 2015'

    # loops the documents
    for d in range(len(docs)):
        doc_dates = {}
        text = docs[d].info['raw_text']
        dates = reg_ex.findall(text) # finds all the dates

        # converts the dates to a dictionary
        for date in dates:
            if date not in doc_dates:
                doc_dates[date] = 1
            else:
                doc_dates[date] += 1

        # finds the date with the highest occurance
        doc_date = max(doc_dates.iteritems(), key=operator.itemgetter(1))[0]
 
        # adds all dates and the main date to the doc object
        docs[d].info['dates'] = doc_dates
        docs[d].info['doc_date'] = doc_date
        
    return(docs)