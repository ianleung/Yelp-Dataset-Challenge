import json
from pprint import pprint
#import pymysql

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
tablefile = '/Users/ruopingxu/Google Drive/4B/ECE356/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json';
table = 'user';


def create_checkin():
    string = "DROP TABLE IF EXISTS checkin; CREATE TABLE `checkin`(`type` VARCHAR(100), business_id VARCHAR(100));"
    for x in range (0,7):
        for y in range(0,24):
            dayhourlist.append("`%d-%d` INT" %(y,x))

    dayhourstring = ", ".join(dayhourlist)
    string += "DROP TABLE IF EXISTS CheckinHoursTable;"+\
        " CREATE TABLE CheckinHoursTable(`business_id` VARCHAR(100)," + dayhourstring +\
        ");"

    constraints = "alter table checkin add foreign key (business_id) references business(business_id);" +\
        "alter table CheckinHoursTable add foreign key (business_id) references business(business_id);"

    return string + constraints

def create_user():
    string = "DROP TABLE IF EXISTS user; CREATE TABLE user (`type` VARCHAR(100)," +\
            " `user_id` VARCHAR(100), `name` VARCHAR(100), `review_count` INT,"+\
            " `average_stars` VARCHAR(100), `yelping_since` VARCHAR(100), `fans` INT);"

    for y in compliment_fields:
        compliment_list.append("`%s` INT" % y )

    compliment_list_string = ", ".join(compliment_list)

    for y in vote_fields:
        vote_list.append("`%s` INT" %y)

    vote_list_string = ", ".join(vote_list)
    string += "DROP TABLE IF EXISTS EliteYears; CREATE TABLE EliteYears(`user_id` VARCHAR(100),`years` INT);"
    string += "DROP TABLE IF EXISTS ComplimentsTable; CREATE TABLE ComplimentsTable(`user_id` VARCHAR(100)," +\
        compliment_list_string + ");"
    string += "DROP TABLE IF EXISTS VotesTable; CREATE TABLE VotesTable(`user_id` VARCHAR(100)," + \
        vote_list_string + ");"
    string += "DROP TABLE IF EXISTS FriendTable; CREATE TABLE FriendTable (`user_id` VARCHAR(100), `friend_id` VARCHAR(100));"

    constraints = "alter table user add primary key (user_id);" +\
            "alter table EliteYears add foreign key (user_id) references user(user_id);"+\
            "alter table ComplimentsTable add foreign key (user_id) references user(user_id);"+\
            "alter table VotesTable add foreign key (user_id) references user(user_id);"+\
            "alter table FriendTable add foreign key (user_id) references user(user_id);"+\
            "alter table FriendTable add foreign key (friend_id) references user(user_id);"

    return string + constraints

def create_tip():
    string = "DROP TABLE IF EXISTS tip; CREATE TABLE `tip" + \
            "` (`type` VARCHAR(100), `business_id` VARCHAR(100), `text` "+\
            "VARCHAR(1000), `user_id` VARCHAR(100), `date` DATE, `likes` INT" +\
            ");"
    
    constraints = "alter table tip add foreign key (business_id) references business(business_id);"+\
        "alter table tip add foreign key (user_id) references user(user_id);"

    return string + constraints

def create_business():
    string = "DROP TABLE IF EXISTS "+ table +"; CREATE TABLE `" + table + \
            "` (`type` VARCHAR(100), `business_id` VARCHAR(100), `name` VARCHAR(100),"+\
            " `full_address` VARCHAR(1000),`city` VARCHAR(1000),`state` VARCHAR(1000),"+\
            " `latitude` INT, `longitude` INT, `stars` FLOAT(10,2),`open` TINYINT, `attributes` VARCHAR(10000));"
    string += "DROP TABLE IF EXISTS BusinessHours; CREATE TABLE BusinessHours (`business_id` VARCHAR(100)"
    for x in days_of_week:

        string += ", "+ x + "OPEN VARCHAR(100), "
        string += x + "CLOSE VARCHAR(100)"
    string += ");";
    string += "DROP TABLE IF EXISTS Categories; CREATE TABLE Categories (`business_id` VARCHAR(100),`categories` VARCHAR(100));"
    string += "DROP TABLE IF EXISTS Neighbourhoods; CREATE TABLE Neighbourhoods (`business_id` VARCHAR(100),`hood_name` VARCHAR(100)"
    string += ");"

    constraints = "alter table business add primary key (business_id);" +\
            "alter table Categories add foreign key (business_id) references business(business_id);"+\
            "alter table Neighbourhoods add foreign key (business_id) references business(business_id);"

    return string + constraints
  
