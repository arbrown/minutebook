def extraction(docs):

    company_tags = ['llc', 'l.l.c', 'inc', 'inc.']
    compnay_tags_short = ['llc', 'inc']
    company_dict = {'llc': ['llc', 'l.l.c'], 'inc': ['inc', 'inc.']}

    def clean_company_names(company_names):
        # cleans up the company names
        company_names = list(set(company_names)) # removes duplicates
        # removes punctuation from the company name
        company_names = [c.replace(',', '') for c in company_names]
        company_names = [c.replace('.', '') for c in company_names]


        company_names = [c.lower() for c in company_names]

        # removes entries that are only a company tag
        company_names = [c for c in company_names if c.lower() not in company_tags]

        # removes entries that are duplicates with extra junk
        new_cn = []
        for c1 in company_names:
            keep = True
            # tests if we want c1 in our new list
            for c2 in company_names:
                if c1.lower() != c2.lower() and c2.lower() in c1.lower():
                    keep = False
                    break

            if keep:
                new_cn.append(c1)

        company_names = list(new_cn)

        new_cn = []

        # removes duplicates with different caps
        for c1 in company_names:
            keep = True
            for c2 in company_names:
                if c1 != c2 and c1.lower() == c2.lower() and c1.upper() == c1:
                    keep = False
            if keep:
                new_cn.append(c1)

        return(new_cn)


    def combine_entries(list_a, list_b):

        # converts everything to lower
        list_a = [a.lower() for a in list_a]
        list_b = [b.lower() for b in list_b]

        new_a = list_a
        offset = 0

        for a in range(len(list_a) - (len(list_b) - 1)):

            # found the begining of the sublist
            if list_b[0] == list_a[a]:
                found_b = True

                # checks if the whole thing is there
                for b in range(1, len(list_b)):
                    if list_b[b] != list_a[a + b]:
                        found_b = False
                        break

                # if we found the whole thing then we modify the list
                if found_b:
                    new_entry = list_a[a:(a + len(list_b))]
                    new_entry = [str(n) for n in new_entry]
                    new_entry = ' '.join(new_entry)
                    new_a = new_a[:(a - offset)] + [new_entry] + list_a[(a + len(list_b)):]
                    offset += len(list_b) - 1
        
        return(new_a)


    def udpate_sentences(text, comp_names):
        # this formats the company names so they are a single
        # entry in the sentence list
        for c in comp_names:
            for i in range(len(text)):
                txt = text[i]
                text[i] = combine_entries(txt, c.split())

        return(text)


    def standardize_comp_titles(text):
        # formats the company titles so they are uniform
        # loops through each sentence
        for s in text:
            # initially loops through each word and standarizes
            # the company titles
            for w in range(len(s)):
                if s[w].lower() in company_tags:
                    for key in company_dict:
                        if s[w].lower() in company_dict[key]:
                            s[w] = key
                            break

        return(text)


    # loops through the docs
    for i in range(len(docs)):
        company_names = []
        text = docs[i].info['text']

        # standarizes the company titles
        text = standardize_comp_titles(text)
        docs[i].info['text'] = text

        for s in text:

            # loops through each word
            for w in range(len(s)):
                # sees if the work is in the list of company tags
                if s[w].lower() in compnay_tags_short:
                    # as long as the first letter of the previous word is capitalized we keep going back
                    back_i = 1
                    company_name = s[w]
                    while w - back_i >= 0 and s[w - back_i][0] == s[w - back_i][0].upper() and s[w - back_i] != ':':
                        company_name = s[w - back_i] + ' ' + company_name
                        back_i += 1
                    company_names.append(company_name)
        

        company_names = clean_company_names(company_names) # removes erronious names
        
        docs[i].info['company_names'] = list(company_names) # adds the company names to the doc object
        docs[i].info['text'] = list(udpate_sentences(text, company_names)) # updates the sente

    # returns the updated docs
    return(docs)
 