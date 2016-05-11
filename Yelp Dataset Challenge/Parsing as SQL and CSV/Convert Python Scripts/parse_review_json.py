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

param_names = 'votes__cool,user_id,review_id,review_text,votes__useful,business_id,stars,review_date,type,votes__funny'


def json_to_sql(infile, outfile):
	with open(outfile, 'wb+') as fout:
		setup = "DROP TABLE IF EXISTS Review; CREATE TABLE Review(user_id VARCHAR(100)," +\
				"review_id VARCHAR(100), review_text VARCHAR(10000), "+\
				"votes__cool INT, business_id VARCHAR(100),votes__funny INT, stars INT, "+\
				"review_date DATE, type VARCHAR(10), votes__useful INT) ENGINE= MyISAM; "
		constraints = "alter table Review add primary key (review_id);"+\
				"alter table Review add foreign key (business_id) references business(business_id);"+\
				"alter table Review add foreign key (user_id) references User(user_id)"
		fout.write(setup)
		with open(infile, 'rb') as fin:
			for line in fin:
				line_contents = json.loads(line)
				output = new_command(json_to_list(line_contents))
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

def new_command(params):
	return "INSERT INTO Review({}) VALUES({});\n".format(param_names, str(params)[1:-1])

if __name__ == '__main__':
	infilename = '/Users/ruopingxu/Google Drive/4B/ECE356/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
	outfilename = 'insert_reviews.sql'
	json_to_sql(infilename, outfilename)