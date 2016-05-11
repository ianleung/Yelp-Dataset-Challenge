import json
from pprint import pprint
import pymysql

data = []
dayhourlist = []
yearlist = []
compliment_list = []
vote_list = []
compliment_fields = ['profile', 'cute', 'funny','plain','list','writer','note','photos','hot','cool','more','useful']
vote_fields = ['funny','useful','cool']
days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Ssaturday","Sunday"]
#define variables to use
#yelp_academic_dataset_
tablefile = 'yelp_academic_dataset_checkin.json';
table = 'checkin';


def return_create_table_string(x):
    if x is 'checkin':
        string = "DROP TABLE IF EXISTS "+ table +"; CREATE TABLE `" + table + "`(`type` VARCHAR(100), business_id VARCHAR(100));"
        for x in range (0,7):
            for y in range(0,24):
                dayhour = "`%d-%d` INT" %(y,x)
                dayhourlist.append(dayhour)
        dayhourstring = ", ".join(dayhourlist)
        string += "DROP TABLE IF EXISTS CheckinHoursTable; CREATE TABLE CheckinHoursTable(`business_id` VARCHAR(100),";
        string += dayhourstring
        #create dayhour table
    elif x is 'user':
        string = "DROP TABLE IF EXISTS "+ table +"; CREATE TABLE `" + table + "` (`type` VARCHAR(100), `user_id` VARCHAR(100), `name` VARCHAR(100), `review_count` INT, `average_stars` VARCHAR(100), `yelping_since` VARCHAR(100), `fans` INT);"
        for y in compliment_fields:
            compliment = "`%s` INT" %(y)
            compliment_list.append(compliment)
        compliment_list_string = ", ".join(compliment_list)
        for y in vote_fields:
            vote = "`%s` INT" %(y)
            vote_list.append(vote)
        vote_list_string = ", ".join(vote_list)
        string += "DROP TABLE IF EXISTS EliteYears; CREATE TABLE EliteYears(`user_id` VARCHAR(100),`years` INT);"
        string += "DROP TABLE IF EXISTS ComplimentsTable; CREATE TABLE ComplimentsTable(`user_id` VARCHAR(100),";
        string += compliment_list_string    
        string += ");"
        string += "DROP TABLE IF EXISTS VotesTable; CREATE TABLE VotesTable(`user_id` VARCHAR(100),";
            #create compliments table
        string += vote_list_string
        string += ");"
        string += "DROP TABLE IF EXISTS FriendTable; CREATE TABLE FriendTable (`user_id` VARCHAR(100), `friend_id` VARCHAR(100)"
    elif x is 'tip':
        string = "DROP TABLE IF EXISTS "+ table +"; CREATE TABLE `" + table + "` (`type` VARCHAR(100), `business_id` VARCHAR(100), `text` VARCHAR(1000), `user_id` VARCHAR(100), `date` DATE, `likes` INT"
    elif x is 'business':
        string = "DROP TABLE IF EXISTS "+ table +"; CREATE TABLE `" + table + "` (`type` VARCHAR(100), `business_id` VARCHAR(100), `name` VARCHAR(100), `full_address` VARCHAR(1000),`city` VARCHAR(1000),`state` VARCHAR(1000), `latitude` INT, `longitude` INT, `stars` FLOAT(10,2),`open` TINYINT, `attributes` VARCHAR(10000));"
        string += "DROP TABLE IF EXISTS BusinessHours; CREATE TABLE BusinessHours (`business_id` VARCHAR(100)"
        for x in days_of_week:

            string += ", "+ x + "OPEN VARCHAR(100), "
            string += x + "CLOSE VARCHAR(100)"
        string += ");";
        string += "DROP TABLE IF EXISTS Categories; CREATE TABLE Categories (`business_id` VARCHAR(100),`categories` VARCHAR(100));"
        string += "DROP TABLE IF EXISTS Neighbourhoods; CREATE TABLE Neighbourhoods (`business_id` VARCHAR(100),`hood_name` VARCHAR(100)"
     
       

  
    string += ");"
    return string
    





