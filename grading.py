import pandas as pd

class grade(object):

    def __init__(self, docs, answer_path, results_path):
        # reads in the answer key
        df_answers = pd.read_csv(answer_path)
        answers = df_answers.values.tolist()
        grade = []
        # combines all the docs into a single list
        results = []
        for d in docs:
            file_name = d.info['file_name']
            comp_names = list(d.info['company_names'])
            results = results + [[file_name, c] for c in comp_names]

        # labels the ones that were correct and missing
        for a in answers:
            found = False
            for r in results:
                if r[0].lower() == a[0].lower() and r[1].lower() == a[1].lower():
                    found = True
                    grade.append('matched')
                    break
            
            if found == False:
                grade.append('not found')
        
        df_answers['grade'] = grade
        
        # labels teh ones that were not in the key
        for r in results:
            found = False
            for a in answers:
                if r[0].lower() == a[0].lower() and r[1].lower() == a[1].lower():
                    found = True
                    break
                
            if found == False:
                append_dict = {'document': r[0], 'company': r[1], 'grade': 'extra'}
                
                df_answers = df_answers.append(append_dict, ignore_index = True)
        
        # saves the results
        df_answers.to_csv(results_path)