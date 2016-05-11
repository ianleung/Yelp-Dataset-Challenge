import simplejson as json


fields = ['votes__cool',
		'user_id',
		'review_id',
		'text',
		'votes__useful',
		'business_id',
		'stars',
		'date',
		'type',
		'votes__funny']

param_names = 'votes__cool,user_id,review_id,review_text,votes__useful,business_id,stars,review_date,type,votes__funny\n'


def json_to_csv(infile, outfile):
	with open(outfile, 'wb+') as fout:
		fout.write(param_names)
		with open(infile, 'rb') as fin:
			for line in fin:
				line_contents = json.loads(line)
				outlist = json_to_list(line_contents)

				output = "\"" + "\",\"".join(outlist) + '\"\n'
				fout.write(output)

def json_to_list(d):
	value_list = []
	for f in fields:
		to_insert = ""
		if '__' in f:
			base, sub = f.split('__', 1)
			if base not in d:
				to_insert = "0"
			else:
				to_insert = str(d[base][sub])
		elif isinstance(d[f], unicode):
			to_insert = str(d[f].encode('punycode'))
		else:
			to_insert=str(d[f])
		value_list.append(to_insert.replace('\n', ''))

	return value_list

if __name__ == '__main__':
	infilename = 'yelp_academic_dataset_review.json'
	#infilename = 'test.json'
	outfilename = 'yelpdata.csv'
	json_to_csv("/Users/ruopingxu/TEMPORARY/" + infilename,
		"/Users/ruopingxu/TEMPORARY/" + outfilename)