def return_create_table_string(table_name):
    string = ""
    if table_name is 'checkin':
        string = create_checkin()
        #create dayhour table
    elif table_name is 'user':
        string = create_user()
    elif table_name is 'tip':
        string = create_tip()
    elif table_name is 'business':
        string = create_business()
    string += ");"
    return string

if __name__ == '__main__':

    filename = table + '_create_and_insert.sql'
    sql_file = open(filename, 'w')
    secondary_sql_file = open("sec_" + filename, 'w')
    
    sql_file.truncate()
    secondary_sql_file.truncate()

    createtablestring = return_create_table_string(table)
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
            main_sql = ""
            sql = ""
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
                elif k =="friends":
                    for x in v:
                        friend_id_list.append(x)
                elif k =="categories" and isinstance(v,dict):
                    for x in v:
                        categories_list.append(x)
                elif k =="neighbourhoods" and isinstance(v,dict):
                    for x in v:
                        neighbourhoods_list.append(x)
                elif k =="elite":
                    for x in v:
                        elite_years_list.append(str(x))
                elif k =="checkin_info":
                   for k, v in v.items():
                        checkin_columns_list.append(k)
                        checkin_values_list.append(str(v)) 
                elif k =="compliments" and isinstance(v,dict):
                    for k, v in v.items():
                        compliment_type_list.append(k)
                        compliment_count_list.append(str(v))
                elif k =="votes" and isinstance(v,dict):
                    for k, v in v.items():
                        vote_type_list.append(k)
                        vote_count_list.append(str(v))
                elif k =="hours" and isinstance(v,dict):
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
            main_sql = 'INSERT INTO %s (`%s`) VALUES ("%s");' % (table, columns, values)
            if table =='checkin':
                if len(checkin_values_list) > 0:
                    sql +='INSERT INTO CheckinHoursTable (`business_id`, `%s`) VALUES'+\
                    ' ("%s", "%s");' % (checkin_columns, businessid, checkin_values)
            
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
                    sql+= 'INSERT INTO  BusinessHours(`business_id`, `%s`) VALUES ("%s", "%s");' \
                        % (sorted_day_columns_list_string, businessid, sorted_day_columns_values_string)
                for x in neighbourhoods_list:
                    sql += 'INSERT INTO  Neighbourhoods(`business_id`, `hoodname`) VALUES ("%s", "%s");' \
                        % (businessid, x)
                for x in categories_list:
                    sql += 'INSERT INTO Categories (`business_id`, `categories`) VALUES ("%s", "%s");' \
                        % (businessid, x)
            


            if table =='user':
                # for x in elite_years_list:
                #     sql += 'INSERT INTO EliteYears (`user_id`, `years`) VALUES ("%s", "%s");' \
                #         % (userid, x) 
                # for x in friend_id_list:
                #     sql += 'INSERT INTO FriendTable (`user_id`, `friend_id`) VALUES ("%s", "%s");' \
                #         % (userid, x)
                if len(vote_values) > 0:
                    sql += 'INSERT INTO VotesTable (`user_id`, `%s`) VALUES ("%s", "%s");' \
                        % (vote_columns, userid, vote_values)
                if len(compliments_values) > 0:
                    sql += 'INSERT INTO ComplimentsTable (`user_id`, `%s`) VALUES ("%s", "%s");' \
                        % (compliments_columns, userid, compliments_values)
          
            #pprint(sql)
            sql_file.write(main_sql + "\n")
            secondary_sql_file.write(sql + "\n")