filename = table + '_create_and_insert.sql'
with open(filename, 'w') as sql_file:
    sql_file.truncate()
    createtablestring = return_create_table_string(table)
    print(createtablestring)
    sql_file.write(createtablestring)

    with open(tablefile) as f:
        for line in f:
            data = json.loads(line)
            sorted_column_headers_list = []
            sorted_column_values_list = []
            user_id_list = []
            friend_id_list = []
            neighbourhoods_list = []
            categories_list = []
            vote_type_list = []
            vote_count_list = []
            compliment_type_list = []
            compliment_count_list = []
            dayhours = {}
            sorted_day_columns_list = []
            sorted_day_columns_values = []
            elite_years_list = []
            checkin_columns_list = []
            checkin_values_list = []
            for k, v in data.items():
                if k == "user_id":
                    userid = v
                    sorted_column_headers_list.append(k)
                    sorted_column_values_list.append(str(v))
                #if friendlist, compile list and insert to seperate table
                elif k == "business_id":
                    businessid = v
                    sorted_column_headers_list.append(k)
                    sorted_column_values_list.append(str(v))
                elif isinstance(v,list) and k =="friends":
                    for x in v:
                        friend_id_list.append(x)
                elif isinstance(v,list) and k =="categories":
                    for x in v:
                        categories_list.append(x)
                elif isinstance(v,list) and k =="neighbourhoods":
                    for x in v:
                        neighbourhoods_list.append(x)
                elif k =="elite":
                    for x in v:
                        elite_years_list.append(str(x))
                elif k =="checkin_info":
                   for k, v in v.items():
                        checkin_columns_list.append(k)
                        checkin_values_list.append(str(v)) 
                elif isinstance(v,dict) and k =="compliments":
                    
                    for k, v in v.items():
                        compliment_type_list.append(k)
                        compliment_count_list.append(str(v))
                elif isinstance(v,dict) and k =="votes":
                    for k, v in v.items():
                        vote_type_list.append(k)
                        vote_count_list.append(str(v))
                elif isinstance(v,dict) and k =="hours":
                    dayhours = v
                        
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
                else:
                   sorted_column_headers_list.append(k)
                   sorted_column_values_list.append(str(v))
            vote_columns = "`, `".join(vote_type_list)
            vote_values = '","'.join(vote_count_list)
           
            checkin_columns = "`, `".join(checkin_columns_list)
            checkin_values = '","'.join(checkin_values_list)

            compliments_columns = "`, `".join(compliment_type_list)
            compliments_values = '","'.join(compliment_count_list)
            value2 = []
            for s in sorted_column_values_list:
                s = s.replace('"', r'\"')
                value2.append(s)
            columns = "`, `".join(sorted_column_headers_list)
            values = '","'.join(value2)
            sql = 'INSERT INTO %s (`%s`) VALUES ("%s");' % (table, columns, values)
            if table =='checkin':
                if len(checkin_values_list) > 0:
                    sql +='INSERT INTO CheckinHoursTable (`business_id`, `%s`) VALUES ("%s", "%s");' % (checkin_columns, businessid, checkin_values)
            
            if table =='business':
                for k,v in dayhours.items():
                    sorted_day_columns_list.append(k+"CLOSE")
                    sorted_day_columns_list.append(k+"OPEN")
                    for k,v in v.items():
                        sorted_day_columns_values.append(str(v))
                sorted_day_columns_list_string = "`, `".join(sorted_day_columns_list)
                sorted_day_columns_values_string = '","'.join(sorted_day_columns_values)
                #if sorted columns > 1
                if len(sorted_day_columns_values)>0:
                    sql+= 'INSERT INTO  BusinessHours(`business_id`, `%s`) VALUES ("%s", "%s");' % (sorted_day_columns_list_string, businessid, sorted_day_columns_values_string)
                for x in neighbourhoods_list:
                    sql += 'INSERT INTO  Neighbourhoods(`business_id`, `hoodname`) VALUES ("%s", "%s");' % (businessid, x)
                for x in categories_list:
                    sql += 'INSERT INTO Categories (`business_id`, `categories`) VALUES ("%s", "%s");' % (businessid, x)
            


            if table =='user':
                for x in elite_years_list:
                    sql += 'INSERT INTO EliteYears (`user_id`, `years`) VALUES ("%s", "%s");' % (userid, x) 
                for x in friend_id_list:
                    sql += 'INSERT INTO FriendTable (`user_id`, `friend_id`) VALUES ("%s", "%s");' % (userid, x)
                if len(vote_values) > 0:
                    sql += 'INSERT INTO VotesTable (`user_id`, `%s`) VALUES ("%s", "%s");' % (vote_columns, userid, vote_values)
                if len(compliments_values) > 0:
                    sql += 'INSERT INTO ComplimentsTable (`user_id`, `%s`) VALUES ("%s", "%s");' % (compliments_columns, userid, compliments_values)
          
            #pprint(sql)
            sql_file.write(sql)

