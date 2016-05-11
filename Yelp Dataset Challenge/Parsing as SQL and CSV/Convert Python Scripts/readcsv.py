infile = open("/Users/ruopingxu/Google Drive/4B/ECE356/Lab1/yelp_dataset_challenge_academic_dataset/test.csv", 'r')

outfile = open("/Users/ruopingxu/Google Drive/4B/ECE356/Lab1/part2script0.sql", 'ab')
param_names = infile.readline()
param_names = 'votes__cool,user_id,review_id,review_text,votes__useful,business_id,stars,review_date,type,votes__funny'

line = infile.readline()
while line:
	if len(line) > 2:
		newline = "INSERT INTO Review({}) VALUES({});\n".format(param_names, line)
		outfile.write(newline)
	line = infile.readline()

infile.close()
outfile.close()