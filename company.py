
def extraction(docs):

    company_tags = ['llc', 'l.l.c', 'inc', 'inc.']

    # cleans up the company names
    def clean_company_names(company_names):
        company_names = list(set(company_names)) # removes duplicates
        # removes punctuation from the company name
        company_names = [c.replace(',', '') for c in company_names]
        company_names = [c.replace('.', '') for c in company_names]

        # removes entries that are only a company tag
        company_names = [c for c in company_names if c.lower() not in company_tags]

        # print('company phase 1')
        # print(company_names)

        # removes entries that are duplicates with extra junk
        new_cn = []
        for c1 in company_names:
            keep = True
            # tests if we want c1 in our new list            
            for c2 in company_names:
                if c1.lower() != c2.lower() and c2.lower() in c1.lower():
                    keep = False
                    break

            # print(c1)
            # print(keep)

            if keep:
                new_cn.append(c1)

        company_names = list(new_cn)
        # print('company phase 2')
        # print(company_names)

        new_cn = []
        # removes duplicates with different caps
        for c1 in company_names:
            keep = True
            for c2 in company_names:
                if c1 != c2 and c1.lower() == c2.lower() and c1.upper() == c1:
                    keep = False
            if keep:
                new_cn.append(c1)

        # print('company phase 3')
        # print(new_cn)
        return(new_cn)

    # this will be needed for determinaning the relationships 
    def udpate_sentences():
        pass


    # loops through the docs
    for i in range(len(docs)):
        text = docs[i].text

        # finds the company names
        company_names = []
        # loops through each sentence
        for s in text:
            # loops through each word
            for w in range(len(s)):
                # sees if the work is in the list of company tags
                if s[w].lower() in company_tags:
                    # as long as the first letter of the previous word is capitalized we keep going back
                    back_i = 1
                    company_name = s[w]
                    while w - back_i >= 0 and s[w - back_i][0] == s[w - back_i][0].upper() and s[w - back_i] != ':':
                        company_name = s[w - back_i] + ' ' + company_name
                        back_i += 1
                    company_names.append(company_name)
        
                    # print(s)
                    # print(company_name)

        company_names = clean_company_names(company_names) # removes erronious names
        docs[i].company_names = company_names # adds the company names to the doc object

    # returns the updated docs
    return(docs)
 