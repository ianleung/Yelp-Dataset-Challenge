import simplejson as json
from pprint import pprint

TABLEFILE = '/Users/ruopingxu/TEMPORARY/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json';
#TABLEFILE = 'testBusiness.json'
# TABLEFILE = '/Users/ruopingxu/Google Drive/4B/ECE356/Labs356/Lab2postLab/testBusiness.json'
TABLE = 'business';
DAYS_OF_WEEK = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
SQL_FILENAME = TABLE + '_create_and_insert.sql'

def create_tables_in_sql():
    # create business table
    string = "DROP TABLE IF EXISTS "+ TABLE +"; CREATE TABLE `" + TABLE + "` (`type` VARCHAR(100), `business_id` VARCHAR(100), `name` VARCHAR(100), `full_address` VARCHAR(1000), `review_count` INT, `city` VARCHAR(1000),`state` VARCHAR(1000), `latitude` INT, `longitude` INT, `bstars` FLOAT(10,2),`open` VARCHAR(10));\n"

    # create business hours table
    string += "DROP TABLE IF EXISTS BusinessHours; CREATE TABLE BusinessHours (`business_id` VARCHAR(100)"
    for x in DAYS_OF_WEEK:
        string += ", "+ x + "OPEN VARCHAR(100), "
        string += x + "CLOSE VARCHAR(100)"
    string += ");";
    string += "DROP TABLE IF EXISTS Categories; CREATE TABLE Categories (`business_id` VARCHAR(100),`categories` VARCHAR(100));\n"
    string += "DROP TABLE IF EXISTS Neighbourhoods; CREATE TABLE Neighbourhoods (`business_id` VARCHAR(100),`hood_name` VARCHAR(100));\n"
    string += "DROP TABLE IF EXISTS Attributes; CREATE TABLE Attributes(business_id VARCHAR(100), attribute_name VARCHAR(50), attribute_value VARCHAR(50));"

    return string

def get_nested_kv_pair(json_obj):
    pairs = []
    for k, v in json_obj.items():
        if isinstance(v, dict):
            inner_pairs = get_nested_kv_pair(v)
            for p in inner_pairs:
                pairs.append((k+ "_" + p[0], p[1]))
        else:
            pairs.append((k, v))

    return pairs


def json_to_sql():
    with open(SQL_FILENAME, 'w') as sql_file:
        sql_file.truncate()
        create_table_strings = create_tables_in_sql()
        sql_file.write(create_table_strings)

        with open(TABLEFILE) as f:
            for line in f:

                data = json.loads(line.replace("\'", ""))
                sorted_column_headers_list = []
                sorted_column_values_list = []
                neighbourhoods_list = []
                categories_list = []
                dayhours = {}
                sorted_day_columns_list = []
                sorted_day_columns_values = []
                full_address = ''
                attributes = []

                for k, v in data.items():
                    if k == "business_id":
                        businessid = v
                        sorted_column_headers_list.append(k)
                        sorted_column_values_list.append(str(v.encode('ascii','replace')))
                    elif k == "full_address":
                        full_address = v
                    elif isinstance(v,list) and k =="categories":
                        for x in v:
                            categories_list.append(x)
                    elif isinstance(v,list) and k =="neighborhoods":
                        for x in v:
                            neighbourhoods_list.append(x)
                    elif isinstance(v,dict) and k =="hours":
                        dayhours = v
                    elif k == "attributes" and isinstance(v, dict):
                        attributes = get_nested_kv_pair(v)
                    elif isinstance(v,dict):
                        for k, v in v.items():
                            if isinstance(v,dict):
                                for k, v in v.items():
                                    sorted_column_headers_list.append(k)
                                    sorted_column_values_list.append(str(v))
                            else:
                                sorted_column_headers_list.append(k)
                                sorted_column_values_list.append(str(v))
                    elif isinstance(v,unicode):
                        sorted_column_headers_list.append(k)
                        sorted_column_values_list.append(v.encode('ascii','replace')) 
                    elif k == "stars":
                        sorted_column_headers_list.append("bstars")
                        sorted_column_values_list.append(str(v))
                    else:
                        sorted_column_headers_list.append(k)
                        sorted_column_values_list.append(str(v))

                columns = "`, `".join(sorted_column_headers_list)
                values = '","'.join(sorted_column_values_list)
                sql = 'INSERT INTO %s (`%s`) VALUES ("%s");\n' % (TABLE, columns, values)

                # make daily hours table
                for k,v in dayhours.items():
                    sorted_day_columns_list.append(k+"CLOSE")
                    sorted_day_columns_list.append(k+"OPEN")
                    for k,v in v.items():
                        sorted_day_columns_values.append(str(v))
                sorted_day_columns_list_string = "`, `".join(sorted_day_columns_list)
                sorted_day_columns_values_string = '","'.join(sorted_day_columns_values)

                # if sorted_day_columns_values_string:
                #     sql+= 'INSERT INTO  BusinessHours(`business_id`, `%s`) VALUES ("%s", "%s");\n' % (sorted_day_columns_list_string, businessid, sorted_day_columns_values_string)

                # # populate neighborhood table
                # for x in categories_list:
                #     sql += 'INSERT INTO  Categories(`business_id`, `categories`) VALUES ("%s", "%s");\n' % (businessid, x)
                # # populate catergories table
                # for x in neighbourhoods_list:
                #     sql += 'INSERT INTO  Neighbourhoods(`business_id`, `hood_name`) VALUES ("%s", "%s");\n' % (businessid, x)
                
                # for x in attributes:
                #     sql += 'INSERT INTO Attributes(business_id, attribute_name, attribute_value) VALUES ("%s", "%s", "%s");\n' % (businessid, x[0], str(x[1]))

                sql_file.write(sql.encode('ascii','replace') + '\n')


if __name__ == '__main__':
    json_to_sql()