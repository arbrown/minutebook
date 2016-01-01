import pandas as pd

class company_extract(object):

	def __init__(self, answer_path, results_path):
		answers = pd.read_csv(answer_path)
		results = pd.read_csv(results_path)

		answers = answers.values.tolist()
		results = results.values.tolist()

		# calculates the amount correct, missed and erroneous
		correct = []
		missed = []
		erroneous = []

		for r in results:
			found = False
			for a in answers:
				if r[0].lower() == a[0].lower() and r[1].lower() == a[1].lower():
					found = True
					correct.append(r)
					break

			if found == False:
				erroneous.append(r)

		for a in answers:
			found = False
			for r in results:
				if r[0].lower() == a[0].lower() and r[1].lower() == a[1].lower():
					found = True
					break

			if found == False:
				missed.append(a)

		print('correct')
		for c in correct:
			print(c)
		print('\n')		
		print('erroneous')
		for e in erroneous:
			print(e)
		print('\n')
		print('missed')
		for m in missed:
			print(m)
		print('\n')

		print('correct: ' + str(len(correct)))
		print('erroneous: ' + str(len(erroneous)))
		print('missed: ' + str(len(missed)))
		print('accuracy: ' + str(len(correct) / float(len(correct) + len(erroneous) + len(missed))))